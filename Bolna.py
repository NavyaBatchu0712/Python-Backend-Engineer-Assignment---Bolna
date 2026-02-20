import requests
import time
import re
from datetime import datetime
import feedparser

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

STATUS_FEED_URL = "https://status.openai.com/history.atom"

seen_entries = set()
etag = None
last_modified = None

console = Console()


def strip_html(raw_html):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", raw_html)


def get_entry_datetime(entry):
    for attr in ["published_parsed", "updated_parsed", "created_parsed"]:
        value = getattr(entry, attr, None)
        if value:
            return datetime(*value[:6])
    return None


def determine_status_color(summary):
    summary_lower = summary.lower()

    if "resolved" in summary_lower:
        return "green"
    elif "degraded" in summary_lower:
        return "yellow"
    elif "investigating" in summary_lower:
        return "magenta"
    elif "error" in summary_lower or "down" in summary_lower:
        return "red"
    else:
        return "cyan"


def print_alert(timestamp, title, summary):
    clean_summary = strip_html(summary)
    status_color = determine_status_color(clean_summary)

    message = Text()
    message.append(f"[{timestamp}] ", style="bold cyan")
    message.append(f"Product: {title}\n", style="bold white")
    message.append("Status: ", style="bold white")
    message.append(clean_summary, style=status_color)

    panel = Panel(
        message,
        border_style=status_color,
        padding=(1, 2),
        box=box.ROUNDED
    )

    console.print(panel)


def fetch_feed():
    global etag, last_modified

    headers = {}
    if etag:
        headers["If-None-Match"] = etag
    if last_modified:
        headers["If-Modified-Since"] = last_modified

    try:
        response = requests.get(STATUS_FEED_URL, headers=headers, timeout=10)
    except requests.RequestException as e:
        console.print(f"[red]Error fetching feed:[/red] {e}")
        return None

    if response.status_code == 304:
        return None

    if response.status_code != 200:
        console.print(f"[red]Unexpected status code:[/red] {response.status_code}")
        return None

    etag = response.headers.get("ETag")
    last_modified = response.headers.get("Last-Modified")

    return feedparser.parse(response.text)


def process_feed(feed):
    if not feed or not hasattr(feed, "entries"):
        return

    for entry in feed.entries:
        entry_id = getattr(entry, "id", None) or getattr(entry, "link", None)

        if not entry_id or entry_id in seen_entries:
            continue

        seen_entries.add(entry_id)

        published_time = get_entry_datetime(entry)
        timestamp = (
            published_time.strftime("%Y-%m-%d %H:%M:%S")
            if published_time
            else "Unknown Time"
        )

        title = getattr(entry, "title", "No Title")
        summary = getattr(entry, "summary", "No Details Available")

        print_alert(timestamp, title, summary)


def main():
    console.print(
        Panel(
            "[bold white]🚨 OpenAI Status Live Monitor 🚨[/bold white]",
            style="bold blue",
            box=box.DOUBLE
        )
    )

    while True:
        feed = fetch_feed()
        process_feed(feed)
        time.sleep(60)


if __name__ == "__main__":
    main()
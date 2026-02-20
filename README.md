# OpenAI Status Live Monitor

A lightweight Python monitoring tool that automatically tracks service updates from the OpenAI Status Page and prints structured alerts in real-time.

## Problem Statement

Build a Python script or lightweight application that automatically tracks and logs service updates from the OpenAI Status Page.

Whenever there is a new incident, outage, degradation, or resolution update related to any OpenAI API product, the program:

- Detects the update automatically  
- Prints the affected product or service  
- Prints the latest status message or event  
- Avoids inefficient polling  
- Scales efficiently to monitor multiple status pages  

The solution does not persist data or require a UI. Console output is sufficient.


## Design Approach

This solution uses:

- HTTP conditional requests (ETag and Last-Modified headers)
- Efficient polling with 304 Not Modified handling
- RSS feed parsing using feedparser
- Defensive parsing for inconsistent fields
- Clean terminal formatting using rich

Instead of repeatedly downloading the entire feed, the script sends conditional headers to fetch updates only when changes occur. This approach is efficient and scalable.


## Features

- Live monitoring of the OpenAI Status feed
- Automatic detection of new incidents
- Clean terminal output
- HTML stripping from feed summaries
- Defensive error handling
- Network timeout handling
- Optimized polling every 60 seconds


## Installation

Clone the repository:

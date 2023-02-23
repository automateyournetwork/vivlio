# vivlio

Business Ready Documents for Meraki

## Current API Coverage

Organizations

Organization Devices

Organization Networks

Network Clients

## Installation

```console
$ python3 -m venv meraki
$ source meraki/bin/activate
(meraki) $ pip install vivlio
```

## Usage - Environment Variable - IMPORTANT

Please export / setup this environment variable prior to running vivlio

```console
(meraki) $ export MERAKI_DASHBOARD_API_KEY=<Meraki API Token>

```

## Usage - In-line

```console
(meraki) $ vivlio
```

## Recommended VS Code Extensions

Excel Viewer - CSV Files

Markdown Preview - Markdown Files

Markmap - Mindmap Files

Open in Default Browser - HTML Files

## Always On Sandbox

This code works with the always on sandbox! 

https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

```console
export MERAKI_DASHBOARD_API_KEY=fd6dd87d96915f21bc0e0b3d96a866ff0e53e381

(venv)$ pip install vivlio
(venv)$ mkdir vivlio_output
(venv)$ cd vivlio_output
(venv)/vivlio_output$ vivlio
(venv)/vivlio_output$ code . 
(Launches VS Code and you can view the output with the recommended VS Code extensions)
```
## Contact

Please contact John Capobianco if you need any assistance

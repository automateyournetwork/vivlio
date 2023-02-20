# vivlio

Business Ready Documents for Meraki

## Current API Coverage

Organizations

## Installation

```console
$ python3 -m venv meraki
$ source meraki/bin/activate
(meraki) $ pip install vivlio
```

## Usage - Help

```console
(meraki) $ vivlio --help
```

![vivlio Help](/images/help.png)

## Usage - In-line

```console
(meraki) $ vivlio --token <Meraki Token>
```

## Usage - Interactive

```console
(meraki) $ vivlio
Meraki Token: <Meraki Token>
```

## Usage - Environment Variables

```console
(meraki) $ export TOKEN=<Meraki API Token>

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
export TOKEN=

(venv)$ pip install vivlio
(venv)$ mkdir vivlio_output
(venv)$ cd vivlio_output
(venv)/vivlio_output$ vivlio
(venv)/vivlio_output$ code . 
(Launches VS Code and you can view the output with the recommended VS Code extensions)
```
## Contact

Please contact John Capobianco if you need any assistance

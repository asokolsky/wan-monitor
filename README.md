# WAN Status Monitor and Modem Power Cycler

## Problem Statement

My cable modem occasionally looses connection to ISP.
So my plan is:

* have the wan connectivity status being monitored, e.g. in a cron job
* if connection is lost - power cycle the modem

## Monitoring WAN connection

Modem status is represented as JSON and is saved into a file.
Periodically get new status, compare with the old one, act on it.

## Linting

While in src:

```
alex@latitude7490:~/Projects/wan-monitor/src$ mypy *.py
Success: no issues found in 3 source files
```

## Testing

While in src:

```
alex@latitude7490:~/Projects/wan-monitor/src$ python3 -m unittest *_test.py
```

## Runing

From command line:

```
alex@latitude7490:~/Projects/wan-monitor/src$ python3 monitor_modem.py
```
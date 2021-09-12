# WAN Status Monitor and Modem Power Cycler

## Problem Statement

My cable modem occasionally looses connection to ISP. So, the plan is:

* monitor the wan connectivity status;
* if connection is lost - powercycle the modem.

## Design

Modem status is represented as JSON and is saved into a file.
Periodically get new status, compare with the old one, act on it.

### WAN Connection States

WAN connectivity state is one of (see ConnectivityState):

* up - WAN gateway ping succeeds;
* sick - WAN gateway ping fails for up to ConnectivityStatus.wan_timeout_down
seconds, 9 by default;
* down - WAN gateway ping fails for more than 
ConnectivityStatus.wan_timeout_down seconds.

If the state is down and WAN gateway ping succeeds, there is an immediate
state transition to up, thus skipping sick.

### WAN State Transition Callbacks

Wehn WAN connectivity state changes, an appropriate on_wan_XXX callback is
called.

on_wan_down will powercycle the modem.

### Powercycling the modem

The plan is to power the modem using 
[Shelly Plug](https://shopusa.shelly.cloud/shelly-plug-us-wifi-smart-home-automation#393).
Use [the API](https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-overview)
to control the plug.


## Implementation

### Linting

While in src:

```
alex@latitude7490:~/Projects/wan-monitor/src$ mypy *.py
Success: no issues found in 8 source files
```

### Testing

While in src:

```
alex@latitude7490:~/Projects/wan-monitor/src$ python3 -m unittest *_test.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.607s

OK
```

### Runing

From command line:

```
alex@latitude7490:~/Projects/wan-monitor/src$ python3 monitor_modem.py 
0911.174616.329 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-11 17:46:16.327362, 3:39:34.862543
0911.174619.463 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-11 17:46:19.462165, 0:00:03.134803
0912.004740.386 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 00:47:40.386028, 7:01:20.923863
0912.004743.519 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 00:47:43.518302, 0:00:03.132274
0912.021340.598 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 02:13:40.596825, 1:25:57.078523
0912.021343.731 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 02:13:43.729680, 0:00:03.132855
0912.031310.265 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 03:13:10.264295, 0:59:26.534615
0912.031313.393 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 03:13:13.392260, 0:00:03.127965
0912.033344.158 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 03:33:44.156815, 0:20:30.764555
0912.033347.304 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 03:33:47.302874, 0:00:03.146059
0912.114825.724 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 11:48:25.717729, 8:14:38.414855
0912.114828.858 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 11:48:28.856590, 0:00:03.138861
0912.122631.794 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 12:26:31.792904, 0:38:02.936314
0912.122635.013 INFO MainThread cstatus.py:116 WAN still sick since 2021-09-12 12:26:31.792904
0912.122638.231 INFO MainThread cstatus.py:116 WAN still sick since 2021-09-12 12:26:31.792904
0912.122641.452 INFO MainThread monitor_modem.py:41 on_wan_down: 2021-09-12 12:26:41.450911, 0:00:09.658007
0912.123349.600 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 12:33:49.599953, 0:07:08.149042
0912.124242.341 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 12:42:42.339615, 0:08:52.739662
0912.124245.468 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 12:42:45.467315, 0:00:03.127700
0912.124817.178 INFO MainThread monitor_modem.py:34 on_wan_sick: 2021-09-12 12:48:17.175794, 0:05:31.708479
0912.124820.307 INFO MainThread monitor_modem.py:27 on_wan_upup: 2021-09-12 12:48:20.306712, 0:00:03.130918
```

## Status

This is a work in progress.  Monitoring part is pretty much done - see above.
Powercycling - not started.

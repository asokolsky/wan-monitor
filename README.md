# WAN Status Monitor and Modem Power Cycler

## Problem Statement

My cable modem occasionally looses connection to ISP. So, the plan is:

* monitor the wan connectivity status;
* if connection is lost - powercycle the modem.

## Design

Modem status is represented as JSON and is saved into a file.
Periodically:

* get WAN connectivity status by pinging WAN gateway;
* compare current status with the old one;
* act on changes.

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

When WAN connectivity state changes, an appropriate on_wan_XXX callback is
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
0915.133708.742 INFO monitoring wan_gw 73.93.94.1
0915.165045.308 INFO on_wan_sick: 2021-09-15 16:50:45.307255, 4:07:57.335309
0915.165048.460 INFO on_wan_upup: 2021-09-15 16:50:48.458745, 0:00:03.151490
0915.203056.721 INFO on_wan_sick: 2021-09-15 20:30:56.720621, 3:40:08.261876
0915.203059.854 INFO on_wan_upup: 2021-09-15 20:30:59.853079, 0:00:03.132458
0916.092051.158 INFO on_wan_sick: 2021-09-16 09:20:51.157001, 12:49:51.303922
0916.092054.283 INFO on_wan_upup: 2021-09-16 09:20:54.281880, 0:00:03.124879
0916.101057.222 INFO on_wan_sick: 2021-09-16 10:10:57.220087, 0:50:02.938207
0916.101100.388 INFO on_wan_upup: 2021-09-16 10:11:00.385276, 0:00:03.165189
0916.103713.134 INFO on_wan_sick: 2021-09-16 10:37:13.132174, 0:26:12.746898
0916.103716.263 INFO on_wan_upup: 2021-09-16 10:37:16.262169, 0:00:03.129995
0916.104807.565 INFO on_wan_sick: 2021-09-16 10:48:07.563828, 0:10:51.301659
0916.104810.704 INFO on_wan_upup: 2021-09-16 10:48:10.702869, 0:00:03.139041
0916.111435.465 INFO on_wan_sick: 2021-09-16 11:14:35.464516, 0:26:24.761647
0916.111438.609 INFO on_wan_upup: 2021-09-16 11:14:38.608475, 0:00:03.143959
0916.112244.853 INFO on_wan_sick: 2021-09-16 11:22:44.852089, 0:08:06.243614
0916.112247.980 INFO on_wan_upup: 2021-09-16 11:22:47.980116, 0:00:03.128027
0916.114316.323 INFO on_wan_sick: 2021-09-16 11:43:16.322291, 0:20:28.342175
0916.114319.474 INFO on_wan_upup: 2021-09-16 11:43:19.472985, 0:00:03.150694
0916.114322.694 INFO on_wan_sick: 2021-09-16 11:43:22.692764, 0:00:03.219779
0916.114325.914 INFO WAN still sick since 2021-09-16 11:43:22.692764
0916.114329.059 INFO on_wan_upup: 2021-09-16 11:43:29.057913, 0:00:06.365149
0916.114541.385 INFO on_wan_sick: 2021-09-16 11:45:41.384545, 0:02:12.326632
0916.114544.519 INFO on_wan_upup: 2021-09-16 11:45:44.518001, 0:00:03.133456
0916.114756.127 INFO on_wan_sick: 2021-09-16 11:47:56.116399, 0:02:11.598398
0916.114759.279 INFO on_wan_upup: 2021-09-16 11:47:59.278229, 0:00:03.161830
0916.114837.133 INFO on_wan_sick: 2021-09-16 11:48:37.132009, 0:00:37.853780
0916.114840.306 INFO on_wan_upup: 2021-09-16 11:48:40.305495, 0:00:03.173486
0916.115008.511 INFO on_wan_sick: 2021-09-16 11:50:08.509934, 0:01:28.204439
0916.115011.690 INFO on_wan_upup: 2021-09-16 11:50:11.689278, 0:00:03.179344
0916.115324.278 INFO on_wan_sick: 2021-09-16 11:53:24.275310, 0:03:12.586032
0916.115327.451 INFO on_wan_upup: 2021-09-16 11:53:27.449142, 0:00:03.173832
0916.115824.420 INFO on_wan_sick: 2021-09-16 11:58:24.418689, 0:04:56.969547
0916.115827.564 INFO on_wan_upup: 2021-09-16 11:58:27.563348, 0:00:03.144659
0916.115915.000 INFO on_wan_sick: 2021-09-16 11:59:14.999337, 0:00:47.435989
0916.115918.148 INFO on_wan_upup: 2021-09-16 11:59:18.147547, 0:00:03.148210
0916.120056.085 INFO on_wan_sick: 2021-09-16 12:00:56.084662, 0:01:37.937115
0916.120059.237 INFO on_wan_upup: 2021-09-16 12:00:59.235697, 0:00:03.151035
0916.121250.335 INFO on_wan_sick: 2021-09-16 12:12:50.334193, 0:11:51.098496
0916.121253.473 INFO on_wan_upup: 2021-09-16 12:12:53.473478, 0:00:03.139285
0916.121325.111 INFO on_wan_sick: 2021-09-16 12:13:25.110992, 0:00:31.637514
0916.121328.332 INFO WAN still sick since 2021-09-16 12:13:25.110992
0916.121331.468 INFO on_wan_upup: 2021-09-16 12:13:31.467580, 0:00:06.356588
0916.121720.952 INFO on_wan_sick: 2021-09-16 12:17:20.951367, 0:03:49.483787
0916.121724.093 INFO on_wan_upup: 2021-09-16 12:17:24.091850, 0:00:03.140483
0916.130037.145 INFO on_wan_sick: 2021-09-16 13:00:37.144522, 0:43:13.052672
0916.130040.359 INFO on_wan_upup: 2021-09-16 13:00:40.358024, 0:00:03.213502
0916.132606.474 INFO on_wan_sick: 2021-09-16 13:26:06.472818, 0:25:26.114794
0916.132609.610 INFO on_wan_upup: 2021-09-16 13:26:09.609190, 0:00:03.136372
0916.134634.286 INFO on_wan_sick: 2021-09-16 13:46:34.284868, 0:20:24.675678
0916.134637.420 INFO on_wan_upup: 2021-09-16 13:46:37.419148, 0:00:03.134280
0916.135638.761 INFO on_wan_sick: 2021-09-16 13:56:38.761343, 0:10:01.342195
0916.135641.897 INFO on_wan_upup: 2021-09-16 13:56:41.896020, 0:00:03.134677
0916.135645.117 INFO on_wan_sick: 2021-09-16 13:56:45.116330, 0:00:03.220310
0916.135648.250 INFO on_wan_upup: 2021-09-16 13:56:48.249397, 0:00:03.133067
0916.140444.276 INFO on_wan_sick: 2021-09-16 14:04:44.275005, 0:07:56.025608
0916.140447.468 INFO on_wan_upup: 2021-09-16 14:04:47.466797, 0:00:03.191792
0916.140450.677 INFO on_wan_sick: 2021-09-16 14:04:50.677572, 0:00:03.210775
0916.140453.811 INFO on_wan_upup: 2021-09-16 14:04:53.810933, 0:00:03.133361
0916.141044.568 INFO on_wan_sick: 2021-09-16 14:10:44.566922, 0:05:50.755989
0916.141047.757 INFO on_wan_upup: 2021-09-16 14:10:47.755655, 0:00:03.188733
0916.141809.452 INFO on_wan_sick: 2021-09-16 14:18:09.451527, 0:07:21.695872
0916.141812.584 INFO on_wan_upup: 2021-09-16 14:18:12.582738, 0:00:03.131211
0916.141818.936 INFO on_wan_sick: 2021-09-16 14:18:18.934849, 0:00:06.352111
0916.141822.064 INFO on_wan_upup: 2021-09-16 14:18:22.063224, 0:00:03.128375
0916.142549.995 INFO on_wan_sick: 2021-09-16 14:25:49.994120, 0:07:27.930896
0916.142553.133 INFO on_wan_upup: 2021-09-16 14:25:53.132204, 0:00:03.138084
0916.143128.310 INFO on_wan_sick: 2021-09-16 14:31:28.308885, 0:05:35.176681
0916.143131.531 INFO WAN still sick since 2021-09-16 14:31:28.308885
0916.143134.751 INFO WAN still sick since 2021-09-16 14:31:28.308885
0916.143137.975 WARNING on_wan_down: 2021-09-16 14:31:37.974260, 0:00:09.665375
0916.143820.597 INFO on_wan_upup: 2021-09-16 14:38:20.594026, 0:06:42.619766
0916.143852.073 INFO on_wan_sick: 2021-09-16 14:38:52.072711, 0:00:31.478685
0916.143855.100 INFO WAN still sick since 2021-09-16 14:38:52.072711
0916.143858.130 INFO WAN still sick since 2021-09-16 14:38:52.072711
0916.143901.155 WARNING on_wan_down: 2021-09-16 14:39:01.154017, 0:00:09.081306
0916.144108.017 INFO on_wan_upup: 2021-09-16 14:41:08.017043, 0:02:06.863026
```

## Status

This is a work in progress.  Monitoring part is pretty much done.
Powercycling - not started.

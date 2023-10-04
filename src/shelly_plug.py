#
# Wrapper for a shelly plug with API described here:
#  https://www.shelly-support.eu/forum/index.php?thread/775-collection-of-http-commands/&postID=7410#post7410
# Product:
#  https://www.shelly.cloud/en-us/products/product-overview/shelly-plus-plug-us
#
from collections.abc import Mapping, Sequence
# import ssl
import requests
from requests.exceptions import RequestException
from typing import Any, Dict, Optional, Tuple, Union

from logger import log


PrimitiveJSON = Union[str, int, float, bool, None]
# Not every instance of Mapping or Sequence can be fed to json.dump() but those
# two generic types are the most specific *immutable* super-types of `list`,
# `tuple` and `dict`:
AnyJSON4 = Union[Mapping[str, Any], Sequence[Any], PrimitiveJSON]
AnyJSON3 = Union[Mapping[str, AnyJSON4], Sequence[AnyJSON4], PrimitiveJSON]
AnyJSON2 = Union[Mapping[str, AnyJSON3], Sequence[AnyJSON3], PrimitiveJSON]
AnyJSON1 = Union[Mapping[str, AnyJSON2], Sequence[AnyJSON2], PrimitiveJSON]
AnyJSON = Union[Mapping[str, AnyJSON1], Sequence[AnyJSON1], PrimitiveJSON]
JSON = Mapping[str, AnyJSON]
# JSONs = Sequence[JSON]
# CompositeJSON = Union[JSON, Sequence[AnyJSON]]


class ShellyPlug:
    '''
    Commands for (US) Shelly Plug
    '''

    def __init__(s, ip: str) -> None:

        s.host = ip
        # TODO: validate ip?
        return

    def turn_on(s, duration: int = 0) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        Turn the plug on for duration seconds.
        If duration is 0, just turn it on.
        Returns ok, errmsg
        '''
        params = dict(turn='on')
        if duration:
            params['timer'] = str(duration)

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get('/relay/0', params)

    def turn_off(s, duration: int = 0) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        Turn the plug off for duration seconds.
        If duration is 0, just turn it off.
        Returns ok, errmsg
        '''
        params = dict(turn='off')
        if duration:
            params['timer'] = str(duration)

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get('/relay/0', params)

    def turn_toggle(s) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        Flip the switch.
        Returns ok, errmsg
        '''
        params = dict(turn='toggle')
        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get('/relay/0', params)

    def is_on(s) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        Get switch status
        Returns ok, errmsg, jdata
        '''
        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get('/relay/0')

    def get(s, uri: str, params: Dict[str, str] = {}) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        Issue HTTP GET to the plug's IP.
        Returns ok, errmsg, jdata
        '''

        assert isinstance(uri, str)
        url = f'http://{s.host}{uri}'
        errmsg = ''
        try:
            r = requests.get(url, params=params)
            if params:
                log.info('HTTP GET %s?%s => %s', url, params, r.status_code)
            else:
                log.info('HTTP GET %s => %s', url, r.status_code)
            if r.ok:
                jdata = r.json()
                log.info('r.json() => %s', jdata)

                return True, None, jdata

            errmsg = str(r)

        except ValueError as err:
            # failed to parse the response JSON
            errmsg = str(err)

        except RequestException as err:
            log.info('HTTP GET %s?%s =>\n%s', url, params, err)
            for arg in err.args:
                log.info('err.arg:\n%s', arg)
            # log.info('err.errno %s', err.errno)
            # log.info('err.filename %s', err.filename)
            # log.info('err.filename2 %s', err.filename2)
            # log.info('err.response %s', err.response)
            # log.info('err.strerror %s', err.strerror)

            errmsg = str(err)

        return False, errmsg, None

    def rpc(s, method: str, params: Dict[str, Any] = {}) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        gen2 API
        see https://shelly-api-docs.shelly.cloud/gen2/Overview/RPCProtocol
        '''

        assert isinstance(method, str)
        assert method

        # prepare params
        assert isinstance(params, dict)

        url = f'http://{s.host}/rpc/'
        request_frame = dict(id=123, src='123456', method=method)
        if params:
            request_frame['params'] = params
        errmsg = ''
        try:
            r = requests.post(url, json=request_frame)
            log.info(
                'HTTP POST %s?%s => %s',
                url, request_frame, r.status_code)
            if r.ok:
                jdata = r.json()
                log.info('r.json() => %s', jdata)
                assert jdata['id'] == request_frame['id']
                assert jdata['src']  # e.g. 'shellyplugus-083af2005bf0'
                assert jdata['dst'] == request_frame['src']
                if 'error' in jdata:
                    err = jdata['error']
                    assert 'code' in err
                    assert 'message' in err
                    return False, None, err['message']

                assert 'result' in jdata
                return True, None, jdata

            errmsg = str(r)

        except ValueError as err:
            # failed to parse the response JSON
            errmsg = str(err)

        except RequestException as err:
            log.info('HTTP GET %s?%s =>\n%s', url, params, err)
            for arg in err.args:
                log.info('err.arg:\n%s', arg)
            # log.info('err.errno %s', err.errno)
            # log.info('err.filename %s', err.filename)
            # log.info('err.filename2 %s', err.filename2)
            # log.info('err.response %s', err.response)
            # log.info('err.strerror %s', err.strerror)

            errmsg = str(err)

        return False, errmsg, None

    def get_status(s) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetstatus
        {
            "ble": {},
            "cloud": {
                "connected": false
            },
            "mqtt": {
                "connected": false
            },
            "switch:0": {
                "id": 0,
                "source": "button",
                "output": true,
                "apower": 53.2,
                "voltage": 122.1,
                "current": 0.698,
                "aenergy": {
                    "total": 17.295,
                    "by_minute": [
                        266.491,
                        877.535,
                        349.815
                   ],
                    "minute_ts": 1666400177
                },
                "temperature": {
                    "tC": 50.0,
                    "tF": 122.0
                }
            },
            "sys": {
                "mac": "083AF2005BF0",
                "restart_required": false,
                "time": "17:56",
                "unixtime": 1666400180,
                "uptime": 6296,
                "ram_size": 249024,
                "ram_free": 174772,
                "fs_size": 458752,
                "fs_free": 225280,
                "cfg_rev": 5,
                "available_updates": {
                    "beta": {
                        "version": "0.11.4-beta1"
                    },
                    "stable": {
                        "version": "0.11.3"
                    }
                }
            },
            "wifi": {
                "sta_ip": "192.168.10.190",
                "status": "got ip",
                "ssid": "960",
                "rssi": -43
            }
        }
        '''
        ok, errmsg, jdata = s.rpc('Shelly.GetStatus')
        if ok:
            assert jdata
            jdata = jdata['result']
        return ok, errmsg, jdata

    def get_config(s) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetconfig
        => {
            "ble": {
                "enable": false
            },
            "cloud": {
                "enable": false,
                "server": "iot.shelly.cloud:6012/jrpc"
            },
            "mqtt": {
                "enable": false,
                "server": null,
                "user": null,
                "pass": null,
                "topic_prefix": "shellyplugus-083af2005bf0",
                "rpc_ntf": true,
                "status_ntf": false
            },
            "switch:0": {
                "id": 0,
                "name": null,
                "initial_state": "off",
                "auto_on": false,
                "auto_on_delay": 60.0,
                "auto_off": false,
                "auto_off_delay": 60.0,
                "power_limit": null,
                "voltage_limit": 280,
                "current_limit": 16.0
            },
            "sys": {
                "device": {
                    "name": null,
                    "mac": "083AF2005BF0",
                    "fw_id": "20220211-132652/plugusprod2_app-gcb4621f",
                    "eco_mode": false
                },
                "location": {
                    "tz": "America/Los_Angeles",
                    "lat": 37.19209,
                    "lon": -122.11168
                },
                "debug": {
                    "mqtt": {
                        "enable": false
                    },
                    "websocket": {
                        "enable": false
                    },
                    "udp": {
                        "addr": null
                    }
                },
                "ui_data": {
                    "consumption_types": [
                        "lights"
                   ]
                },
                "rpc_udp": {
                    "dst_addr": null,
                    "listen_port": null
                },
                "sntp": {
                    "server": "time.google.com"
                },
                "cfg_rev": 5
            },
            "wifi": {
                "ap": {
                    "ssid": "ShellyPlugUS-083AF2005BF0",
                    "is_open": true,
                    "enable": false
                },
                "sta": {
                    "ssid": "960",
                    "is_open": false,
                    "enable": true,
                    "ipv4mode": "dhcp",
                    "ip": null,
                    "netmask": null,
                    "gw": null,
                    "nameserver": null
                },
                "sta1": {
                    "ssid": null,
                    "is_open": true,
                    "enable": false,
                    "ipv4mode": "dhcp",
                    "ip": null,
                    "netmask": null,
                    "gw": null,
                    "nameserver": null
                },
                "roam": {
                    "rssi_thr": -80,
                    "interval": 60
                }
            }
        }
        '''
        ok, errmsg, jdata = s.rpc('Shelly.GetConfig')
        if ok:
            jdata = jdata['result']
        return ok, errmsg, jdata

    def get_device_info(s) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetdeviceinfo
        {
            "name": null,
            "id": "shellyplugus-083af2005bf0",
            "mac": "083AF2005BF0",
            "model": "SNPL-00116US",
            "gen": 2,
            "fw_id": "20220211-132652/plugusprod2_app-gcb4621f",
            "ver": "plugusprod2",
            "app": "PlugUS",
            "auth_en": false,
            "auth_domain": null
        }
        '''
        ok, errmsg, jdata = s.rpc('Shelly.GetDeviceInfo')
        if ok:
            jdata = jdata['result']
        return ok, errmsg, jdata

    def list_methods(s) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellylistmethods
        jdata => {
            "methods": [
                "Switch.SetConfig",
                "Switch.GetConfig",
                "Switch.GetStatus",
                "Switch.Toggle",
                "Switch.Set",
                "Schedule.List",
                "Schedule.DeleteAll",
                "Schedule.Delete",
                "Schedule.Update",
                "Schedule.Create",
                "Input.SetConfig",
                "Input.GetConfig",
                "Input.GetStatus",
                "Webhook.ListSupported",
                "Webhook.List",
                "Webhook.DeleteAll",
                "Webhook.Delete",
                "Webhook.Update",
                "Webhook.Create",
                "Script.Stop",
                "Script.Start",
                "Script.Eval",
                "Script.GetCode",
                "Script.PutCode",
                "Script.SetConfig",
                "Script.GetConfig",
                "Script.GetStatus",
                "Script.List",
                "Script.Delete",
                "Script.Create",
                "Mqtt.SetConfig",
                "Mqtt.GetConfig",
                "Mqtt.GetStatus",
                "Cloud.SetConfig",
                "Cloud.GetConfig",
                "Cloud.GetStatus",
                "BLE.SetConfig",
                "BLE.GetConfig",
                "BLE.GetStatus",
                "Wifi.Scan",
                "Wifi.SetConfig",
                "Wifi.GetConfig",
                "Wifi.GetStatus",
                "Sys.SetConfig",
                "Sys.GetConfig",
                "Sys.GetStatus",
                "HTTP.POST",
                "HTTP.GET",
                "Shelly.ListMethods",
                "Shelly.PutUserCA",
                "Shelly.Reboot",
                "Shelly.SetAuth",
                "Shelly.Update",
                "Shelly.CheckForUpdate",
                "Shelly.DetectLocation",
                "Shelly.ListTimezones",
                "Shelly.GetStatus",
                "Shelly.FactoryReset",
                "Shelly.ResetWiFiConfig",
                "Shelly.GetConfig",
                "Shelly.GetDeviceInfo"
           ]
        }
        '''
        ok, errmsg, jdata = s.rpc('Shelly.ListMethods')
        if ok:
            assert jdata
            jdata = jdata['result']
        return ok, errmsg, jdata

    def get_input_config(s, id:int=0) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Input
        '''
        ok, errmsg, jdata = s.rpc('Input.GetConfig', {'id': id})
        if ok:
            jdata = jdata['result']
        return ok, errmsg, jdata

    def get_input_status(s, id: int = 0) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Input
        '''
        ok, errmsg, jdata = s.rpc('Input.GetStatus', {'id': id})
        if ok:
            jdata = jdata['result']
        return ok, errmsg, jdata

    def get_switch_config(s, id: int = 0) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Switch
        => {
            "id": 0,
            "name": null,
            "initial_state": "off",
            "auto_on": false,
            "auto_on_delay": 60.0,
            "auto_off": false,
            "auto_off_delay": 60.0,
            "power_limit": null,
            "voltage_limit": 280,
            "current_limit": 16.0
        }
        '''
        ok, errmsg, jdata = s.rpc('Switch.GetConfig', {'id': id})
        if ok:
            jdata = jdata['result']
        return ok, errmsg, jdata

    def get_switch_status(s, id: int = 0) -> Tuple[
            bool, Optional[str], Optional[JSON]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Switch

        jdata: {
            "id": 0,
            "source": "button",
            "output": true,
            "apower": 48.4,
            "voltage": 121.5,
            "current": 0.639,
            "aenergy": {
                "total": 16.005,
                "by_minute": [
                    203.553,
                    0.0,
                    0.0
               ],
                "minute_ts": 1666400087
            },
            "temperature": {
                "tC": 49.4,
                "tF": 120.9
            }
        }
        '''
        ok, errmsg, jdata = s.rpc('Switch.GetStatus', {'id': id})
        if ok:
            assert jdata
            jdata = jdata['result']
        return ok, errmsg, jdata

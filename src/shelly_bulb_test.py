#
#
#
import json
# from typing import List
import unittest

from shelly import ShellyBulb
from logger import log


class ShellyBulb_test(unittest.TestCase):
    '''
    class ShellyBulb test cases

    to run all these:
    `python3 -m unittest shelly_plug_test.py`

    to run just one:
    python3 -m unittest shelly_plug_test.ShellyPlug_test.test_nonexistent_plug
    '''

    # IP Address of your shelly plug
    ip = '192.168.11.88'

    def test_nonexistent_bulb(s) -> None:
        '''
        Test behavior of misconfigured object
        '''
        log.info('test_nonexistent_plug')

        badIP = '192.168.11.126'
        bulb = ShellyBulb(badIP)
        ok, errmsg, jdata = bulb.turn_on()
        s.assertFalse(ok, errmsg)
        return

    def test_gen1api(s) -> None:
        '''
        Test Gen1 API support
        '''
        log.info('test_gen1api')

        bulb = ShellyBulb(s.ip)

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly
        log.info('test_gen1api /shelly')
        ok, errmsg, jdata = bulb.get('/shelly')
        s.assertTrue(ok, errmsg)
        log.info('get(/shelly)=> %s', json.dumps(jdata, indent=4))
        # {
        #    "type": "SHBDUO-1",
        #    "mac": "98F4ABD12B55",
        #    "auth": false,
        #    "fw": "20191216-140245/???",
        #    "num_outputs": 1
        # }
        expected_fields = ('type', 'mac', 'auth', 'fw', 'num_outputs')
        for f in expected_fields:
            s.assertIn(f, jdata)
        s.assertEqual(jdata["type"], "SHBDUO-1")

        ok, errmsg, jdata = bulb.get_status()
        s.assertTrue(ok, errmsg)
        log.info('get(/status)=> %s', json.dumps(jdata, indent=4))
        expected_fields = (
            "wifi_sta", "cloud", "mqtt", "time", "serial", "has_update", "mac",
            "lights", "meters", "update", "ram_total", "ram_free", "fs_size",
            "fs_free", "uptime"
        )
        for f in expected_fields:
            s.assertIn(f, jdata)

        ok, errmsg, jdata = bulb.get_settings()
        s.assertTrue(ok, errmsg)
        log.info('get(/settings)=> %s', json.dumps(jdata, indent=4))
        expected_fields = (
            'device', 'wifi_ap', 'wifi_sta', 'wifi_sta1', 'mqtt', 'sntp',
            'login', 'pin_code', 'name', 'fw', 'build_info', 'cloud',
            'timezone', "lat", "lng", "tzautodetect", "tz_utc_offset",
            "tz_dst", "tz_dst_auto", "time", "hwinfo", "mode", "transition",
            "lights", "night_mode"
        )
        for f in expected_fields:
            s.assertIn(f, jdata)

        ok, errmsg, jdata = bulb.is_on()
        s.assertTrue(ok, errmsg)
        log.info('get(/light/0)=> %s', json.dumps(jdata, indent=4))
        expected_fields2 = ("ison", "brightness", "white", "temp")
        for f in expected_fields2:
            s.assertIn(f, jdata)
        was_on = jdata['ison']
        if jdata['ison']:
            ok, errmsg, jdata = bulb.turn_off(0)
            log.info('bulb.turn_off() => %s', json.dumps(jdata, indent=4))
            ok, errmsg, jdata = bulb.is_on()
            s.assertTrue(ok, errmsg)
            s.assertFalse(jdata['ison'], 'Failed to turn bulb off')

        ok, errmsg, jdata = bulb.is_on()
        s.assertTrue(ok, errmsg)
        log.info('get(/light/0)=> %s', json.dumps(jdata, indent=4))
        s.assertFalse(jdata['ison'], 'Failed to meet expectations')

        ok, errmsg, jdata = bulb.turn_on(0)
        s.assertTrue(ok, errmsg)
        assert jdata
        for f in expected_fields2:
            s.assertIn(f, jdata)
        ok, errmsg, jdata = bulb.is_on()
        s.assertTrue(ok, errmsg)
        s.assertTrue(jdata['ison'], 'Failed to turn bulb on')

        ok, errmsg, jdata = bulb.turn_toggle(0)
        s.assertTrue(ok, errmsg)
        assert jdata
        for f in expected_fields2:
            s.assertIn(f, jdata)

        ok, errmsg, jdata = bulb.is_on()
        s.assertTrue(ok, errmsg)
        if not jdata['ison']:
            ok, errmsg, jdata = bulb.turn_on()
            s.assertTrue(ok, errmsg)

        return

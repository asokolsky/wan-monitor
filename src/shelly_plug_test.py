#
#
#
import json
# from typing import List
import unittest

from shelly import ShellyPlug
from logger import log


class ShellyPlug_test(unittest.TestCase):
    '''
    class ShellyPlug test cases

    to run all these:
    `python3 -m unittest shelly_plug_test.py`

    to run just one:
    `python3 -m unittest shelly_plug_test.ShellyPlug_test.test_nonexistent_plug`
    '''

    # IP Address of your shelly plug
    ip = '192.168.11.86'

    def test_nonexistent_plug(s) -> None:
        '''
        Test behavior of misconfigured object
        '''
        log.info('test_nonexistent_plug')

        badIP = '192.168.10.126'
        plug = ShellyPlug(badIP)
        ok, errmsg, jdata = plug.turn_on()
        s.assertFalse(ok, errmsg)
        return

    def test_gen1api(s) -> None:
        '''
        Test Gen1 API support
        '''
        log.info('test_gen1api')

        plug = ShellyPlug(s.ip)

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly
        log.info('test_gen1api /shelly')
        ok, errmsg, jdata = plug.get('/shelly')
        log.info('get(/shelly)=> %s', json.dumps(jdata, indent=4))
        # {
        #     "name": null,
        #     "id": "shellyplugus-083af2005bf0",
        #     "mac": "083AF2005BF0",
        #     "slot": 1,
        #     "model": "SNPL-00116US",
        #     "gen": 2,
        #     "fw_id": "20231219-133953/1.1.0-g34b5d4f",
        #     "ver": "1.1.0",
        #     "app": "PlugUS",
        #     "auth_en": false,
        #     "auth_domain": null
        # }
        s.assertTrue(ok, errmsg)
        assert jdata
        # these are the fields I find in my gen2 device
        expected_fields1 = (
            'name', 'id', 'mac', 'model', 'gen', 'fw_id', 'ver', 'app',
            'auth_en', 'auth_domain')
        for f in expected_fields1:
            s.assertIn(f, jdata)

        log.info('test_gen1api /settings')
        ok, errmsg, jdata = plug.get('/settings')
        s.assertFalse(ok, errmsg)

        log.info('test_gen1api /status')
        ok, errmsg, jdata = plug.get('/status')
        s.assertFalse(ok, errmsg)

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        log.info('test_gen1api /relay/0')
        ok, errmsg, jdata = plug.get('/relay/0')
        s.assertTrue(ok, errmsg)
        assert jdata
        expected_fields2 = (
            'ison', 'has_timer', 'timer_started_at', 'timer_duration',
            'timer_remaining', 'overpower', 'source')
        for f in expected_fields2:
            s.assertIn(f, jdata)

        if jdata['ison']:
            ok, errmsg, jdata = plug.turn_off()
            s.assertTrue(ok, errmsg)

        ok, errmsg, jdata = plug.turn_on()
        s.assertTrue(ok, errmsg)
        assert jdata
        for f in expected_fields2:
            s.assertIn(f, jdata)
        s.assertTrue(jdata['ison'])

        ok, errmsg, jdata = plug.turn_off()
        s.assertTrue(ok, errmsg)
        assert jdata
        for f in expected_fields2:
            s.assertIn(f, jdata)
        s.assertFalse(jdata['ison'])

        ok, errmsg, jdata = plug.is_on()
        s.assertTrue(ok, errmsg)
        assert jdata
        was_on = jdata['ison']

        ok, errmsg, jdata = plug.turn_toggle()
        s.assertTrue(ok, errmsg)
        assert jdata
        for f in expected_fields2:
            s.assertIn(f, jdata)
        s.assertTrue(jdata['ison'])
        is_on = jdata['ison']
        s.assertNotEqual(was_on, is_on)

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-meter-0
        log.info('test_gen1api /meter/0')
        ok, errmsg, jdata = plug.get('/meter/0')
        s.assertFalse(ok, errmsg)
        return

    def test_gen2api(s) -> None:
        '''
        Test Gen2 API support
        '''
        log.info('test_gen2api')

        plug = ShellyPlug(s.ip)

        # https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetstatus
        log.info('test_gen2api Shelly.GetStatus')
        ok, errmsg, jdata = plug.rpc('Shelly.GetStatus')
        s.assertTrue(ok, errmsg)
        assert jdata
        expected_fields = ('id', 'src', 'dst', 'result')
        for f in expected_fields:
            s.assertIn(f, jdata)
        result = jdata['result']

        ok, errmsg, jdata = plug.get_status()
        s.assertTrue(ok, errmsg)
        assert jdata
        log.info('plug.get_status() => %s', json.dumps(jdata, indent=4))
        s.assertEqual(len(result), len(jdata))

        expected_fields = ('ble', 'cloud', 'mqtt', 'switch:0', 'sys', 'wifi')
        for f in expected_fields:
            s.assertIn(f, jdata)

        data = result['switch:0']
        expected_fields = (
            'id', 'source', 'output', 'apower', 'voltage',
            'current', 'aenergy', 'temperature')
        for f in expected_fields:
            s.assertIn(f, data)

        ok, errmsg, jdata = plug.get_config()
        s.assertTrue(ok, errmsg)
        assert jdata
        log.info('plug.get_config() => %s', json.dumps(jdata, indent=4))

        expected_fields = ('ble', 'cloud', 'mqtt', 'switch:0', 'sys', 'wifi')
        for f in expected_fields:
            s.assertIn(f, jdata)

        ok, errmsg, jdata = plug.get_device_info()
        s.assertTrue(ok, errmsg)
        assert jdata
        log.info('plug.get_device_info() => %s', json.dumps(jdata, indent=4))

        expected_fields = (
            'name', 'id', 'mac', 'model', 'gen', 'fw_id', 'ver',
            'app', 'auth_en', 'auth_domain')
        for f in expected_fields:
            s.assertIn(f, jdata)

        ok, errmsg, jdata = plug.list_methods()
        s.assertTrue(ok, errmsg)
        assert jdata
        log.info('plug.list_methods() => %s', json.dumps(jdata, indent=4))
        s.assertIn('methods', jdata)

        ok, errmsg, jdata = plug.get_input_config()
        log.info('plug.get_input_config() => %s, %s, %s', ok, errmsg, jdata)
        # s.assertTrue(ok, errmsg)
        # ok, errmsg, jdata = plug.get('/rpc/Input.GetConfig', {'id':0})
        # s.assertTrue(ok, errmsg)

        ok, errmsg, jdata = plug.get_input_status()
        log.info('plug.get_input_status() => %s, %s, %s', ok, errmsg, jdata)

        ok, errmsg, jdata = plug.get_switch_config()
        s.assertTrue(ok, errmsg)
        assert jdata
        log.info('plug.get_switch_config() => %s', json.dumps(jdata, indent=4))

        expected_fields = (
            'id', 'name', 'initial_state', 'auto_on',
            'auto_on_delay', 'auto_off', 'auto_off_delay', 'power_limit',
            'voltage_limit', 'current_limit')
        for f in expected_fields:
            s.assertIn(f, jdata)

        ok, errmsg, jdata = plug.get_switch_status()
        s.assertTrue(ok, errmsg)
        assert jdata
        log.info('plug.get_switch_status() => %s', json.dumps(jdata, indent=4))

        expected_fields = (
            'id', 'source', 'output', 'apower', 'voltage',
            'current', 'aenergy', 'temperature')
        for f in expected_fields:
            s.assertIn(f, jdata)
        return

#
#
#

from typing import List
import unittest

from shelly_plug import ShellyPlug


class ShellyPlug_test( unittest.TestCase ):
    '''
    class ShellyPlug test cases
    '''

    def test_nonexistent_plug( s ) -> None:

        badIP = '192.168.100.1'
        badIP = '192.168.10.126'
        plug = ShellyPlug( badIP )
        ok, errmsg, jdata = plug.turn_on()
        s.assertFalse( ok, errmsg )

        return

    def test_gen1api( s ) -> None:

        ip = '192.168.10.190'
        plug = ShellyPlug( ip )

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly
        ok, errmsg, jdata = plug.get('/shelly')
        s.assertTrue( ok, errmsg )

        # these are the fields I find in my gen2 device
        expected_fields = (
            'name', 'id', 'mac', 'model', 'gen', 'fw_id', 'ver', 'app',
            'auth_en', 'auth_domain')
        for f in expected_fields:
            s.assertIn( f, jdata )

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        ok, errmsg, jdata = plug.get('/relay/0')
        s.assertTrue( ok, errmsg )
        expected_fields = (
            'ison', 'has_timer', 'timer_started_at', 'timer_duration',
            'timer_remaining', 'overpower', 'source')
        for f in expected_fields:
            s.assertIn( f, jdata )

        if jdata['ison']:
            ok, errmsg, jdata = plug.turn_off()
            s.assertTrue( ok, errmsg )


        ok, errmsg, jdata = plug.turn_on()
        s.assertTrue( ok, errmsg )
        for f in expected_fields:
            s.assertIn( f, jdata )
        s.assertTrue( jdata['ison'] )

        ok, errmsg, jdata = plug.turn_off()
        s.assertTrue( ok, errmsg )
        for f in expected_fields:
            s.assertIn( f, jdata )
        s.assertFalse( jdata['ison'] )


        ok, errmsg, jdata = plug.is_on()
        s.assertTrue( ok, errmsg )
        was_on = jdata['ison']

        ok, errmsg, jdata = plug.turn_toggle()
        s.assertTrue( ok, errmsg )
        for f in expected_fields:
            s.assertIn( f, jdata )
        s.assertTrue( jdata['ison'] )
        is_on = jdata['ison']
        s.assertNotEqual( was_on, is_on )


        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-meter-0
        ok, errmsg, jdata = plug.get('/meter/0')
        s.assertFalse( ok, errmsg )

        return

    def test_gen2api( s ) -> None:

        ip = '192.168.10.190'
        plug = ShellyPlug( ip )

        # https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetstatus
        ok, errmsg, jdata = plug.rpc( 'Shelly.GetStatus' )
        s.assertTrue( ok, errmsg )
        expected_fields = ('id', 'src', 'dst', 'result')
        for f in expected_fields:
            s.assertIn( f, jdata )
        result = jdata['result']

        ok, errmsg, jdata = plug.get_status()
        s.assertTrue( ok, errmsg )
        s.assertEqual( len(result), len(jdata) )

        expected_fields = ( 'ble', 'cloud', 'mqtt', 'switch:0', 'sys', 'wifi')
        for f in expected_fields:
            s.assertIn( f, jdata )

        data = result[ 'switch:0' ]
        expected_fields = ( 'id', 'source', 'output', 'apower', 'voltage',
            'current', 'aenergy', 'temperature')
        for f in expected_fields:
            s.assertIn( f, data )

        ok, errmsg, jdata = plug.get_config()
        s.assertTrue( ok, errmsg )
        expected_fields = ( 'ble', 'cloud', 'mqtt', 'switch:0', 'sys', 'wifi')
        for f in expected_fields:
            s.assertIn( f, jdata )

        ok, errmsg, jdata = plug.get_device_info()
        s.assertTrue( ok, errmsg )
        expected_fields = ( 'name', 'id', 'mac', 'model', 'gen', 'fw_id', 'ver',
            'app', 'auth_en', 'auth_domain' )
        for f in expected_fields:
            s.assertIn( f, jdata )

        ok, errmsg, jdata = plug.list_methods()
        s.assertTrue( ok, errmsg )
        s.assertIn( 'methods', jdata )

        ok, errmsg, jdata = plug.get_input_config()
        #s.assertTrue( ok, errmsg )
        #ok, errmsg, jdata = plug.get('/rpc/Input.GetConfig', {'id':0})
        #s.assertTrue( ok, errmsg )

        ok, errmsg, jdata = plug.get_input_status()

        ok, errmsg, jdata = plug.get_switch_config()
        s.assertTrue( ok, errmsg )
        expected_fields = ('id', 'name', 'initial_state', 'auto_on',
            'auto_on_delay', 'auto_off', 'auto_off_delay', 'power_limit',
            'voltage_limit', 'current_limit' )
        for f in expected_fields:
            s.assertIn( f, jdata )

        ok, errmsg, jdata = plug.get_switch_status()
        s.assertTrue( ok, errmsg )
        expected_fields = ( 'id', 'source', 'output', 'apower', 'voltage',
        'current', 'aenergy', 'temperature' )
        for f in expected_fields:
            s.assertIn( f, jdata )
        return

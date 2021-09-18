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
        ok, errmsg = plug.turn_on()
        s.assertFalse( ok, errmsg )

        return
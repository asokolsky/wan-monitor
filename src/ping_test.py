#
# 
#

from typing import List
import unittest

from ping import ping
from logger import log

badip = '192.168.0.1'
lan_gw = '192.168.10.1'
wan_gw = '192.168.10.1'
modem_ip = '192.168.100.10'

class ping_test( unittest.TestCase ):
    '''
    function ping test cases
    '''

    def test_good_ping( s ):

        res = ping( badip )
        log.debug( 'ping( %s ) => %s', badip, res )
        s.assertFalse( res, 'Failed to NOT ping ' + badip )

        res = ping( lan_gw )
        log.debug( 'ping( %s ) => %s', lan_gw, res )
        s.assertTrue( res, 'Failed to ping ' + lan_gw )

        res = ping( wan_gw )
        log.debug( 'ping( %s ) => %s', wan_gw, res )
        s.assertTrue( res, 'Failed to ping ' + wan_gw )
                
        return

if __name__ == '__main__':
    unittest.main()

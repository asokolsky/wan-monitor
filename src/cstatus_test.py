#

import unittest

from cstatus import ConnectivityStatus
from logger import log

lan_gw = '192.168.10.1'
wan_gw = '192.168.100.1'
modem_ip = '192.168.100.10'
modem_status_path = '/tmp/modem_status.json'

class ConnectivityStatus_test( unittest.TestCase ):
    '''
    class ConnectivityStatus test cases
    '''

    def test_connectivity_status(s) -> None:
        stat = ConnectivityStatus( lan_gw, wan_gw, modem_ip )
        stat.update()
        log.debug( 'stat:%s', stat )

        bad_path = '/tmp/fff/modem_status.json'
        assert not stat.to_file( bad_path )

        assert stat.to_file( modem_status_path )

        stat1 = ConnectivityStatus( lan_gw, wan_gw, modem_ip )
        assert not stat1.from_file( bad_path )

        assert stat1.from_file( modem_status_path )
        log.debug( 'stat1:%s', stat1 )

        assert stat == stat1

        stat1.update()
        log.debug( 'stat1:%s', stat1 )

        return

if __name__ == '__main__':
    unittest.main()

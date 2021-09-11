#
#
#

from datetime import datetime, timedelta
from enum import Enum
from json_serializable import JsonSerializable
from ping import ping
from typing import Optional, Tuple, Union

from logger import log

class ConnectivityState( str, Enum ):
    '''
    String enum to represent state.
    '''
    none=''
    up='up'
    down='down'
    sick='sick'

    @classmethod
    def is_valid( cls, st: Union[ str, 'ConnectivityState' ] ) -> bool:
        return st in cls._value2member_map_

    def __repr__( s ):
        'Enable serialization as a string'
        return repr( s.value )

    def __str__( s ):
        'Enable serialization as a string'
        return s.value


def str2datetime( tstamp:str ) -> datetime:
    assert tstamp
    tformat = '%Y-%m-%d %H:%M:%S.%f'
    return datetime.strptime( tstamp, tformat )

class ConnectivityStatus( JsonSerializable ):
    '''
    Representation of LAN connectivity.
    '''
    # wan gw ping failure for this long === wan considered down
    wan_timeout_down = timedelta( seconds=9 )

    def __init__( s, lan_gw:str='', wan_gw:str='', modem_ip:str='', path:str='' ):
        s.lan_gw = lan_gw
        s.wan_gw = wan_gw
        s.modem_ip = modem_ip
        s.lan_gw_rtt = ''
        s.wan_gw_rtt = ''
        s.modem_ip_rtt = ''
        s.last_state_change = ''            # set in update_state
        s.state = ConnectivityState.none

        if path:
            s.from_file( path )
        else:
            s.update()
        return

    def loaded( s ) -> bool:
        '''
        To verify that __init__(path='/foo/bar' ) succeded
        '''
        return s.lan_gw != '' # and s.wan_gw


    def update( s ):
        '''
        Do actual communication with the world
        '''
        s.lan_gw_rtt = ping( s.lan_gw )
        s.modem_ip_rtt = ping( s.modem_ip )
        s.wan_gw_rtt = ping( s.wan_gw )
        #s.wan_gw_rtt = s.get_from_file( '/tmp/wan_gw_rtt.txt' )

        # state machine transition is done in update_state
        return

    def update_state( s, old:'ConnectivityStatus' ) -> Tuple[
            ConnectivityState, ConnectivityState, datetime, timedelta ]:
        '''
        Given an old ConnectivityStatus update current state.
        Returns old, new states
        '''

        n = datetime.now()
        s.last_state_change = old.last_state_change
        if not s.last_state_change:
            s.last_state_change = str(n)
        o = str2datetime( s.last_state_change )

        if s.wan_gw_rtt:
            s.state = ConnectivityState.up
            if old.wan_gw_rtt:
                log.debug( 'LAN:%9s, WAN:%9s, up since %s',
                    s.lan_gw_rtt, s.wan_gw_rtt, s.last_state_change )
            else:
                s.last_state_change = str(n)
                log.debug( 'WAN going up on %s', s.last_state_change )
        
        elif old.wan_gw_rtt:
            s.state = ConnectivityState.sick
            s.last_state_change = str(n)
            log.debug( 'WAN going sick on %s', s.last_state_change )

        elif old.state == ConnectivityState.down:
            s.state = ConnectivityState.down
            log.debug( 'WAN still down since %s', s.last_state_change )

        elif n < o + s.wan_timeout_down:
            s.state = ConnectivityState.sick
            log.info( 'WAN still sick since %s', s.last_state_change )
        
        else:
            s.state = ConnectivityState.down
            s.last_state_change = str(n)
            log.debug( 'WAN going down on %s', s.last_state_change )

        if old.state != s.state:
            delta = n-o
        else:
            delta = timedelta( seconds=0 )

        return old.state, s.state, n, delta

    def get_from_file( s, path ) -> str:
        with open( path ) as fp:
            for line in fp:
                return line.strip()
        return ''

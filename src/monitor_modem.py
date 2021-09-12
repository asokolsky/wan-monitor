#
# Monitor Modem Status and Act on Its Changes
#

lan_gw = '192.168.10.1'
wan_gw = '73.93.94.1'

#lan_gw = '192.168.1.1'
#wan_gw = '73.15.24.1'

modem_ip = '192.168.100.10'
modem_status_path = '/tmp/modem_status.json'

# no more customization below

from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional

from logger import log
from cstatus import ConnectivityState, ConnectivityStatus

def on_wan_up( now:datetime, downtime:timedelta ) -> None:
    '''
    Wan is available.  Again!
    '''
    log.info( 'on_wan_upup: %s, %s', now, downtime )
    return

def on_wan_sick( now:datetime, uptime:timedelta ) -> None:
    '''
    Wan goes sick.  It can get better soon.  Or not.
    '''
    log.info( 'on_wan_sick: %s, %s', now, uptime )
    return

def on_wan_down( now:datetime, sicktime:timedelta ) -> None:
    '''
    Wan goes down!  Do something about it!
    '''
    log.info( 'on_wan_down: %s, %s', now, sicktime )
    return

def monitor_modem_tick() -> None:
    '''
    This can be called from a loop or cron
    '''
    old = ConnectivityStatus( path=modem_status_path )
    now = ConnectivityStatus( lan_gw, wan_gw, modem_ip )
        
    if not old.loaded():
        now.to_file( modem_status_path )
        return
    #
    # compare old and new and act on changes
    #
    if not now.lan_gw_rtt:
        log.info( 'LAN inaccessible' )
        return

    ostate, nstate, n, delta = now.update_state( old )
    now.to_file( modem_status_path )

    if ostate == nstate:
        pass

    elif nstate == ConnectivityState.up:
        log.debug( 'wan going up on %s', now.last_state_change )
        on_wan_up( n, delta )

    elif nstate == ConnectivityState.sick:
        log.debug( 'wan going sick on %s', now.last_state_change )
        on_wan_sick( n, delta )

    elif nstate == ConnectivityState.down:
        log.debug( 'wan going down on %s', now.last_state_change )
        on_wan_down( n, delta )

    else:
        log.error( 'unhandled transition from %s to %s', ostate, nstate )

    return

def test_loop() -> None:
    try:
        while True:
            monitor_modem_tick()
            time.sleep( 3 )

    except KeyboardInterrupt:
        print( 'Exiting' )
    return

if __name__ == '__main__':
    test_loop()

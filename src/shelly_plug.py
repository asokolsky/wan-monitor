#
#  Wrapper for a shelly plug
#  https://www.shelly-support.eu/forum/index.php?thread/775-collection-of-http-commands/&postID=7410#post7410
#
import requests
from requests.exceptions import RequestException

from typing import Dict, Optional, Tuple

from logger import log

class ShellyPlug:
    '''
    Commands for Shelly Plug
    https://shopusa.shelly.cloud/shelly-plug-us-wifi-smart-home-automation#393
    '''

    def __init__(s, ip:str ) -> None:

        s.url = f'http://{ip}/relay/0'

        # TODO: validate ip?
        return

    def turn_on( s, duration:int = 0 ) -> Tuple[ bool, Optional[str]]:
        '''
        Turn the plug on for duration seconds.  If duration is 0, just turn it on.
        Returns ok, errmsg
        '''
        params = dict( turn='on' )
        if duration:
            params[ 'timer' ] = str( duration )

        return s.get( params )

    def turn_off( s, duration:int = 0 ) -> Tuple[ bool, Optional[str]]:
        '''
        Turn the plug off for duration seconds.  If duration is 0, just turn it off.
        Returns ok, errmsg
        '''
        params = dict( turn='off' )
        if duration:
            params[ 'timer' ] = str( duration )

        return s.get( params )

    def turn_toggle( s ) -> Tuple[ bool, Optional[str]]:
        '''
        Flip the switch.
        Returns ok, errmsg
        '''
        params = dict( turn='toggle' )
        return s.get( params )

    def get( s, params:Dict[str,str] ) -> Tuple[ bool, Optional[str]]:
        '''
        Issue HTTP GET to the plug's IP.
        Returns ok, errmsg
        '''

        errmsg = ''
        try:
            r = requests.get( s.url, params=params )
            log.info( 'HTTP GET %s?%s => %s', s.url, params, r.status_code )
            if r.ok:
                jdata = r.json()
                # see https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
                log.info( 'r.json() => %s', jdata )

                return True, None

            errmsg = str( r )

        except ValueError as err:
            # failed to parse the response JSON
            errmsg = str( err )


        except RequestException as err:
            log.info( 'HTTP GET %s?%s =>\n%s', s.url, params, err )
            for arg in err.args:
                log.info( 'err.arg:\n%s', arg )
            #log.info( 'err.errno %s', err.errno )
            #log.info( 'err.filename %s', err.filename )
            #log.info( 'err.filename2 %s', err.filename2 )
            #log.info( 'err.response %s', err.response )
            #log.info( 'err.strerror %s', err.strerror )

            errmsg = str( err )

        return False, errmsg

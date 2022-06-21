#
#  Wrapper for a shelly plug
#  https://www.shelly-support.eu/forum/index.php?thread/775-collection-of-http-commands/&postID=7410#post7410
#
import ssl
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

        s.host = ip
        # TODO: validate ip?
        return

    def turn_on( s, duration:int = 0 ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        Turn the plug on for duration seconds.
        If duration is 0, just turn it on.
        Returns ok, errmsg
        '''
        params = dict( turn='on' )
        if duration:
            params[ 'timer' ] = str( duration )

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get( '/relay/0', params )

    def turn_off( s, duration:int = 0 ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        Turn the plug off for duration seconds.
        If duration is 0, just turn it off.
        Returns ok, errmsg
        '''
        params = dict( turn='off' )
        if duration:
            params[ 'timer' ] = str( duration )

        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get( '/relay/0', params )

    def turn_toggle( s ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        Flip the switch.
        Returns ok, errmsg
        '''
        params = dict( turn='toggle' )
        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get( '/relay/0', params )

    def is_on( s ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        Get switch status
        Returns ok, errmsg, jdata
        '''
        # https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs-relay-0
        return s.get( '/relay/0')

    def get( s, uri:str, params:Dict[str,str] = {} ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        Issue HTTP GET to the plug's IP.
        Returns ok, errmsg, jdata
        '''

        assert isinstance(uri, str)
        url = f'http://{s.host}{uri}'
        errmsg = ''
        try:
            r = requests.get( url, params=params )
            if params:
                log.info( 'HTTP GET %s?%s => %s', url, params, r.status_code )
            else:
                log.info( 'HTTP GET %s => %s', url, r.status_code )
            if r.ok:
                jdata = r.json()
                log.info( 'r.json() => %s', jdata )

                return True, None, jdata

            errmsg = str( r )

        except ValueError as err:
            # failed to parse the response JSON
            errmsg = str( err )


        except RequestException as err:
            log.info( 'HTTP GET %s?%s =>\n%s', url, params, err )
            for arg in err.args:
                log.info( 'err.arg:\n%s', arg )
            #log.info( 'err.errno %s', err.errno )
            #log.info( 'err.filename %s', err.filename )
            #log.info( 'err.filename2 %s', err.filename2 )
            #log.info( 'err.response %s', err.response )
            #log.info( 'err.strerror %s', err.strerror )

            errmsg = str( err )

        return False, errmsg, None

    def rpc( s, method:str, params:Dict[str,str] = {} ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        gen2 API
        see https://shelly-api-docs.shelly.cloud/gen2/Overview/RPCProtocol
        '''

        assert isinstance( method, str )
        assert method

        # prepare params
        assert isinstance( params, dict )

        url = f'http://{s.host}/rpc/'
        request_frame = dict( id=123, src='123456', method=method )
        if params:
            request_frame['params'] = params
        errmsg = ''
        try:
            r = requests.post( url, json=request_frame )
            log.info( 'HTTP POST %s?%s => %s',
                url, request_frame, r.status_code )
            if r.ok:
                jdata = r.json()
                log.info( 'r.json() => %s', jdata )
                assert jdata[ 'id' ] == request_frame[ 'id' ]
                assert jdata[ 'src' ] # e.g. 'shellyplugus-083af2005bf0'
                assert jdata[ 'dst' ] == request_frame[ 'src' ]
                if 'error' in jdata:
                    err = jdata[ 'error' ]
                    assert 'code' in  err
                    assert 'message' in  err
                    return False, None, err['message']

                assert 'result' in jdata
                return True, None, jdata

            errmsg = str( r )

        except ValueError as err:
            # failed to parse the response JSON
            errmsg = str( err )


        except RequestException as err:
            log.info( 'HTTP GET %s?%s =>\n%s', url, params, err )
            for arg in err.args:
                log.info( 'err.arg:\n%s', arg )
            #log.info( 'err.errno %s', err.errno )
            #log.info( 'err.filename %s', err.filename )
            #log.info( 'err.filename2 %s', err.filename2 )
            #log.info( 'err.response %s', err.response )
            #log.info( 'err.strerror %s', err.strerror )

            errmsg = str( err )

        return False, errmsg, None

    def get_status( s ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetstatus
        '''
        ok, errmsg, jdata = s.rpc( 'Shelly.GetStatus' )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

    def get_config( s ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetconfig
        '''
        ok, errmsg, jdata = s.rpc( 'Shelly.GetConfig' )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

    def get_device_info( s ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellygetdeviceinfo
        '''
        ok, errmsg, jdata = s.rpc( 'Shelly.GetDeviceInfo' )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

    def list_methods( s ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Overview/CommonServices/Shelly#shellylistmethods
        '''
        ok, errmsg, jdata = s.rpc( 'Shelly.ListMethods' )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

    def get_input_config( s, id='0' ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Input
        '''
        ok, errmsg, jdata = s.rpc( 'Input.GetConfig', {'id': id} )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

    def get_input_status( s, id=0 ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Input
        '''
        ok, errmsg, jdata = s.rpc( 'Input.GetStatus', {'id': id} )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

    def get_switch_config( s, id=0 ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Switch
        '''
        ok, errmsg, jdata = s.rpc( 'Switch.GetConfig', {'id': id} )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

    def get_switch_status( s, id=0 ) -> Tuple[
            bool, Optional[str], Optional[Dict[str,str]]]:
        '''
        https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Switch
        '''
        ok, errmsg, jdata = s.rpc( 'Switch.GetStatus', {'id': id} )
        if ok:
            jdata = jdata[ 'result' ]
        return ok, errmsg, jdata

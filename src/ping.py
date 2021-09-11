#
import subprocess

def ping( hostname:str, timeout=0.1 ) -> str:
    '''
    Ping hostname for upto timeout secs.
    Returns: rtt, e.g. '7.445 ms' or '' in case of failure
    '''
    try:
        cmdv = [ 'ping', '-q', '-c', '1', hostname ]
        res = subprocess.run( cmdv, timeout=timeout, text=True, capture_output=True )
        if res.returncode != 0:
            return ''

        parts = res.stdout.split( '\n' )
        parts = [ part for part in parts if part ]
        part = parts[-1]
        parts = part.split( '=' )
        part = parts[-1]
        parts = part.split( ' ' )
        parts = [ part for part in parts if part ]
        unit = parts[-1]
        part = parts[0]
        parts = part.split( '/' )
        part = parts[0]
        return f'{part} {unit}'

    except subprocess.TimeoutExpired:
        return ''

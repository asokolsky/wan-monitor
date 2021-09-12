#
# 
#

import json
import pickle
from typing import Any

class JsonSerializable:
    '''
    Parent for an object that should be serialized to/from JSON
    TODO: save class name
    '''
    def __init__( s ) -> None:
        s.class_name = type( s ).__name__
        return

    def dumps( s ) -> str:
        '''
        Serialize object into a string
        '''
        return json.dumps(
            s,
            default=lambda o: o.__dict__, sort_keys=True,
            separators=(',', ':')
            #indent=4 
        )

    def dump( s, f ):
        '''
        Serialize object into a file
        '''
        return json.dump(
            s, f, default=lambda o: o.__dict__, sort_keys=True,
            separators=(',', ':')
            #indent=4
        )

    def loads( s, datas:str ) -> bool:
        '''
        Load object values from a string
        '''
        data = json.loads( datas )
        for k,v in data.items():
            s.__setattr__(k,v)
        return True

    def load( s, f ) -> None:
        '''
        Load object values from a file
        '''
        data = json.load( f )
        for k,v in data.items():
            s.__setattr__(k,v)
        return

    def __repr__( s ) -> str:
        return s.dumps()

    def to_file( s, path:str ) -> bool:
        '''
        Save the object values into a file identified by a path
        '''
        res = False
        try:
            with open( path, 'w' ) as f:
                s.dump( f )
                res = True
        except FileNotFoundError:
            pass

        return res

    def from_file( s, path:str ) -> bool:
        '''
        Load the object values into a file identified by a path
        '''
        res = False
        try:
            with open( path, 'r' ) as f:
                s.load( f )
                res = True
        except FileNotFoundError:
            pass

        return res

    def __eq__( s, other:Any ) -> bool:
        '''
        To support comparison of instances...
        '''
        #p1 = pickle.dumps( s )
        #p1len = len( p1 )
        #p2 = pickle.dumps( other )
        #p2len = len( p2 )
        #return (p1len == p2len) and (p1 == p2)
        return str(s) == str(other)
        #if not isinstance( other, dict ):
        #    return False
        #if len( s ) != len( other ):
        #    return False
        #for k,v in s.items():
        #    if other[k] != v:
        #        return False
        #return True

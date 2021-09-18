#
#
#
import json
import pickle
from typing import Any, TextIO

class JsonSerializable:
    '''
    Parent for an object that should be serialized to/from JSON
    '''

    def __init__( s ) -> None:
        # at the very least we will be serializing the class name
        s.class_name = type( s ).__name__
        return

    def dumps( s ) -> str:
        '''
        Serialize object into a string
        '''
        # TODO: catch exception raised by bad json?
        return json.dumps(
            s,
            default=lambda o: o.__dict__, sort_keys=True,
            separators=(',', ':')
            #indent=4
        )

    def dump( s, f:TextIO ) -> None:
        '''
        Serialize object into a file
        '''
        # TODO: catch exception raised by bad json?
        json.dump(
            s, f, default=lambda o: o.__dict__, sort_keys=True,
            separators=(',', ':')
            #indent=4
        )
        return

    def loads( s, datas:str ) -> bool:
        '''
        Load object values from a string.
        '''
        try:
            data = json.loads( datas )
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            return False

        # verify class name is right
        if data.get( 'class_name', '') != s.class_name:
            return False

        for k,v in data.items():
            s.__setattr__(k,v)
        return True

    def load( s, f:TextIO ) -> bool:
        '''
        Load object values from a file
        '''
        try:
            data = json.load( f )
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            return False

        # verify class name is right
        if data.get( 'class_name', '') != s.class_name:
            return False

        for k,v in data.items():
            s.__setattr__(k,v)
        return True

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
        # TODO: catch exception raised by bad json

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

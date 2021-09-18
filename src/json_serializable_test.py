#
# 
#

from typing import List
import unittest

from json_serializable import JsonSerializable

class Animal( JsonSerializable ):
    def __init__( s, species:str='', sound:str='', name:str='' ):
        super().__init__()
        s.name = name
        s.sound = sound
        s.species = species
        return

class Dog( Animal ):
    def __init__( s, name:str='' ):
        super().__init__( 'dog', 'bark', name )
        return

class Cat( Animal ):
    def __init__( s, name:str='' ):
        super().__init__( 'cat', 'meouw', name )
        return

class Person( Animal ):
    def __init__( s, name:str='', pets:List[Animal]=[] ):
        super().__init__( 'homo', 'blah', name )
        s.pets = pets
        return

class JsonSerializable_test( unittest.TestCase ):
    '''
    class JsonSerializable test cases
    TODO: test file ops
    '''

    def test_dumps_eq_loads( s ) -> None:
        rudy = Dog( 'Rudy' )
        dogs = rudy.dumps()

        s.assertEqual( dogs, '{"class_name":"Dog","name":"Rudy","sound":"bark","species":"dog"}' )

        dog = Dog()
        s.assertNotEqual( dog, rudy )

        s.assertTrue( dog.loads( dogs ) )
        s.assertTrue( dog == rudy )
        s.assertEqual( dog, rudy )

        alex = Person( 'Alex', [rudy] )
        persons = alex.dumps()
        s.assertEqual( persons,
            '{"class_name":"Person","name":"Alex","pets":['+dogs+'],"sound":"blah","species":"homo"}' )
        return

    def test_loads_fail( s ) -> None:
        '''
        test loads from improperly formatted string
        '''
        return

    def test_load_fail( s ) -> None:
        '''
        test load from non-existent file, file with improperly formatted content
        '''
        return



if __name__ == '__main__':
    unittest.main()

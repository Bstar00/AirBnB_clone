#!/usr/bin/python3
"""This module implements the storage engine
   The stoage engine uses the file system to store data
   the module contains only one class for
   serializing and deseializing the data
"""
import json

import datetime

from os.path import exists


class FileStorage:
    """The storage class for serializing
        and deserializing data
    """

    __file_path = 'db.json'

    __objects = dict()

    def __init__(self):
        """The filestorage class constructor"""

        pass

    def all(self):
        """Returns the dictionary __objects"""

        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""

        if not obj:

            raise ValueError('Missing instance argument')

        from models.base_model import BaseModel

        if not issubclass(type(obj), BaseModel):

            raise TypeError('{obj} must be a subclass of BaseModel')

        obj_in_dict = obj.to_dict()

        key = f"{obj_in_dict['__class__']}.{obj_in_dict['id']}"

        self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""

        dict_to_save = {k: v.to_dict() for k, v in self.__objects.items()}

        with open(self.__file_path, 'w', encoding='utf-8') as file:
            file.write(self.convert_to_json(dict_to_save))

    @staticmethod
    def convert_to_json(json_str):
        """Verify the json_string supplied"""
        if not json_str:
            raise ValueError('No input data')

        try:
            return json.dumps(json_str)

        except Exception as e:

            raise TypeError('Invalid JSON string supplied')

    def reload(self):
        """deserializes the JSON file to __objects"""

        if exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:

                file_content = file.read()

                try:
                    retreived_dict = json.loads(file_content)

                    objs = {k: self.create_obj(**v) for k, v in retreived_dict}

                    self.__objects = objs

                except Exception as e:
                    pass

    def create_obj(self, **dictionary):
        """Create an object from the dictionary"""

        return dictionary['__class__'](**dictionary)

    def classes(self):
        """Returns a dictionary of all implemented classes"""

        from models.base_model import BaseModel

        from models.user import User

        from models.state import State

        from models.city import City

        from models.amenity import Amenity

        from models.place import Place

        from models.review import Review

        return {
                "BaseModel": BaseModel,

                "User": User,

                "State": State,

                "City": City,

                "Amenity": Amenity,

                "Place": Place,

                "Review": Review
        }

    def attributes(self):
        """Return the attributes and its type for all objects"""
        return {
                "BaseModel": {
                                'id': str,
                                'created_at': datetime.datetime,
                                'updated_at': datetime.datetime
                                },

                "User": {
                            'email': str,
                            'password': str,
                            'first_name': str,
                            'last_name': str
                        },

                "State": {'name': str},

                "City": {
                            'state_id': str,
                            'name': str
                        },

                "Amenity": {'name': str},

                "Place": {
                            'city_id': str,
                            'user_id': str,
                            'name': str,
                            'description': str,
                            'number_rooms': int,
                            'max_guest': int,
                            'price_by_night': int,
                            'longitude': float,
                            'latitude': float,
                            'amenity_ids': list
                        },

                "Review": {
                            'place_id': str,
                            'user_id': str,
                            'text': str
                            }
        }

#!/usr/bin/env python3

""" Base model for models that have things in common"""

from uuid import uuid4
from datetime import datetime


class BaseModel:
    """ Base class for all models """

    def __init__(self):
        """ The class constructor """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """ Return a human-readable format of the object """
        string = f"[{type(self).__name__}] ({self.id}) {self.__dict__}"
        return string

    def save(self):
        """ updates the public instance attribute updated_at
            with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """ returns a dictionary containing all keys/values
            of __dict__ of the instance.
            Dates objects are converted to str objects
            in ISO format
        """

        dictionary_format = self.__dict__.copy()
        dictionary_format['__class__'] = type(self).__name__
        dictionary_format['created_at'] = self.created_at.isoformat()
        dictionary_format['updated_at'] = self.updated_at.isoformat()
        return dictionary_format

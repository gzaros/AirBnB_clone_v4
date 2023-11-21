#!/usr/bin/python3
"""class to manage fileStorage for hbnb clone"""
import json

class FileStorage:
    """class to managestorage of hbnb models in format JSON"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """get dictionary of models currently in fileStorage"""
        if cls is None:
            return FileStorage.__objects
        else:
            class_objects = {}
            for key, value in FileStorage.__objects.items():
                if type(value) is cls:
                    class_objects[key] = FileStorage.__objects[key]
            return class_objects

    def new(self, obj):
        """add new Objet to fileStorage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """save fileStorage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """loaded fileStorage dictionary From file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ remove obj from __objects if it’s inside """
        if obj is not None:
            try:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                if key in FileStorage.__objects.keys():
                    FileStorage.__objects.pop(key)
            except AttributeError:
                pass

#!/usr/bin/python3
'''  '''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """  """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the SQL database"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                           user, passwd, host, database), pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Return all objects of all classes in the database
        in case no classe name provided, else get one class objects
        """
        objs = {}

        def gen_key(name, id):
            return "{}.{}".format(name, id)

        cls_list = [User, State, City, Amenity, Place, Review]
        if cls is None:
            for Class in cls_list:
                class_data = self.__session.query(Class).all()
                for data in class_data:
                    key = gen_key(Class.__name__, data.id)
                    objs[key] = data
        else:
            class_data = self.__session.query(cls).all()
            for data in class_data:
                key = gen_key(cls.__name__, data.id)
                objs[key] = data
        return objs

    def new(self, obj):
        """ add the object to the current database
        session (self.__session)"""
        if obj is not None:
            if not self.__session:
                raise Exception("Session is not srarted")
            self.__session.add(obj)
            self.__session.commit()

    def save(self):
        """ commit all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None"""

        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """create all tables in the database, and"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))()

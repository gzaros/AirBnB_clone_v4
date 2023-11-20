#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')

    @property
    def cities(self):
        """Returns the cities"""
        from models import storage
        city_list = []
        for key, value in storage.all(City).items():
            if self.id == value.state_id:
                city_list.append(value)
        return city_list

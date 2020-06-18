# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Usuario(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, email: str=None, password: str=None):  # noqa: E501
        """Usuario - a model defined in Swagger

        :param email: The email of this Usuario.  # noqa: E501
        :type email: str
        :param password: The password of this Usuario.  # noqa: E501
        :type password: str
        """
        self.swagger_types = {
            'email': str,
            'password': str
        }

        self.attribute_map = {
            'email': 'email',
            'password': 'password'
        }

        self._email = email
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'Usuario':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Usuario of this Usuario.  # noqa: E501
        :rtype: Usuario
        """
        return util.deserialize_model(dikt, cls)

    @property
    def email(self) -> str:
        """Gets the email of this Usuario.


        :return: The email of this Usuario.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this Usuario.


        :param email: The email of this Usuario.
        :type email: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def password(self) -> str:
        """Gets the password of this Usuario.


        :return: The password of this Usuario.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this Usuario.


        :param password: The password of this Usuario.
        :type password: str
        """
        if password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501

        self._password = password

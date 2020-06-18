# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Video(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, url: str=None, titulo: str=None, descripcion: str=None, ubicacion: str=None, duracion: str=None, usuario_id: str=None, visibilidad: str=None):  # noqa: E501
        """Video - a model defined in Swagger

        :param url: The url of this Video.  # noqa: E501
        :type url: str
        :param titulo: The titulo of this Video.  # noqa: E501
        :type titulo: str
        :param descripcion: The descripcion of this Video.  # noqa: E501
        :type descripcion: str
        :param ubicacion: The ubicacion of this Video.  # noqa: E501
        :type ubicacion: str
        :param duracion: The duracion of this Video.  # noqa: E501
        :type duracion: str
        :param usuario_id: The usuario_id of this Video.  # noqa: E501
        :type usuario_id: str
        :param visibilidad: The visibilidad of this Video.  # noqa: E501
        :type visibilidad: str
        """
        self.swagger_types = {
            'url': str,
            'titulo': str,
            'descripcion': str,
            'ubicacion': str,
            'duracion': str,
            'usuario_id': str,
            'visibilidad': str
        }

        self.attribute_map = {
            'url': 'url',
            'titulo': 'titulo',
            'descripcion': 'descripcion',
            'ubicacion': 'ubicacion',
            'duracion': 'duracion',
            'usuario_id': 'usuario_id',
            'visibilidad': 'visibilidad'
        }

        self._url = url
        self._titulo = titulo
        self._descripcion = descripcion
        self._ubicacion = ubicacion
        self._duracion = duracion
        self._usuario_id = usuario_id
        self._visibilidad = visibilidad

    @classmethod
    def from_dict(cls, dikt) -> 'Video':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Video of this Video.  # noqa: E501
        :rtype: Video
        """
        return util.deserialize_model(dikt, cls)

    @property
    def url(self) -> str:
        """Gets the url of this Video.


        :return: The url of this Video.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this Video.


        :param url: The url of this Video.
        :type url: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def titulo(self) -> str:
        """Gets the titulo of this Video.


        :return: The titulo of this Video.
        :rtype: str
        """
        return self._titulo

    @titulo.setter
    def titulo(self, titulo: str):
        """Sets the titulo of this Video.


        :param titulo: The titulo of this Video.
        :type titulo: str
        """
        if titulo is None:
            raise ValueError("Invalid value for `titulo`, must not be `None`")  # noqa: E501

        self._titulo = titulo

    @property
    def descripcion(self) -> str:
        """Gets the descripcion of this Video.


        :return: The descripcion of this Video.
        :rtype: str
        """
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion: str):
        """Sets the descripcion of this Video.


        :param descripcion: The descripcion of this Video.
        :type descripcion: str
        """
        if descripcion is None:
            raise ValueError("Invalid value for `descripcion`, must not be `None`")  # noqa: E501

        self._descripcion = descripcion

    @property
    def ubicacion(self) -> str:
        """Gets the ubicacion of this Video.


        :return: The ubicacion of this Video.
        :rtype: str
        """
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, ubicacion: str):
        """Sets the ubicacion of this Video.


        :param ubicacion: The ubicacion of this Video.
        :type ubicacion: str
        """
        if ubicacion is None:
            raise ValueError("Invalid value for `ubicacion`, must not be `None`")  # noqa: E501

        self._ubicacion = ubicacion

    @property
    def duracion(self) -> str:
        """Gets the duracion of this Video.


        :return: The duracion of this Video.
        :rtype: str
        """
        return self._duracion

    @duracion.setter
    def duracion(self, duracion: str):
        """Sets the duracion of this Video.


        :param duracion: The duracion of this Video.
        :type duracion: str
        """
        if duracion is None:
            raise ValueError("Invalid value for `duracion`, must not be `None`")  # noqa: E501

        self._duracion = duracion

    @property
    def usuario_id(self) -> str:
        """Gets the usuario_id of this Video.


        :return: The usuario_id of this Video.
        :rtype: str
        """
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, usuario_id: str):
        """Sets the usuario_id of this Video.


        :param usuario_id: The usuario_id of this Video.
        :type usuario_id: str
        """
        if usuario_id is None:
            raise ValueError("Invalid value for `usuario_id`, must not be `None`")  # noqa: E501

        self._usuario_id = usuario_id

    @property
    def visibilidad(self) -> str:
        """Gets the visibilidad of this Video.


        :return: The visibilidad of this Video.
        :rtype: str
        """
        return self._visibilidad

    @visibilidad.setter
    def visibilidad(self, visibilidad: str):
        """Sets the visibilidad of this Video.


        :param visibilidad: The visibilidad of this Video.
        :type visibilidad: str
        """
        if visibilidad is None:
            raise ValueError("Invalid value for `visibilidad`, must not be `None`")  # noqa: E501

        self._visibilidad = visibilidad

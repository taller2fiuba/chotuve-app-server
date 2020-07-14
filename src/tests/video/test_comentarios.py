# pylint: skip-file
import unittest
import mock

from tests.base import LoginMockTestCase
from app import app, log

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

class VideoComentariosTestCase(LoginMockTestCase):
    def cargar_mock_obtener_video(self, mock, id):
        mock.return_value = {
            "descripcion": None,
            "ubicacion": None,
            "visibilidad": "publico",
            "habilitado": True,
            "_id": id,
            "url": "chauchis",
            "titulo": "holis",
            "usuario_id": 1,
            "duracion": 120,
            "time_stamp": "2020-06-07T11:31:40.665Z",
            "__v": 0
        }
        
        return mock

    @mock.patch('app.servicios.auth_server.obtener_usuarios')
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_obtener_comentarios_video_sin_comentarios(self, mock_obtener_video, mock_auth):
        self.cargar_mock_obtener_video(mock_obtener_video, "5edcd01cd3cf810031d865db")
        mock_auth.return_value = {}

        response = self.app.get("/video/5edcd01cd3cf810031d865db/comentario")
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, [])
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_devuelve_201(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"comentario": "test"}

        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json, {})
    
    @mock.patch('app.servicios.auth_server.obtener_usuarios')
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_obtener_comentarios_video_con_comentarios(self, mock, mock_auth):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        autor = {
            "id": 1,
            "nombre": "",
            "apellido": "",
            "email": "lucho@lucho.com",
            "telefono": "",
            "foto": ""
        }
        mock_auth.return_value = {autor['id']: autor}

        body = {"comentario": "test"}

        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        
        self.assertEquals(response.status_code, 201)

        response = self.app.get("/video/5edcd01cd3cf810031d865db/comentario")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json), 1)
        self.assertEquals(response.json[0]["autor"], autor)
        self.assertEquals(response.json[0]["comentario"], "test")
        self.assertIn("fecha", response.json[0])
        self.assertIsNotNone(response.json[0]["fecha"])

    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_con_content_type_erroneo_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"comentario": "test"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            data=body)
        self.assertEquals(response.status_code, 400)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_body_sin_clave_comentario_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        self.assertEquals(response.status_code, 400)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_vacio_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"comentario": ""}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        self.assertEquals(response.status_code, 400)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_nulo_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"comentario": None}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        self.assertEquals(response.status_code, 400)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_tipo_incorrecto_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"comentario": 17}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        self.assertEquals(response.status_code, 400)
        
        body = {"comentario": {"a": "test"}}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        self.assertEquals(response.status_code, 400)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_a_video_inexistente_devuelve_404(self, mock):
        mock.return_value = None
        body = {"comentario": "test"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body)
        self.assertEquals(response.status_code, 404)
   
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_comentario_content_type_con_charset_devuelve_201(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"comentario": "test"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/comentario", 
            json=body, headers={"Content-Type": "application/json; charset=UTF-8"})
        self.assertEquals(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()

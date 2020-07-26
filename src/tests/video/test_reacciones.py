# pylint: skip-file
import unittest
import mock

from tests.base import LoginMockTestCase
from app import app, log

class VideoReaccionesTestCase(LoginMockTestCase):
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

    @mock.patch('app.servicios.media_server.obtener_video')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_agregar_me_gusta_a_video_sin_me_gusta_devuelve_201(self, _, mock_obtener_video):
        self.cargar_mock_obtener_video(mock_obtener_video, "5edcd01cd3cf810031d865db")
        body = {"reaccion": "me-gusta"}

        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 201)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_agregar_me_gusta_a_video_con_me_gusta_devuelve_200(self, _, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"reaccion": "me-gusta"}

        # Poner el MG
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        # Sacar el MG
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 200)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_agregar_no_me_gusta_a_video_sin_no_me_gusta_devuelve_201(self, _, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"reaccion": "no-me-gusta"}

        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 201)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_agregar_no_me_gusta_a_video_con_no_me_gusta_devuelve_200(self, _, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "no-me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 200)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_agregar_me_gusta_a_video_con_no_me_gusta_devuelve_200(self, _, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "no-me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 200)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_agregar_no_me_gusta_a_video_con_me_gusta_devuelve_200(self, _, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        body = {"reaccion": "no-me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 200)

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_me_gusta_video_trae_reacciones(self, mock_obtener_video, mock_get_usuario):
        self.cargar_mock_obtener_video(mock_obtener_video, "5edcd01cd3cf810031d865db")
        mock_get_usuario.return_value = {
            "id": 1,
            "nombre": "",
            "apellido": "",
            "email": "test@test.com",
            "telefono": "",
            "foto": ""
        }
        
        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        response = self.app.get("/video/5edcd01cd3cf810031d865db")
        data = response.json
        
        self.assertEqual(response.status_code, 200)
        assert 'me-gustas' in data
        self.assertEquals(data['me-gustas'], 1)
        assert 'no-me-gustas' in data
        self.assertEquals(data['no-me-gustas'], 0)
        assert 'mi-reaccion' in data
        self.assertEquals(data['mi-reaccion'], 'me-gusta')
    
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_no_me_gusta_video_trae_reacciones(self, mock_obtener_video, mock_get_usuario):
        self.cargar_mock_obtener_video(mock_obtener_video, "5edcd01cd3cf810031d865db")
        mock_get_usuario.return_value = {
            "id": 1,
            "nombre": "",
            "apellido": "",
            "email": "test@test.com",
            "telefono": "",
            "foto": ""
        }

        body = {"reaccion": "no-me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        response = self.app.get("/video/5edcd01cd3cf810031d865db")
        data = response.json
        
        self.assertEqual(response.status_code, 200)
        assert 'me-gustas' in data
        self.assertEquals(data['me-gustas'], 0)
        assert 'no-me-gustas' in data
        self.assertEquals(data['no-me-gustas'], 1)
        assert 'mi-reaccion' in data
        self.assertEquals(data['mi-reaccion'], 'no-me-gusta')
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_reaccion_invalida_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "invalida"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 400)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_agregar_me_gusta_a_video_inexistente_devuelve_404(self, mock):
        mock.return_value = None
        
        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 404)
    
    @mock.patch('app.servicios.media_server.obtener_video')
    def test_reaccionar_con_content_type_erroneo_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            data=body)
        self.assertEquals(response.status_code, 400)

    @mock.patch('app.servicios.media_server.obtener_video')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_reaccionar_content_type_con_charset_devuelve_201(self, _, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")

        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", json=body,
                                 headers={"Content-Type": 'application/json; charset=UTF-8'})
        self.assertEquals(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()

# pylint: skip-file
import unittest
import mock

from tests.base import LoginMockTestCase
from app import app

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

class VideoReaccionesTestCase(LoginMockTestCase):
    def cargar_mock_obtener_video(self, mock, id):
        mock.return_value.status_code = 200
        mock.return_value.json = lambda: {
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

    @mock.patch('media_server_api.obtener_video')
    def test_agregar_me_gusta_a_video_sin_me_gusta_devuelve_201(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"reaccion": "me-gusta"}

        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 201)
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_me_gusta_a_video_con_me_gusta_devuelve_200(self, mock):
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
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_no_me_gusta_a_video_sin_no_me_gusta_devuelve_201(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        body = {"reaccion": "no-me-gusta"}

        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 201)
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_no_me_gusta_a_video_con_no_me_gusta_devuelve_200(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "no-me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 200)
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_me_gusta_a_video_con_no_me_gusta_devuelve_200(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "no-me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 200)
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_no_me_gusta_a_video_con_me_gusta_devuelve_200(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 201)

        body = {"reaccion": "no-me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        
        self.assertEquals(response.status_code, 200)
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_me_gusta_video_trae_reacciones(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
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
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_no_me_gusta_video_trae_reacciones(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
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
    
    @mock.patch('media_server_api.obtener_video')
    def test_reaccion_invalida_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "invalida"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 400)
    
    @mock.patch('media_server_api.obtener_video')
    def test_agregar_me_gusta_a_video_inexistente_devuelve_404(self, mock):
        mock.return_value.status_code = 404
        
        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            json=body)
        self.assertEquals(response.status_code, 404)
    
    @mock.patch('media_server_api.obtener_video')
    def test_reaccionar_con_content_type_erroneo_devuelve_400(self, mock):
        self.cargar_mock_obtener_video(mock, "5edcd01cd3cf810031d865db")
        
        body = {"reaccion": "me-gusta"}
        response = self.app.post("/video/5edcd01cd3cf810031d865db/reaccion", 
            data=body)
        self.assertEquals(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

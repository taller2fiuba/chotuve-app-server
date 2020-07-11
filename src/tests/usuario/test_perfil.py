import unittest
import mock

from tests.base import LoginMockTestCase

class UsuarioActualizarPerfilMockTestCase(LoginMockTestCase):
    @mock.patch('auth_server_api.requests.put')
    def test_actualizar_perfil_exitosamente(self, mock_put):
        mock_put.return_value.json = lambda: {}
        mock_put.return_value.status_code = 200

        nuevo_nombre = "Lucas"
        nuevo_apellido = "Perez"
        nueva_direccion = "La Pampa 1111"
        nuevo_telefono = "1530449926"
        nueva_foto = 'foto.jpg'
        response = self.app.put('/usuario/perfil', json={
            'nombre': nuevo_nombre,
            'apellido': nuevo_apellido,
            'telefono': nuevo_telefono,
            'direccion': nueva_direccion,
            'foto': nueva_foto
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.requests.put')
    def test_actualizar_perfil_sin_campos_falla(self, mock_put):
        mock_put.return_value.json = lambda: {}
        mock_put.return_value.status_code = 400

        response = self.app.put('/usuario/perfil')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.requests.put')
    def test_actualizar_perfil_sin_un_campos_obligatorio(self, mock_put):
        mock_put.return_value.json = lambda: {}
        mock_put.return_value.status_code = 400

        nuevo_nombre = "Lucas"
        nueva_direccion = "La Pampa 1111"
        nuevo_telefono = "123456879"

        response = self.app.put('/usuario/perfil', json={
            'nombre': nuevo_nombre,
            'direccion': nueva_direccion,
            'telefono': nuevo_telefono})

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

class UsuarioConsultarPerfilMockTestCase(LoginMockTestCase):
    @mock.patch('media_server_api.obtener_videos_usuario')
    @mock.patch('auth_server_api.requests.get')
    def test_get_mi_perfil_sin_campos_completados(self, mock_get, mock_media):
        mock_get.return_value.json = lambda: {
            'id': 1,
            'nombre': None,
            'apellido': None,
            'email': 'test@test',
            'telefono': None,
            'direccion': None,
            'foto': None}
        mock_get.return_value.status_code = 200

        mock_media.return_value.json = lambda: {
            "videos": [],
            "cantidad_de_videos": 20
        }
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/perfil')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'id': 1,
            'nombre': None,
            'apellido': None,
            'email': 'test@test',
            'telefono': None,
            'direccion': None,
            'foto': None,
            'cantidad-contactos': 0,
            'cantidad-videos': 20
        }, response.json)

    @mock.patch('media_server_api.obtener_videos_usuario')
    @mock.patch('auth_server_api.requests.get')
    def test_get_otro_perfil_sin_campos_completados(self, mock_get, mock_media):
        mock_get.return_value.json = lambda: {
            'id': 1,
            'nombre': None,
            'apellido': None,
            'email': 'test@test',
            'telefono': None,
            'direccion': None,
            'foto': None}
        mock_get.return_value.status_code = 200

        mock_media.return_value.json = lambda: {
            "videos": [],
            "cantidad_de_videos": 20
        }
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/1/perfil')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'id': 1,
            'nombre': None,
            'apellido': None,
            'email': 'test@test',
            'telefono': None,
            'direccion': None,
            'foto': None,
            'cantidad-contactos': 0,
            'cantidad-videos': 20
        }, response.json)

    @mock.patch('media_server_api.obtener_videos_usuario')
    @mock.patch('auth_server_api.requests.get')
    def test_get_mi_perfil_con_todos_los_campos(self, mock_get, mock_media):
        mock_get.return_value.json = lambda: {
            'id': 1,
            'nombre': 'Lucas',
            'apellido': 'Perez',
            'email': 'test@test',
            'telefono': '123456789',
            'direccion': 'Calle falsa 123',
            'foto': None}
        mock_get.return_value.status_code = 200

        mock_media.return_value.json = lambda: {
            "videos": [],
            "cantidad_de_videos": 20
        }
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/perfil')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'id': 1,
            'nombre': 'Lucas',
            'apellido': 'Perez',
            'email': 'test@test',
            'telefono': '123456789',
            'direccion': 'Calle falsa 123',
            'foto': None,
            'cantidad-contactos': 0,
            'cantidad-videos': 20
        }, response.json)

    @mock.patch('media_server_api.obtener_videos_usuario')
    @mock.patch('auth_server_api.requests.get')
    def test_get_otro_perfil_con_todos_los_campos(self, mock_get, mock_media):
        mock_get.return_value.json = lambda: {
            'id': 2,
            'nombre': 'Lucas',
            'apellido': 'Perez',
            'email': 'test@test',
            'telefono': '123456789',
            'direccion': 'Calle falsa 123',
            'foto': None}
        mock_get.return_value.status_code = 200

        mock_media.return_value.json = lambda: {
            "videos": [],
            "cantidad_de_videos": 20
        }
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/2/perfil')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'id': 2,
            'nombre': 'Lucas',
            'apellido': 'Perez',
            'email': 'test@test',
            'telefono': '123456789',
            'direccion': 'Calle falsa 123',
            'foto': None,
            'cantidad-contactos': 0,
            'estado-contacto': None,
            'cantidad-videos': 20
        }, response.json)

    @mock.patch('auth_server_api.requests.get')
    def test_get_otro_perfil_identificador_inexistente(self, mock_get):
        mock_get.return_value.json = lambda: {}
        mock_get.return_value.status_code = 404
        response = self.app.get('/usuario/10215/perfil')
        self.assertEqual(response.status_code, 404)
        self.assertEqual({}, response.json)

if __name__ == '__main__':
    unittest.main()

import unittest
import mock

from tests.base import LoginMockTestCase

class UsuarioActualizarPerfilTestCase(LoginMockTestCase):
    @mock.patch('app.servicios.auth_server.actualizar_usuario')
    def test_actualizar_perfil_exitosamente(self, _):
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

    @mock.patch('app.servicios.auth_server.actualizar_usuario')
    def test_actualizar_perfil_sin_campos_falla(self, _):
        response = self.app.put('/usuario/perfil')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

    @mock.patch('app.servicios.auth_server.actualizar_usuario')
    def test_actualizar_perfil_sin_un_campos_obligatorio(self, _):
        nuevo_nombre = "Lucas"
        nueva_direccion = "La Pampa 1111"
        nuevo_telefono = "123456879"

        response = self.app.put('/usuario/perfil', json={
            'nombre': nuevo_nombre,
            'direccion': nueva_direccion,
            'telefono': nuevo_telefono})

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

class UsuarioConsultarPerfilTestCase(LoginMockTestCase):
    @mock.patch('app.servicios.media_server.obtener_cantidad_videos')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_mi_perfil_sin_campos_completados(self, mock_get, mock_videos):
        mock_videos.return_value = 20
        mock_get.return_value = {
            'id': 1,
            'nombre': None,
            'apellido': None,
            'email': 'test@test',
            'telefono': None,
            'direccion': None,
            'foto': None
        }

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

    @mock.patch('app.servicios.media_server.obtener_cantidad_videos')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_otro_perfil_sin_campos_completados(self, mock_get, mock_videos):
        mock_videos.return_value = 20
        mock_get.return_value = {
            'id': 1,
            'nombre': None,
            'apellido': None,
            'email': 'test@test',
            'telefono': None,
            'direccion': None,
            'foto': None
        }

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

    @mock.patch('app.servicios.media_server.obtener_cantidad_videos')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_mi_perfil_con_todos_los_campos(self, mock_get, mock_videos):
        mock_videos.return_value = 20
        mock_get.return_value = {
            'id': 1,
            'nombre': 'Lucas',
            'apellido': 'Perez',
            'email': 'test@test',
            'telefono': '123456789',
            'direccion': 'Calle falsa 123',
            'foto': None
        }

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

    @mock.patch('app.servicios.media_server.obtener_cantidad_videos')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_otro_perfil_con_todos_los_campos(self, mock_get, mock_videos):
        mock_videos.return_value = 20
        mock_get.return_value = {
            'id': 2,
            'nombre': 'Lucas',
            'apellido': 'Perez',
            'email': 'test@test',
            'telefono': '123456789',
            'direccion': 'Calle falsa 123',
            'foto': None
        }

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

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_otro_perfil_identificador_inexistente(self, mock_get):
        mock_get.return_value = None

        response = self.app.get('/usuario/10215/perfil')
        self.assertEqual(response.status_code, 404)
        self.assertEqual({}, response.json)

if __name__ == '__main__':
    unittest.main()

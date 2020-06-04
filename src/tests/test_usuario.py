import unittest
import mock

from tests.base import BaseTestCase, LoginMockTestCase

class UsuarioTestCase(BaseTestCase):
    @mock.patch('auth_server_api.requests.post')
    def test_post_signup_exitoso(self, mock_post):
        mock_post.return_value.json = lambda: {'Token': '11111'}
        mock_post.return_value.status_code = 201
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual({'Token': '11111'}, response.json)

    @mock.patch('auth_server_api.requests.post')
    def test_post_signup_fallido(self, mock_post):
        error = {'errores': {'email': 'El mail ya se encuentra registrado'}}
        mock_post.return_value.json = lambda: error
        mock_post.return_value.status_code = 400
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, error)

class UsuarioLoginMockTestCase(LoginMockTestCase):

    @mock.patch('auth_server_api.requests.get')
    def test_get_usuario_por_id(self, mock_get):
        mock_get.return_value.json = lambda: {'email': 'test@test'}
        mock_get.return_value.status_code = 200
        response = self.app.get('/usuario/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'email': 'test@test'}, response.json)

    @mock.patch('auth_server_api.get_usuario')
    def test_get_usuario_sin_id_es_el_actual(self, mock_get_usuario):
        mock_get_usuario.return_value.json = lambda: {'email': 'test@test'}
        mock_get_usuario.return_value.status_code = 200
        response = self.app.get('/usuario')
        mock_get_usuario.assert_called_with(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'email': 'test@test'}, response.json)

class UsuarioActualizarPerfilMockTestCase(LoginMockTestCase):

    @mock.patch('auth_server_api.requests.put')
    def test_actualizar_perfil_exitosamente(self, mock_put):
        mock_put.return_value.json = lambda: {}
        mock_put.return_value.status_code = 200

        nuevo_nombre = "Lucas"
        nuevo_apellido = "Perez"
        nueva_direccion = "La Pampa 1111"
        nuevo_telefono = "1530449926"
        response = self.app.put('/usuario/perfil', json={
            'nombre': nuevo_nombre,
            'apellido': nuevo_apellido,
            'telefono': nuevo_telefono,
            'direccion': nueva_direccion})

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

    @mock.patch('auth_server_api.requests.get')
    def test_get_mi_perfil_sin_campos_completados(self, mock_get):
        mock_get.return_value.json = lambda: {
            'email': "test@test"}
        mock_get.return_value.status_code = 200
        response = self.app.get('/usuario/perfil')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'email': "test@test"}, response.json)

    @mock.patch('auth_server_api.requests.get')
    def test_get_otro_perfil_sin_campos_completados(self, mock_get):
        mock_get.return_value.json = lambda: {
            'email': "test@test"}
        mock_get.return_value.status_code = 200
        response = self.app.get('/usuario/perfil/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'email': "test@test"}, response.json)

    @mock.patch('auth_server_api.requests.get')
    def test_get_mi_perfil_con_todos_los_campos(self, mock_get):
        mock_get.return_value.json = lambda: {
            'email': "test@test",
            'nombre': "Lucas",
            'apellido': "Perez",
            'telefono': "123456789",
            'direccion': "Calle falsa 123"}
        mock_get.return_value.status_code = 200
        response = self.app.get('/usuario/perfil')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'email': "test@test",
            'nombre': "Lucas",
            'apellido': "Perez",
            'telefono': "123456789",
            'direccion': "Calle falsa 123"}, response.json)

    @mock.patch('auth_server_api.requests.get')
    def test_get_otro_perfil_con_todos_los_campos(self, mock_get):
        mock_get.return_value.json = lambda: {
            'email': "test@test",
            'nombre': "Lucas",
            'apellido': "Perez",
            'telefono': "123456789",
            'direccion': "Calle falsa 123"}
        mock_get.return_value.status_code = 200
        response = self.app.get('/usuario/perfil/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'email': "test@test",
            'nombre': "Lucas",
            'apellido': "Perez",
            'telefono': "123456789",
            'direccion': "Calle falsa 123"}, response.json)

    @mock.patch('auth_server_api.requests.get')
    def test_get_otro_perfil_identificador_inexistente(self, mock_get):
        mock_get.return_value.json = lambda: {}
        mock_get.return_value.status_code = 404
        response = self.app.get('/usuario/perfil/10215')
        self.assertEqual(response.status_code, 404)
        self.assertEqual({}, response.json)

if __name__ == '__main__':
    unittest.main()

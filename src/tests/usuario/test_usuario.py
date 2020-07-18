import unittest
import mock

from tests.base import BaseTestCase, LoginMockTestCase

class RegistrarUsuarioTestCase(BaseTestCase):
    @mock.patch('app.servicios.auth_server.registrar_usuario')
    def test_post_registro_de_usuario_exitoso(self, mock_auth):
        mock_auth.return_value = 'token-auth', 1
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual({'auth_token': 'token-auth', 'id': 1}, response.json)

    @mock.patch('app.servicios.auth_server.registrar_usuario')
    def test_post_registro_de_usuario_fallido(self, mock_auth):
        error = {'errores': {'email': 'El mail ya se encuentra registrado'}}
        mock_auth.return_value = None
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, error)

class ObtenerUsuarioTestCase(LoginMockTestCase):
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_usuario_por_id(self, mock_auth):
        mock_auth.return_value = {'email': 'test@test'}
        response = self.app.get('/usuario/5')
        mock_auth.assert_called_with(5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'email': 'test@test'}, response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_usuario_sin_id_es_el_actual(self, mock_obtener_usuario):
        mock_obtener_usuario.return_value = {'email': 'test@test'}
        response = self.app.get('/usuario')
        mock_obtener_usuario.assert_called_with(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'email': 'test@test'}, response.json)

if __name__ == '__main__':
    unittest.main()

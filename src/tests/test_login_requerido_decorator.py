import unittest
import mock

from tests.base import BaseTestCase

class LoginRequeridoDecoratorTestCase(BaseTestCase):
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.servicios.auth_server.autenticar')
    def test_middleware_autenticacion_exitosa(self, autenticar, obtener_usuario):
        autenticar.return_value = 3
        obtener_usuario.return_value = {'email': 'test@test.com'}
        token = 'token-valido'
        response = self.app.get('/usuario/1', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'test@test.com')
        autenticar.assert_called_with(token)

    @mock.patch('app.servicios.auth_server.autenticar')
    def test_middleware_autenticacion_fallida(self, autenticar):
        autenticar.return_value = None
        token = 'token-invalido'
        response = self.app.get('/usuario/1', headers={
            'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 401)
        autenticar.assert_called_with(token)


if __name__ == '__main__':
    unittest.main()

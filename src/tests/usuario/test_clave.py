import mock

from tests.base import LoginMockTestCase

class UsuarioClaveTestCase(LoginMockTestCase):
    @mock.patch('app.servicios.auth_server.actualizar_clave')
    def test_actualizar_clave_correctamente(self, mock_auth):
        mock_auth.return_value = True
        response = self.app.put('/usuario/clave', json={
            'password': 'nueva-clave'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

    @mock.patch('app.servicios.auth_server.actualizar_clave')
    def test_actualizar_clave_fallido(self, mock_auth):
        mock_auth.return_value = False
        response = self.app.put('/usuario/clave', json={
            'password': ''
        })
        self.assertEqual(response.status_code, 400)

from tests.servicios.mock_cliente_http import MockClienteHttpTestCase
from app.servicios.servicio_auth_server import AuthServer, AuthServerError

# pylint: disable=too-many-public-methods
class AuthServerTestCase(MockClienteHttpTestCase):
    def setUp(self):
        super().setUp()
        self.auth_server = AuthServer('http://localhost')

    def test_autenticar_envia_solicitud_correcta(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'usuario_id': 1}

        self.auth_server.autenticar('token-de-auth')

        self.mock_get.assert_called_with('/usuario/sesion', headers={
            'Authorization': 'Bearer token-de-auth'
        })

    def test_autenticar_devuelve_id_de_usuario(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'usuario_id': 1}

        uid = self.auth_server.autenticar('token-de-auth')

        self.assertEqual(uid, (1, False))

    def test_autenticar_devuelve_none_con_token_invalido(self):
        self.mock_get.return_value.status_code = 401
        self.mock_get.return_value.json = lambda: {}

        uid = self.auth_server.autenticar('token-invalido')

        self.assertIsNone(uid)

    def test_autenticar_lanza_excepcion_en_error(self):
        self.mock_get.return_value.status_code = 500
        self.mock_get.return_value.json = lambda: {}

        self.assertRaises(AuthServerError, self.auth_server.autenticar, 'token')

    def test_iniciar_sesion_envia_solicitud_correcta(self):
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json = lambda: {'auth_token': 'token', 'id': 1}

        self.auth_server.iniciar_sesion('e-mail', 'clave')

        self.mock_post.assert_called_with('/usuario/sesion', json={
            'email': 'e-mail',
            'password': 'clave'
        })

    def test_iniciar_sesion_devuelve_id_y_token_en_exito(self):
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json = lambda: {'auth_token': 'token', 'id': 1}

        data = self.auth_server.iniciar_sesion('e-mail', 'clave')

        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], 'token')
        self.assertEqual(data[1], 1)

    def test_iniciar_sesion_devuelve_none_en_clave_erronea(self):
        self.mock_post.return_value.status_code = 400
        self.mock_post.return_value.json = lambda: {}

        data = self.auth_server.iniciar_sesion('e-mail', 'clave-erronea')

        self.assertIsNone(data)

    def test_iniciar_sesion_lanza_excepcion_en_error(self):
        self.mock_get.return_value.status_code = 500
        self.mock_get.return_value.json = lambda: {}

        self.assertRaises(AuthServerError, self.auth_server.iniciar_sesion, 'e-mail', 'clave')

    def test_registrar_usuario_envia_solicitud_correcta(self):
        self.mock_post.return_value.status_code = 201
        self.mock_post.return_value.json = lambda: {'auth_token': 'token', 'id': 1}

        self.auth_server.registrar_usuario('e-mail', 'clave')

        self.mock_post.assert_called_with('/usuario', json={
            'email': 'e-mail',
            'password': 'clave'
        })

    def test_registrar_usuario_devuelve_id_y_token_en_exito(self):
        self.mock_post.return_value.status_code = 201
        self.mock_post.return_value.json = lambda: {'auth_token': 'token', 'id': 1}

        data = self.auth_server.registrar_usuario('e-mail', 'clave')

        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], 'token')
        self.assertEqual(data[1], 1)

    def test_registrar_usuario_devuelve_none_si_ya_existe(self):
        self.mock_post.return_value.status_code = 400
        self.mock_post.return_value.json = lambda: {}

        data = self.auth_server.registrar_usuario('e-mail', 'clave-erronea')

        self.assertIsNone(data)

    def test_registrar_usuario_lanza_excepcion_en_error(self):
        self.mock_get.return_value.status_code = 500
        self.mock_get.return_value.json = lambda: {}

        self.assertRaises(AuthServerError, self.auth_server.registrar_usuario, 'e-mail', 'clave')

    def test_obtener_usuario_envia_solicitud_correcta(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'id': 1, 'email': 'e-mail'}

        uid = 1
        self.auth_server.obtener_usuario(uid)

        self.mock_get.assert_called_with(f"/usuario/{uid}")

    def test_obtener_usuario_devuelve_data_de_usuario_en_exito(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'id': 1, 'email': 'e-mail'}

        data = self.auth_server.obtener_usuario(1)

        self.assertEqual(data, {'id': 1, 'email': 'e-mail'})

    def test_obtener_usuario_devuelve_none_en_404(self):
        self.mock_get.return_value.status_code = 404
        self.mock_get.return_value.json = lambda: {}

        data = self.auth_server.obtener_usuario(1)

        self.assertIsNone(data)

    def test_obtener_usuario_lanza_excepcion_en_error(self):
        self.mock_get.return_value.status_code = 500
        self.mock_get.return_value.json = lambda: {}

        self.assertRaises(AuthServerError, self.auth_server.obtener_usuario, 1)

    def test_obtener_usuarios_envia_solicitud_correcta(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: [{'id': 1}, {'id': 2}, {'id': 3}]

        self.auth_server.obtener_usuarios({1, 2, 3})

        self.mock_get.assert_called_with('/usuario', params={'ids': '1,2,3', 'cantidad': 3})

    def test_obtener_usuarios_devuelve_datos_recibidos(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: [{'id': 123}, {'id': 124}]

        data = self.auth_server.obtener_usuarios({123, 124})

        self.assertDictEqual({123: {'id': 123}, 124: {'id': 124}}, data)

    def test_obtener_usuarios_devuelve_diccionario_vacio_si_no_hay_datos(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: []

        self.assertDictEqual({}, self.auth_server.obtener_usuarios({1, 2, 3}))

    def test_obtener_usuarios_lanza_excepcion_en_error(self):
        self.mock_get.return_value.status_code = 500
        self.mock_get.return_value.json = lambda: None

        self.assertRaises(AuthServerError, self.auth_server.obtener_usuarios, {1, 2, 3})

    def test_actualizar_clave_envia_solicitud_correcta(self):
        self.mock_put.return_value.status_code = 200
        self.mock_put.return_value.json = lambda: {}

        uid = 1
        self.auth_server.actualizar_clave(uid, 'nueva-clave')

        self.mock_put.assert_called_with(f"/usuario/{uid}/clave",
                                         json={'password': 'nueva-clave'})

    def test_actualizar_clave_devuelve_true_en_exito(self):
        self.mock_put.return_value.status_code = 200
        self.mock_put.return_value.json = lambda: {}

        self.assertTrue(self.auth_server.actualizar_clave(1, 'nueva-clave'))

    def test_actualizar_clave_devuelve_false_en_400(self):
        self.mock_put.return_value.status_code = 400
        self.mock_put.return_value.json = lambda: {}

        self.assertFalse(self.auth_server.actualizar_clave(1, ''))

    def test_actualizar_clave_lanza_excepcion_en_error(self):
        self.mock_put.return_value.status_code = 500
        self.mock_put.return_value.json = lambda: {}

        self.assertRaises(AuthServerError,
                          self.auth_server.actualizar_clave,
                          1,
                          'nueva-clave')

    def test_actualizar_clave_lanza_excepcion_en_404(self):
        self.mock_put.return_value.status_code = 404
        self.mock_put.return_value.json = lambda: {}

        self.assertRaises(AuthServerError,
                          self.auth_server.actualizar_clave,
                          1,
                          'nueva-clave')

    def test_actualizar_usuario_envia_solicitud_correcta(self):
        self.mock_put.return_value.status_code = 200
        self.mock_put.return_value.json = lambda: {}

        uid = 1
        self.auth_server.actualizar_usuario(uid, {'nombre': 'Lucho'})

        self.mock_put.assert_called_with(f"/usuario/{uid}", json={'nombre': 'Lucho'})

    def test_actualizar_usuario_devuelve_true_en_exito(self):
        self.mock_put.return_value.status_code = 200
        self.mock_put.return_value.json = lambda: {}

        self.assertTrue(self.auth_server.actualizar_usuario(1, {'nombre': 'Lucho'}))

    def test_actualizar_usuario_devuelve_false_en_404(self):
        self.mock_put.return_value.status_code = 404
        self.mock_put.return_value.json = lambda: {}

        self.assertFalse(self.auth_server.actualizar_usuario(1, {'nombre': 'Lucho'}))

    def test_actualizar_usuario_lanza_excepcion_en_error(self):
        self.mock_put.return_value.status_code = 500
        self.mock_put.return_value.json = lambda: {}

        self.assertRaises(AuthServerError,
                          self.auth_server.actualizar_usuario,
                          1,
                          {'nombre': 'Lucho'})

    def test_actualizar_usuario_lanza_excepcion_en_campos_desconocidos(self):
        self.mock_put.return_value.status_code = 200
        self.mock_put.return_value.json = lambda: {}

        self.assertRaises(ValueError,
                          self.auth_server.actualizar_usuario,
                          1,
                          {'campo-desconocido': 'valor'})
        self.mock_put.assert_not_called()

    def test_limpiar_base_de_datos_envia_solicitud_correcta(self):
        self.mock_delete.return_value.status_code = 200

        self.auth_server.limpiar_base_de_datos()

        self.mock_delete.assert_called_with("/base_de_datos")

    def test_limpiar_base_de_datos_devuelve_true_en_exito(self):
        self.mock_delete.return_value.status_code = 200

        self.assertTrue(self.auth_server.limpiar_base_de_datos())

    def test_limpiar_base_de_datos_devuelve_false_en_error(self):
        self.mock_delete.return_value.status_code = 500

        self.assertFalse(self.auth_server.limpiar_base_de_datos())

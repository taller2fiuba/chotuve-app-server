import unittest
import mock

from tests.base import LoginMockTestCase
from app.models.solicitud_contacto import SolicitudContacto
from app.models.contacto import Contacto

class SolicitudContactoTestCase(LoginMockTestCase):
    @mock.patch('auth_server_api.obtener_usuarios')
    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_solicitudes_pendientes')
    def test_get_mis_solicitudes_devuelve_vacio_sin_solicitudes(self, mock_sol, mock_auth):
        mock_auth.return_value.json = lambda: []
        mock_auth.return_value.status_code = 200
        mock_sol.return_value = []
        response = self.app.get('/usuario/solicitud-contacto')

        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json)

    @mock.patch('auth_server_api.obtener_usuarios')
    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_solicitudes_pendientes')
    def test_get_mis_solicitudes_forwardea_mala_respuesta_del_auth(self, mock_sol, mock_auth):
        mock_auth.return_value.json = lambda: {}
        mock_auth.return_value.status_code = 500
        mock_sol.return_value = [
            SolicitudContacto(id=1, usuario_emisor=1, usuario_receptor=2)
        ]
        response = self.app.get('/usuario/solicitud-contacto')

        self.assertEqual(response.status_code, 500)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.obtener_usuarios')
    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_solicitudes_pendientes')
    def test_get_mis_solicitudes_devuelve_solicitudes(self, mock_sol, mock_auth):
        mock_auth.return_value.json = lambda: [
            {'id': 2, 'email': 'test-2@test.com'},
            {'id': 3, 'email': 'test-3@test.com'},
        ]
        mock_auth.return_value.status_code = 200
        mock_sol.return_value = [
            SolicitudContacto(id=10, usuario_emisor=2, usuario_receptor=1),
            SolicitudContacto(id=11, usuario_emisor=3, usuario_receptor=1),
        ]
        response = self.app.get('/usuario/solicitud-contacto')

        self.assertEqual(200, response.status_code)
        self.assertEqual([
            {'id': 10, 'usuario_id': 2, 'email': 'test-2@test.com'},
            {'id': 11, 'usuario_id': 3, 'email': 'test-3@test.com'},
        ], response.json)

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.hay_solicitud')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    @mock.patch('app.db.session')
    def test_crear_solicitud_devuelve_201(self, db_session, es_contacto, hay_solicitud):
        es_contacto.return_value = False
        hay_solicitud.return_value = False

        response = self.app.post('/usuario/solicitud-contacto', json={
            'usuario_id': 2
        })

        self.assertEqual(201, response.status_code)
        self.assertEqual({}, response.json)
        db_session.add.assert_called_with(SolicitudContacto(usuario_emisor=1,
                                                            usuario_receptor=2))
        db_session.commit.assert_called_once()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.hay_solicitud')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    @mock.patch('app.db.session')
    def test_crear_solicitud_sin_data_devuelve_400(self, db_session, es_contacto, hay_solicitud):
        response = self.app.post('/usuario/solicitud-contacto', json={})
        self.assertEqual(400, response.status_code)
        es_contacto.assert_not_called()
        hay_solicitud.assert_not_called()
        db_session.add.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.hay_solicitud')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    @mock.patch('app.db.session')
    def test_crear_solicitud_a_mi_mismo_devuelve_400(self, db_session, es_contacto, hay_solicitud):
        es_contacto.return_value = False
        hay_solicitud.return_value = False

        response = self.app.post('/usuario/solicitud-contacto', json={
            'usuario_id': 1
        })

        self.assertEqual(400, response.status_code)
        db_session.add.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.hay_solicitud')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    @mock.patch('app.db.session')
    def test_crear_solicitud_si_ya_envie_devuelve_400(self, db_session, es_contacto, hay_solicitud):
        es_contacto.return_value = False
        # hay solicitud de emisor a receptor, con emisor = yo
        hay_solicitud.side_effect = lambda emisor, receptor: emisor == 1

        response = self.app.post('/usuario/solicitud-contacto', json={
            'usuario_id': 2
        })

        self.assertEqual(400, response.status_code)
        db_session.add.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.hay_solicitud')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    @mock.patch('app.db.session')
    def test_crear_solicitud_si_hay_pendiente_devuelve_400(self, db_session, es_contacto, hay_sol):
        es_contacto.return_value = False
        # hay solicitud de emisor a receptor, con receptor = yo
        hay_sol.side_effect = lambda emisor, receptor: receptor == 1

        response = self.app.post('/usuario/solicitud-contacto', json={
            'usuario_id': 2
        })

        self.assertEqual(400, response.status_code)
        db_session.add.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.hay_solicitud')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    @mock.patch('app.db.session')
    def test_crear_solicitud_si_es_contacto_devuelve_400(self, db_session, es_contacto, hay_sol):
        es_contacto.return_value = True
        hay_sol.return_value = False

        response = self.app.post('/usuario/solicitud-contacto', json={
            'usuario_id': 2
        })

        self.assertEqual(400, response.status_code)
        db_session.add.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_aceptar_solicitud_correcta_devuelve_200(self, db_session, obtener_sol_por_id):
        solicitud = SolicitudContacto(id=1,
                                      usuario_emisor=2,
                                      usuario_receptor=1)
        obtener_sol_por_id.return_value = solicitud

        response = self.app.put('/usuario/solicitud-contacto/1', json={
            'accion': 'aceptar'
        })

        self.assertEqual(200, response.status_code)
        db_session.add.assert_called_with(Contacto(usuario_1=2, usuario_2=1))
        db_session.delete.assert_called_with(solicitud)
        db_session.commit.assert_called_once()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_rechazar_solicitud_correcta_devuelve_200(self, db_session, obtener_sol_por_id):
        solicitud = SolicitudContacto(id=1,
                                      usuario_emisor=2,
                                      usuario_receptor=1)
        obtener_sol_por_id.return_value = solicitud

        response = self.app.put('/usuario/solicitud-contacto/1', json={
            'accion': 'rechazar'
        })

        self.assertEqual(200, response.status_code)
        db_session.add.assert_not_called()
        db_session.delete.assert_called_with(solicitud)
        db_session.commit.assert_called_once()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_aceptar_solicitud_accion_invalida_devuelve_400(self, db_session, obtener_sol_por_id):
        solicitud = SolicitudContacto(id=1,
                                      usuario_emisor=2,
                                      usuario_receptor=1)
        obtener_sol_por_id.return_value = solicitud

        response = self.app.put('/usuario/solicitud-contacto/1', json={
            'accion': 'accion-invalida'
        })

        self.assertEqual(400, response.status_code)
        db_session.add.assert_not_called()
        db_session.delete.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_aceptar_solicitud_inexistente_devuelve_400(self, db_session, obtener_sol_por_id):
        obtener_sol_por_id.return_value = None

        response = self.app.put('/usuario/solicitud-contacto/1', json={
            'accion': 'aceptar'
        })

        self.assertEqual(404, response.status_code)
        db_session.add.assert_not_called()
        db_session.delete.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_aceptar_solicitud_que_no_es_mia_devuelve_404(self, db_session, obtener_sol_por_id):
        solicitud = SolicitudContacto(id=1,
                                      usuario_emisor=20,
                                      usuario_receptor=30)
        obtener_sol_por_id.return_value = solicitud

        response = self.app.put('/usuario/solicitud-contacto/1', json={
            'accion': 'aceptar'
        })

        self.assertEqual(404, response.status_code)
        db_session.add.assert_not_called()
        db_session.delete.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_eliminar_solicitud_enviada_devuelve_200(self, db_session, obtener_sol_por_id):
        solicitud = SolicitudContacto(id=1,
                                      usuario_emisor=1,
                                      usuario_receptor=2)
        obtener_sol_por_id.return_value = solicitud

        response = self.app.delete('/usuario/solicitud-contacto/1')

        self.assertEqual(200, response.status_code)
        db_session.delete.assert_called_with(solicitud)
        db_session.commit.assert_called_once()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_eliminar_solicitud_inexistente_devuelve_404(self, db_session, obtener_sol_por_id):
        obtener_sol_por_id.return_value = None

        response = self.app.delete('/usuario/solicitud-contacto/1')

        self.assertEqual(404, response.status_code)
        db_session.delete.assert_not_called()
        db_session.commit.assert_not_called()

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.obtener_por_id')
    @mock.patch('app.db.session')
    def test_eliminar_solicitud_que_no_es_mia_devuelve_404(self, db_session, obtener_sol_por_id):
        solicitud = SolicitudContacto(id=1,
                                      usuario_emisor=20,
                                      usuario_receptor=30)
        obtener_sol_por_id.return_value = solicitud

        response = self.app.delete('/usuario/solicitud-contacto/1')

        self.assertEqual(404, response.status_code)
        db_session.delete.assert_not_called()
        db_session.commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()

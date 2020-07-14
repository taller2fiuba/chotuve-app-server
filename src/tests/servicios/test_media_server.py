from tests.servicios.mock_cliente_http import MockClienteHttpTestCase
from app.servicios.servicio_media_server import MediaServer, MediaServerError

class MediaServerTestCase(MockClienteHttpTestCase):
    def setUp(self):
        super().setUp()
        self.media_server = MediaServer('http://localhost')

    def test_obtener_video_envia_solicitud_correcta(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'id': 'asd', 'duracion': 120}

        video_id = 'asd'
        self.media_server.obtener_video(video_id)

        self.mock_get.assert_called_with(f"/video/{video_id}")

    def test_obtener_video_devuelve_data_de_usuario_en_exito(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'id': 'asd', 'duracion': 120}

        video_id = 'asd'
        data = self.media_server.obtener_video(video_id)

        self.assertEqual(data, {'id': 'asd', 'duracion': 120})

    def test_obtener_video_devuelve_none_en_404(self):
        self.mock_get.return_value.status_code = 404
        self.mock_get.return_value.json = lambda: {}

        video_id = 'asd'
        data = self.media_server.obtener_video(video_id)

        self.assertIsNone(data)

    def test_obtener_video_lanza_excepcion_en_error(self):
        self.mock_get.return_value.status_code = 500
        self.mock_get.return_value.json = lambda: {}

        self.assertRaises(MediaServerError, self.media_server.obtener_video, 'asd')

    def test_obtener_videos_envia_solicitud_correcta(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: [{'id': 'a1'}, {'id': 'a2'}, {'id': 'a3'}]

        self.media_server.obtener_videos()

        self.mock_get.assert_called_with('/video', params={'offset': 0, 'cantidad': 10})

    def test_obtener_videos_envia_solicitud_correcta_con_offset_y_cantidad(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: [{'id': 'a1'}, {'id': 'a2'}, {'id': 'a3'}]

        self.media_server.obtener_videos(offset=4, cantidad=7)

        self.mock_get.assert_called_with('/video', params={'offset': 4, 'cantidad': 7})

    def test_obtener_videos_devuelve_datos_recibidos(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: [{'id': 'a1'}, {'id': 'a2'}, {'id': 'a3'}]

        data = self.media_server.obtener_videos()

        self.assertListEqual([{'id': 'a1'}, {'id': 'a2'}, {'id': 'a3'}], data)

    def test_obtener_videos_devuelve_diccionario_vacio_si_no_hay_datos(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: []

        self.assertListEqual([], self.media_server.obtener_videos())

    def test_obtener_videos_lanza_excepcion_en_error(self):
        self.mock_get.return_value.status_code = 500
        self.mock_get.return_value.json = lambda: None

        self.assertRaises(MediaServerError, self.media_server.obtener_videos)

    def test_subir_video_envia_solicitud_correcta(self):
        self.mock_post.return_value.status_code = 201
        self.mock_post.return_value.json = lambda: {}

        self.media_server.subir_video({'titulo': 'Lucho'})

        self.mock_post.assert_called_with(f"/video", json={'titulo': 'Lucho'})

    def test_subir_video_lanza_excepcion_en_bad_request(self):
        self.mock_post.return_value.status_code = 400
        self.mock_post.return_value.json = lambda: {}

        self.assertRaises(MediaServerError,
                          self.media_server.subir_video,
                          {'titulo': 'Lucho'})

    def test_subir_video_lanza_excepcion_en_error(self):
        self.mock_post.return_value.status_code = 500
        self.mock_post.return_value.json = lambda: {}

        self.assertRaises(MediaServerError,
                          self.media_server.subir_video,
                          {'titulo': 'Lucho'})

    def test_limpiar_base_de_datos_envia_solicitud_correcta(self):
        self.mock_delete.return_value.status_code = 200

        self.media_server.limpiar_base_de_datos()

        self.mock_delete.assert_called_with("/base_de_datos")

    def test_limpiar_base_de_datos_devuelve_true_en_exito(self):
        self.mock_delete.return_value.status_code = 200

        self.assertTrue(self.media_server.limpiar_base_de_datos())

    def test_limpiar_base_de_datos_devuelve_false_en_error(self):
        self.mock_delete.return_value.status_code = 500

        self.assertFalse(self.media_server.limpiar_base_de_datos())

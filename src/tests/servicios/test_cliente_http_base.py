from unittest import TestCase
from mock import patch

from app.servicios.cliente_http_base import ClienteHttpBase

# pylint: disable=protected-access
class ClienteHttpBaseTestCase(TestCase):
    def setUp(self):
        patchers = [
            patch('requests.get'),
            patch('requests.post'),
            patch('requests.put'),
            patch('requests.delete')
        ]

        for patcher in patchers:
            self.addCleanup(patcher.stop)

        self.mock_get = patchers[0].start()
        self.mock_post = patchers[1].start()
        self.mock_put = patchers[2].start()
        self.mock_delete = patchers[3].start()

    def test_get_ignora_barra_final_url(self):
        cliente = ClienteHttpBase('http://localhost/')

        cliente._get('/test')

        self.mock_get.assert_called_with('http://localhost/test',
                                         headers=None,
                                         params=None,
                                         json=None)

    def test_get_con_token_envia_token(self):
        cliente = ClienteHttpBase('http://localhost/', 'app-server-token')

        cliente._get('/test')

        self.mock_get.assert_called_with('http://localhost/test',
                                         headers={'X-APP-SERVER-TOKEN': 'app-server-token'},
                                         params=None,
                                         json=None)

    def test_get_sin_token_no_envia_encabezado(self):
        cliente = ClienteHttpBase('http://localhost')

        cliente._get('/test')

        self.mock_get.assert_called_with('http://localhost/test',
                                         headers=None,
                                         params=None,
                                         json=None)

    def test_get_envia_query_params(self):
        cliente = ClienteHttpBase('http://localhost')

        cliente._get('/test', params={'offset': 4, 'cantidad': 7})

        self.mock_get.assert_called_with('http://localhost/test',
                                         headers=None,
                                         params={'offset': 4, 'cantidad': 7},
                                         json=None)

    def test_post_ignora_barra_final_url(self):
        cliente = ClienteHttpBase('http://localhost/')

        cliente._post('/test', {'data': 'post-data'})

        self.mock_post.assert_called_with('http://localhost/test',
                                          headers=None,
                                          params=None,
                                          json={'data': 'post-data'})

    def test_post_con_token_envia_token(self):
        cliente = ClienteHttpBase('http://localhost/', 'app-server-token')

        cliente._post('/test', {'data': 'post-data'})

        self.mock_post.assert_called_with('http://localhost/test',
                                          headers={'X-APP-SERVER-TOKEN': 'app-server-token'},
                                          params=None,
                                          json={'data': 'post-data'})

    def test_post_sin_token_no_envia_encabezado(self):
        cliente = ClienteHttpBase('http://localhost')

        cliente._post('/test', {'data': 'post-data'})

        self.mock_post.assert_called_with('http://localhost/test',
                                          headers=None,
                                          params=None,
                                          json={'data': 'post-data'})

    def test_post_envia_query_params(self):
        cliente = ClienteHttpBase('http://localhost')

        cliente._post('/test', {'data': 'post-data'}, params={'offset': 4, 'cantidad': 7})

        self.mock_post.assert_called_with('http://localhost/test',
                                          headers=None,
                                          params={'offset': 4, 'cantidad': 7},
                                          json={'data': 'post-data'})

    def test_put_ignora_barra_final_url(self):
        cliente = ClienteHttpBase('http://localhost/')

        cliente._put('/test', {'data': 'post-data'})

        self.mock_put.assert_called_with('http://localhost/test',
                                         headers=None,
                                         params=None,
                                         json={'data': 'post-data'})

    def test_put_con_token_envia_token(self):
        cliente = ClienteHttpBase('http://localhost/', 'app-server-token')

        cliente._put('/test', {'data': 'post-data'})

        self.mock_put.assert_called_with('http://localhost/test',
                                         headers={'X-APP-SERVER-TOKEN': 'app-server-token'},
                                         params=None,
                                         json={'data': 'post-data'})

    def test_put_sin_token_no_envia_encabezado(self):
        cliente = ClienteHttpBase('http://localhost')

        cliente._put('/test', {'data': 'post-data'})

        self.mock_put.assert_called_with('http://localhost/test',
                                         headers=None,
                                         params=None,
                                         json={'data': 'post-data'})

    def test_put_envia_query_params(self):
        cliente = ClienteHttpBase('http://localhost')

        cliente._put('/test', {'data': 'post-data'}, params={'offset': 4, 'cantidad': 7})

        self.mock_put.assert_called_with('http://localhost/test',
                                         headers=None,
                                         params={'offset': 4, 'cantidad': 7},
                                         json={'data': 'post-data'})

    def test_delete_ignora_barra_final_url(self):
        cliente = ClienteHttpBase('http://localhost/')

        cliente._delete('/test')

        self.mock_delete.assert_called_with('http://localhost/test',
                                            headers=None,
                                            params=None,
                                            json=None)

    def test_delete_con_token_envia_token(self):
        cliente = ClienteHttpBase('http://localhost/', 'app-server-token')

        cliente._delete('/test')

        self.mock_delete.assert_called_with('http://localhost/test',
                                            headers={'X-APP-SERVER-TOKEN': 'app-server-token'},
                                            params=None,
                                            json=None)

    def test_delete_sin_token_no_envia_encabezado(self):
        cliente = ClienteHttpBase('http://localhost')

        cliente._delete('/test')

        self.mock_delete.assert_called_with('http://localhost/test',
                                            headers=None,
                                            params=None,
                                            json=None)

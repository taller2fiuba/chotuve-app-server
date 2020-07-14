from unittest import TestCase
from mock import patch

class MockClienteHttpTestCase(TestCase):
    def setUp(self):
        patcher_get = patch('app.servicios.cliente_http_base.ClienteHttpBase._get')
        self.mock_get = patcher_get.start()
        self.addCleanup(patcher_get.stop)

        patcher_post = patch('app.servicios.cliente_http_base.ClienteHttpBase._post')
        self.mock_post = patcher_post.start()
        self.addCleanup(patcher_post.stop)

        patcher_put = patch('app.servicios.cliente_http_base.ClienteHttpBase._put')
        self.mock_put = patcher_put.start()
        self.addCleanup(patcher_put.stop)

        patcher_delete = patch('app.servicios.cliente_http_base.ClienteHttpBase._delete')
        self.mock_delete = patcher_delete.start()
        self.addCleanup(patcher_delete.stop)

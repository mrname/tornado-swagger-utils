import json
import os

from swagnado.handlers import SwaggerJSONRequestHandler
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Swagger data pulled from:
# https://raw.githubusercontent.com/Yelp/bravado-core/master/test-data/2.0/petstore/swagger.json
SWAGGER_PATH = os.path.join(BASE_DIR, 'data', 'swagger.json')
with open(SWAGGER_PATH, 'r') as fp:
    SWAGGER_DATA = json.load(fp)

BASE_SWAGGER_ROUTE = '/v2/pet'
RESOURCE_ROUTE = '/v2/pet/(?P<pet_id>[^/]+)'

class BasicHandler(SwaggerJSONRequestHandler):

    _swagger_data = SWAGGER_DATA

    def get(self):
        pass

    def post(self):
        pass

class TestBase(AsyncHTTPTestCase):

    def get_app(self):
        return Application(self.get_handlers())

class TestInputValidation(TestBase):

    def get_handlers(self):
        return [(BASE_SWAGGER_ROUTE, BasicHandler)]

    def TestInvalidPOST(self):
        response = self.fetch(BASE_SWAGGER_ROUTE, method='POST',
                              body='{"test":1}')
        body_str = response.body.decode()
        self.assertEqual(response.code, 400)
        self.assertIn('missing required params', body_str)

        # Missing one key required by the schema
        test_data = {'name': 'heman'}
        response = self.fetch(BASE_SWAGGER_ROUTE, method='POST',
                              body=json.dumps(test_data))
        body_str = response.body.decode()
        self.assertEqual(response.code, 400)
        self.assertIn('\'photoUrls\' is a required property', body_str)

        # Both required keys but bad value type.
        test_data['photoUrls'] = [1]
        response = self.fetch(BASE_SWAGGER_ROUTE, method='POST',
                              body=json.dumps(test_data))
        body_str = response.body.decode()
        self.assertEqual(response.code, 400)
        self.assertIn('1 is not of type \'string\'', body_str)

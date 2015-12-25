from bravado_core.param import get_param_type_spec
from bravado_core.spec import Spec
from bravado_core.validate import validate_schema_object
from jsonschema.exceptions import ValidationError
from tornado.escape import json_decode
from tornado.web import RequestHandler

from .exceptions import MissingSpecError


class SwaggerJSONRequestHandler(RequestHandler):
    """
    Base Tornado handler with capabilities for validating input/output
    of data based on the provided Swagger spec.
    """

    def __init__(self, application, request, **kwargs):
        """
        :param swagger_data: Swagger specification
        :type swagger_spec: dict
        :param swagger_url: URL of Swagger specification
        :type swagger_spec: string
        :param swagger_config: Configuration dict. See CONFIG_DEFAULTS here::
        https://github.com/Yelp/bravado-core/blob/master/bravado_core/spec.py.
        :type swagger_config: dict
        """
        swagger_data = getattr(self, '_swagger_data', None)
        swagger_url = getattr(self, '_swagger_url', None)
        swagger_config = getattr(self, 'swagger_config', None)
        if not swagger_data and not swagger_url:
            raise ValueError(
                'self._swagger_data or self._swagger_url must be defined')
        if swagger_data:
            self.swagger_spec = Spec.from_dict(swagger_data,
                                               config=swagger_config)
        elif swagger_url:
            self.swagger_spec = Spec.from_url(swagger_url,
                                              config=swagger_config)
        super().__init__(application, request, **kwargs)

    def prepare(self):
        self.post_data = json_decode(self.request.body)
        self._prepare()
        self.swagger_validate_input()

    def _prepare(self):
        pass

    def send_error(self, exception):
        """
        Sends reasonable error JSON
        """
        print(dir(exception))
        print(str(exception))

    def swagger_validate_input(self):
        """
        Validates input parameters using the supplied swagger spec

        :raises: jsonschema.exceptions.ValidationError if input does not match
        :raises: MissingSpecError if the spec for a given resource (a specific
        URL and HTTP method) does not exist
        schema
        """
        # Convert the URI to match Swagger syntax. If our swagger spec has an
        # endpoint like /stuff/{thing_id}, and we received a request for
        # /stuff/123, we need to convert it back to /stuff/{thing_id} so that we
        # can reference the swagger definition. self.path_kwargs holds this map
        converted_uri = self.request.uri
        for key, value in self.path_kwargs.items():
            target = '{{{0}}}'.format(key)
            converted_uri = converted_uri.replace(value, target)
        # Retrieve swagger spec for the particular resource
        request_spec = self.swagger_spec.get_op_for_request(
            self.request.method, converted_uri)
        if request_spec is None:
            raise MissingSpecError(
                'No swagger spec found for {0} on {1}'.format(
                    self.request.method, converted_uri)
            )

        # Verify each param required by the schema
        for param in request_spec.params.values():
            param_spec = get_param_type_spec(param)
            if param.location == 'body':
                param_value = self.post_data
            elif param.location == 'path':
                param_value = self.path_kwargs.get(param.name)

            try:
                validate_schema_object(self.swagger_spec, param_spec,
                                       param_value)
            except ValidationError as e:
                self.send_error(e)

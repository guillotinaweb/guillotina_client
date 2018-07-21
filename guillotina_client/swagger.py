import json


class EndpointsDoNotExist(Exception):
    pass


class EndpointObject:
    """Abstract respresentation of and Endpoint Swagger representation
    """
    def __init__(self, endpoint_json, path_endpoint):
        self._path = path_endpoint
        self.endpoint_json = endpoint_json
        self._methods = []

    def __repr__(self):
        return str(self.summary)

    @property
    def methods(self):
        self._methods = []
        for method in self.endpoint_json.keys():
            self._methods.append(method)
        return self._methods

    @property
    def responses(self):
        responses = {}
        for method in self.methods:
            responses[method] = self.endpoint_json.get(method).get('responses')
        return responses

    @property
    def summary(self):
        summary = {}
        for method in self.methods:
            summary[method] = self.endpoint_json.get(method).get('summary')
        return summary

    @property
    def parameters(self):
        parameters = {}
        for method in self.methods:
            parameters[method] = self.endpoint_json.get(method).get('parameters')
        return parameters

    @property
    def endpoint(self):
        is_endpoint = False
        list_path = self._path.split('/')
        for name_endpoint in list_path:
            if '@' in name_endpoint:
                is_endpoint = True
                return name_endpoint
        if not is_endpoint:
            return self.path

    @property
    def path(self):
        return self._path


class EndpointProducer:
    """Given a swagger json response, yields EndpointObject instances
    """
    def __init__(self, swagger_response):
        if isinstance(swagger_response, str):
            self.swagger_response = json.loads(swagger_response)
        elif isinstance(swagger_response, dict):
            self.swagger_response = swagger_response
        else:
            raise Exception("Bad swagger type")

    @property
    def path(self):
        """Guillotina swagger response contains path key where all endpoints
        are defined as a json
        """
        endpoints = self.swagger_response.get('paths')
        if endpoints:
            return endpoints
        else:
            raise EndpointsDoNotExist

    def endpoint_generator(self):
        """
        Generator that yield EndpointObject instances
        """
        try:
            endpoints = self.path
            for path_endpoint in endpoints.keys():
                yield EndpointObject(endpoints[path_endpoint], path_endpoint)
        except EndpointsDoNotExist:
            raise Exception('Object without endpoint')
        except Exception as e:
            raise e

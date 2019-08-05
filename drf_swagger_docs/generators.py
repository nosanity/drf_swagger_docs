from drf_yasg import openapi
from rest_framework.settings import api_settings
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.openapi import ReferenceResolver
from drf_yasg.utils import get_consumes, get_produces
from .utils import requires_authentication, generate_security_definitions, get_security_for_operation


class SchemaGenerator(OpenAPISchemaGenerator):
    """
    Измененный класс OpenAPISchemaGenerator, добавляющий securityDefinitions и дополнтельный
    параметр swaggerInnerApi для внутренних ручек апи
    """
    def get_security_definitions(self, endpoints):
        perm_classes = set()
        auth_classes = set()
        for url, (cls, methods) in endpoints.items():
            permissions = cls.permission_classes
            perm_classes |= set(permissions)
            if requires_authentication(permissions):
                auth_classes |= set(cls.authentication_classes)
        return generate_security_definitions(perm_classes, auth_classes)

    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object representing the API schema.

        :param request: the request used for filtering accessible endpoints and finding the spec URI
        :type request: rest_framework.request.Request or None
        :param bool public: if True, all endpoints are included regardless of access through `request`

        :return: the generated Swagger specification
        :rtype: openapi.Swagger
        """
        endpoints = self.get_endpoints(request)
        components = ReferenceResolver(openapi.SCHEMA_DEFINITIONS, force_init=True)
        self.consumes = get_consumes(api_settings.DEFAULT_PARSER_CLASSES)
        self.produces = get_produces(api_settings.DEFAULT_RENDERER_CLASSES)
        paths, prefix = self.get_paths(endpoints, components, request, public)

        security_definitions = self.get_security_definitions(endpoints)
        security_requirements = []

        url = self.url
        if url is None and request is not None:
            url = request.build_absolute_uri()

        return openapi.Swagger(
            info=self.info, paths=paths, consumes=self.consumes or None, produces=self.produces or None,
            security_definitions=security_definitions, security=security_requirements,
            _url=url, _prefix=prefix, _version=self.version, **dict(components)
        )

    def get_operation(self, view, path, prefix, method, components, request):
        op = super().get_operation(view, path, prefix, method, components, request)
        op['security'] = get_security_for_operation(view, method)
        return op

    def get_path_item(self, path, view_cls, operations):
        path = super().get_path_item(path, view_cls, operations)
        path['swaggerInnerApi'] = getattr(view_cls, '_swagger_inner_api', False)
        return path

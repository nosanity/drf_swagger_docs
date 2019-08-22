import hashlib
from django.forms.models import ALL_FIELDS
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoObjectPermissions
from .permissions import SwaggerBasePermission


REQUIRE_AUTH = {IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoObjectPermissions}


def requires_authentication(perm_classes):
    """
    требуется ли авторизация для доступа к ручке исходя из ее permission_classes
    """
    if set(perm_classes) & REQUIRE_AUTH:
        return True
    for cls in perm_classes:
        if issubclass(cls, SwaggerBasePermission) and cls._require_authentication:
            return True
    return False


def generate_security_definitions(perm_classes, auth_classes):
    definitions = {}
    for perm in perm_classes:
        definition = get_security_definition(perm)
        if definition:
            definitions[get_security_definition_name(perm)] = definition
    auth = get_auth_security_definition(auth_classes)
    if auth:
        definitions['__auth__'] = auth
    return definitions


def get_security_definition(cls):
    if issubclass(cls, SwaggerBasePermission):
        return cls._swagger_security_definition


def get_auth_security_definition(classes):
    auth = list(filter(lambda x: issubclass(x, BaseAuthentication) and x is not SessionAuthentication, classes))
    if auth:
        # т.к. спецификация swagger 2.0 не дает возможности указать авторизацию более подробно, нежели как просто
        # через apiKey или query, то, если в authentication_classes есть что-то помимо SessionAuthentication, такого
        # обозначения будет достаточно
        return {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }


def get_security_definition_name(cls):
    return getattr(cls, '_swagger_definition_name', None) or hashlib.md5(cls.__name__.encode('utf8')).hexdigest()


def permission_applies_for_method(perm, method):
    if issubclass(perm, SwaggerBasePermission):
        if perm.exclude_methods is not None and method in perm.exclude_methods:
            return False
        if perm.methods and (method in perm.methods or perm.methods == ALL_FIELDS):
            return True
        return False
    return True


def get_security_for_operation(view, method):
    perm_classes, auth_classes = view.permission_classes, view.authentication_classes
    security_keys = []
    for perm in perm_classes:
        definition = get_security_definition(perm)
        apply = permission_applies_for_method(perm, method)
        if definition and apply:
            security_keys.append(get_security_definition_name(perm))
        if apply and requires_authentication((perm,)):
            definition = get_auth_security_definition(auth_classes)
            if definition:
                security_keys.append('__auth__')
    return [{key: []} for key in set(security_keys)]

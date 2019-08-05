from django.forms.models import ALL_FIELDS


class SwaggerBasePermission:
    """
    Миксин для указания  securityDefinitions
    """
    _require_authentication = False
    _swagger_security_definition = None
    _swagger_definition_name = None
    methods = ALL_FIELDS
    exclude_methods = None

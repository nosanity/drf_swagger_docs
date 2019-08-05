from drf_yasg.app_settings import swagger_settings
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view as get_schema_view_base
from rest_framework.permissions import AllowAny
from .generators import SchemaGenerator


def get_schema_view(info=None, url=None, patterns=None, urlconf=None, public=None, validators=None,
                    generator_class=None, authentication_classes=None, permission_classes=None):
    if info is None:
        default_info = swagger_settings.DEFAULT_INFO or {}
        if isinstance(default_info, dict):
            default_info = default_info.copy()
            default_info.setdefault('title', 'api')
            default_info.setdefault('default_version', '1')
            info = Info(**default_info)
    return get_schema_view_base(
        info=info,
        url=url,
        patterns=patterns,
        urlconf=urlconf,
        public=True if public is None else public,
        validators=validators,
        generator_class=generator_class or SchemaGenerator,
        authentication_classes=authentication_classes if authentication_classes is not None else (),
        permission_classes=permission_classes if permission_classes is not None else (AllowAny, )
    )

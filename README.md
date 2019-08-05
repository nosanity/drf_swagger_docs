## Установка

    pip install git+https://github.com/nosanity/drf_swagger_docs/
    
Добавить в файл urls.py

    from django.conf.urls import url
    from drf_swagger_docs.views import get_schema_view
    
    urlpatterns = [
        ...
        url(r'^api/swagger(?P<format>\.json)$', get_schema_view().without_ui(cache_timeout=0)),
    ]
    
## Использование

### Указание securityDefinitions для класса rest_framework.permissions.BasePermission

    from rest_framework.permissions import BasePermission
    from drf_swagger_docs.permissions import SwaggerBasePermission
    
    
    class CustomPermission(SwaggerBasePermission, BasePermission):
        # требует ли этот permission, чтобы пользователь был авторизован
        # если да, то надо будет указать authentication_classes во вьюхе, используемой
        # с этим permission
        _require_authentication = True
        # описание securityDefinition в корректном для swagger формате
        _swagger_security_definition = {
            'type': 'apiKey',
            'name': 'x-api-key',
            'in': 'header',
        }
        # необязательный, но желательный параметр
        _swagger_definition_name = 'api_key'
        # методы запроса, к которым permission не будет применяться
        exclude_methods = ['GET', 'OPTIONS']
        
        def has_permission(self, request, view):
            if request.user and request.user.is_authenticated:
                if request.method not in self.exclude_methods:
                    # check something
                    ...
                return True
            return False
            
### Исключение ручки из общедоступного отображения в документации

    from rest_framework.views import APIView
    
    class SomeView(APIView):
        _swagger_inner_api = True
        ...

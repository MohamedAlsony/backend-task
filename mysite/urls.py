from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import permissions


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

schema_view = get_schema_view(
   openapi.Info(
      title="loan system API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,  # Here,
    authentication_classes=[SessionAuthentication, TokenAuthentication],
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/borrower/', include('borrower.urls', 'borrower_api')),
    path('api/account/', include('account.urls', 'account_api')),

    path('api/investor/', include('investor.urls', 'investor_api')),
    path('api/loan/', include('loan.urls', 'loan_api')),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

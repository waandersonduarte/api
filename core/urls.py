from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from desafio.views import *

router = routers.DefaultRouter()
router.register('mulheres_mereen', MulheresDeMereenViewSet, basename='mulheres_mereen')
router.register('lista_pessoas', ListaDePessoasViewSet, basename='lista_pessoas') 

urlpatterns = [
    path('', include('desafio.urls')),
    path('admin/', admin.site.urls),
    path('desafio/', include(router.urls), name='desafio'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT,
    )

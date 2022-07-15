from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #abdel
    # path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  #   path('api-auth/', include('rest_framework.urls')),

    path('admin/', admin.site.urls),
    path('' , include("quiz.urls")),
        
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)

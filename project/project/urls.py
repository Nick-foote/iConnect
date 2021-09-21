from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


PREFIX_API = 'api/v1/'

api_patterns = [
    path(f'', include('users.urls')),
    path(f'', include('playlists.urls')),
    path(f'social-auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path(f'social/', include('social_django.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{PREFIX_API}', include(api_patterns)),
]

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)
    
    urlpatterns += [ 
        path('api/schema', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/swagger/ui', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ]

    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    )

    import debug_toolbar
    urlpatterns += [            
        path('__debug__/', include(debug_toolbar.urls)),
    ]

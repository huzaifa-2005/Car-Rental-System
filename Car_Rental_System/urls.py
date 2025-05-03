from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings.py from Django
from django.conf.urls.static import static

urlpatterns = [
    # Anything starting with /admin/ will go to Django's built-in admin site
    path('admin/', admin.site.urls),  
    path('', include('main_app.urls')),  
]

# this is to serve static files during development
'''In development mode (DEBUG mode),  
since we  don't have a separate web server 
therefore Django temporarily acts like a file server to make development easier.'''
if settings.DEBUG:
    # Only serve static and media files manually when developing locally -- DEBUG = True.
    # static is a django helper function to serve static files
    # static()--it generates a new URL pattern for serving static files during development.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # STATIC_URL	URL prefix for static files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # MEDIA_URL	URL prefix for media files
    # STATIC_ROOT	Folder where collected static files are stored
    # MEDIA_ROOT	Folder where uploaded media files are stored
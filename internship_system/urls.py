from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),   # ready-made management website: /admin
    path('', include('portal.urls')),  # our pages live in the portal app
]

# lets the browser open uploaded resumes at http://127.0.0.1:8000/media/...
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

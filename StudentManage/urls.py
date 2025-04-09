from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
    path('view_file/<int:file_id>/', views.view_file, name='view_file'),
    path('viewEditor/<int:file_id>/', views.editor, name='viewEditor'),
    path('save_code/<int:file_id>/', views.save_code, name='save_code'),  # ✅ Added missing save_code route
    path('run_code/<int:file_id>/', views.run_code, name='run_code'),  # ✅ Ensure correct path
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

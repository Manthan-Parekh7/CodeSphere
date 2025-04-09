from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_assignment/', views.add_assignment, name='add_assignment'),
    path('delete_assignment/<int:assig_id>/',
         views.delete_assignment, name='delete_assignment'),
]

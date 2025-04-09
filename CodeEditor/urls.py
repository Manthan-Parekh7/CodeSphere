from django.urls import path
from .views import editor, runCode, save_code

urlpatterns = [
    path("", editor, name="editor"),
    path("run_code", runCode, name="run_code"),
    path("save_code/", save_code, name="save_code"),
]

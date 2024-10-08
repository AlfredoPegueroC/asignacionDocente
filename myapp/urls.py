
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('api/create_Universidad', views.create_Universidad),
    path('api/create_facultad', views.create_Facultad),
    path('api/universidad', views.getAllUniversidad),
    path('api/facultad', views.getAllFacultad),
    path('api/escuela', views.getAllEscuela),
    path('api/tipoDocente', views.getAllTipoDocente),
    path('api/categoriaDocente', views.getAllCategoriaDocente),
    path('api/docente', views.getAllDocente),
    path('api/periodoAcademico', views.getAllPeriodoAcademico),
]

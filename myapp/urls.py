
from django.urls import path
from . import views
urlpatterns = [
    #URLS CREATE
    path('', views.index, name='index'),
    path('api/universidad/create', views.create_Universidad),
    path('api/facultad/create', views.create_Facultad),
    path('api/escuela/create', views.create_Escuela),
    path('api/tipodocente/create', views.create_TipoDocente),
    path('api/categoriadocente/create', views.create_CategoriaDocente),
    path('api/docente/create', views.create_Docente),
    path('api/periodoacademico/create', views.create_PeriodoAcademico),
    # URLS GET OR RETRIEVE
    path('api/universidad', views.getAllUniversidad),
    path('api/facultad', views.getAllFacultad),
    path('api/escuela', views.getAllEscuela),
    path('api/tipodocente', views.getAllTipoDocente),
    path('api/categoriaDocente', views.getAllCategoriaDocente),
    path('api/docente', views.getAllDocente),
    path('api/periodoacademico', views.getAllPeriodoAcademico),
    # URLS UPDATE
    path('api/universidad/update/<int:pk>/', views.update_universidad),
    path('api/universidad/update/<int:pk>/', views.update_universidad),
    path('api/facultad/update/<int:pk>/', views.update_facultad),
    path('api/escuela/update/<int:pk>/', views.update_escuela),
    path('api/tipodocente/update/<int:pk>/', views.update_tipoDocente),
    path('api/categoriadocente/update/<int:pk>/', views.update_categoriaDocente),
    path('api/docente/update/<int:pk>/', views.update_docente),
    path('api/periodoacademico/update/<int:pk>/', views.update_periodoAcademico),
    # URLS DELETE
    path('api/universidad/delete/<int:pk>/', views.delete_universidad),
    path('api/facultad/delete/<int:pk>/', views.delete_facultad),
    path('api/escuela/delete/<int:pk>/', views.delete_escuela),
    path('api/tipodocente/delete/<int:pk>/', views.delete_tipoDocente),
    path('api/categoriadocente/delete/<int:pk>/', views.delete_categoriaDocente),
    path('api/docente/delete/<int:pk>/', views.delete_docente),
    path('api/periodoacademico/delete/<int:pk>/', views.delete_periodoAcademico),
    # AUTH
    path('api/login', views.login_view),
    path('api/logout', views.logout_view)
]

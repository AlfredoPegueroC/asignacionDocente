
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #URLS CREATE
    path('', views.index, name='index'),
    path('api/usuarios', views.UserListView.as_view(), name='user-list'),
    path('api/registro', views.RegistroUsuarioAPI.as_view(), name='registro'),
    path('api/logs/', views.APILogList.as_view(), name='api-logs'),
    path("api/usuarios/<int:pk>/", views.EditarUsuarioAPI.as_view()),
    path('api/asignacion/copiar', views.copiar_asignaciones),
    
    path('api/universidad/create', views.create_Universidad),
    path('api/campus/create', views.create_Campus),
    path('api/facultad/create', views.create_Facultad),
    path('api/escuela/create', views.create_Escuela),
    path('api/tipodocente/create', views.create_TipoDocente),
    path('api/categoriadocente/create', views.create_CategoriaDocente),
    path('api/docente/create', views.create_Docente),
    path('api/periodoacademico/create', views.create_PeriodoAcademico),
    path('api/asignacion/create', views.create_asignacion),
    # URLS GET OR RETRIEVE
    path('api/universidad', views.getAllUniversidad),
    path('api/campus', views.getAllCampus),
    path('api/facultad', views.getAllFacultad),
    path('api/escuela', views.getAllEscuela),
    path('api/tipodocente', views.getAllTipoDocente),
    path('api/categoriaDocente', views.getAllCategoriaDocente),
    path('api/docente', views.getAllDocente),
    path('api/periodoacademico', views.getAllPeriodoAcademico),
    path('api/asignacion', views.getAllAsignacion),
    path('api/asignacion_frontend', views.getAllAsignacion_frontend),
    # test
    path('universidades', views.get_Universidad),
    path('facultades', views.get_Facultad),
    path('escuelas', views.get_Escuela),
    path('tipodocentes', views.get_TipoDocente),
    path('categoriadocentes', views.get_CategoriaDocente),
    path('periodos', views.get_PeriodoAcademico),
    path('docentes', views.get_Docente),

    # URLS UPDATE
    path('api/universidad/edit/<int:pk>/', views.update_universidad),
    path('api/facultad/edit/<int:pk>/', views.update_facultad),
    path('api/escuela/edit/<int:pk>/', views.update_escuela),
    path('api/tipodocente/edit/<int:pk>/', views.update_tipoDocente),
    path('api/categoriadocente/edit/<int:pk>/', views.update_categoriaDocente),
    path('api/docente/edit/<int:pk>/', views.update_docente),
    path('api/periodoacademico/edit/<int:pk>/', views.update_periodoAcademico),
    path('api/asignacion/edit/<int:pk>/', views.update_asignacion),
    # URLS DELETE
    path('api/universidad/delete/<pk>/', views.delete_universidad),
    path('api/campus/delete/<int:pk>/', views.delete_campus),
    path('api/facultad/delete/<int:pk>/', views.delete_facultad),
    path('api/escuela/delete/<int:pk>/', views.delete_escuela),
    path('api/tipodocente/delete/<int:pk>/', views.delete_tipoDocente),
    path('api/categoriadocente/delete/<int:pk>/', views.delete_categoriaDocente),
    path('api/docente/delete/<int:pk>/', views.delete_docente),
    path('api/periodoacademico/delete/<int:pk>/', views.delete_periodoAcademico),
    path('api/asignacionDocente/delete/<int:pk>/', views.delete_asignacionDocente),
    path('api/asignacionDocente/delete', views.delete_asignacion_by_period),
    # DETAILS
    path('api/universidad/<int:pk>/', views.details_universidad, name='detalle_universidad'),
    path("api/campus/<str:codigo>/", views.details_campus),
    path('api/facultad/<int:pk>/', views.details_facultad, name='detalle_facultad'),
    path('api/escuela/<int:pk>/', views.details_escuela, name='detalle_escuela'),
    path('api/tipodocente/<int:pk>/', views.details_tipoDocente, name='detalle_tipoDocente'),
    path('api/categoriadocente/<int:pk>/', views.details_categoriaDocente, name='detalle_categoriaDocente'),
    path('api/docente/<int:pk>/', views.details_docente, name='detalle_docente'),
    path('api/periodoacademico/<int:pk>/', views.details_periodoAcademico, name='detalle_periodoAcademico'),
    path('api/asignacion/<int:pk>/', views.details_Asignacion),
    # AUTH
    path('api/login', views.login_view),
    path('api/logout', views.logout_view),

    # Exports or Reports
    path('export/universidad',views.UniversidadExport),
    path('export/campus', views.CampusExport),
    path('export/facultad', views.FacultadExport),
    path('export/escuela', views.EscuelaExport),
    path('export/docente', views.DocenteExport),
    path('export/asignacionDocenteExport', views.asignacionDocenteExport),
    path('export/categoriaDocente', views.CategoriaDocenteExport),
    path('export/tipoDocente', views.TipoDocenteExport),
    path('export/periodoAcademico', views.PeriodoAcademicoExport),
    # import
    path('import/asignacion', views.ImportAsignacion.as_view()),
    path('import/campus', views.ImportCampus.as_view()),
    path('import/facultad', views.ImportFacultad.as_view()),
    path('import/escuela', views.ImportEscuela.as_view()),
    path('import/docente', views.ImportDocente.as_view()),
    path('import/universidad', views.ImportUniversidad.as_view()),
    path('import/categoriaDocente', views.ImportCategoriaDocente.as_view()),
    path('import/tipoDocente', views.ImportTipoDocente.as_view()),
    path('api/resumen/docente/', views.resumen_asignaciones_docente)

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


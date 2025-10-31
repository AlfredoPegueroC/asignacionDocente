
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'usuarios', views.UserViewSet, basename='usuarios')

urlpatterns = router.urls

urlpatterns = [
    #URLS CREATE
    path('', views.index, name='index'),
    path('api/protegida/', views.vista_protegida, name='vista_protegida'),
    path('api/', include(router.urls)),
    path('api/logs/', views.APILogList.as_view(), name='api-logs'),
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
    path('api/asignatura/create', views.create_Asignatura),
    path('api/accion/create', views.create_accion),
    path('api/status/create', views.create_status),
    
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
    path('api/asignatura', views.getAllAsignatura),
    path('api/accion', views.getAllAccion),
    path('api/status', views.getAllStatus),
    
    # test
    path('universidades', views.get_Universidad),
    path('campus', views.get_Campus),
    path('facultades', views.get_Facultad),
    path('escuelas', views.get_Escuela),
    path('tipodocentes', views.get_TipoDocente),
    path('categoriadocentes', views.get_CategoriaDocente),
    path('periodos', views.get_PeriodoAcademico),
    path('docentes', views.get_Docente),
    path('acciones', views.get_acciones),
    path('status', views.get_status),

    # URLS UPDATE
    path('api/universidad/edit/<str:codigo>/', views.update_universidad),
    path('api/facultad/edit/<str:codigo>/', views.update_facultad),
    path('api/campus/edit/<str:codigo>/', views.update_campus),
    path('api/escuela/edit/<str:codigo>/', views.update_escuela),
    path('api/tipodocente/edit/<str:codigo>/', views.update_tipoDocente),
    path('api/categoriadocente/edit/<str:codigo>/', views.update_categoriaDocente),
    path('api/docente/edit/<str:codigo>/', views.update_docente),
    path('api/periodoacademico/edit/<str:codigo>/', views.update_periodoAcademico),
    path('api/asignacion/edit/<int:pk>/', views.update_asignacion),
    path('api/asignatura/edit/<str:codigo>/', views.update_asignatura),
    path('api/accion/edit/<str:codigo>/', views.update_accion),
    path('api/status/edit/<str:codigo>/', views.update_status),
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
    path('api/asignatura/delete/<str:codigo>/', views.delete_asignatura),
    path('api/accion/delete/<int:pk>/', views.delete_accion),
    path('api/status/delete/<int:pk>/', views.delete_status),
    # DETAILS
    path('api/universidad/<str:codigo>/', views.details_universidad, name='detalle_universidad'),
    path("api/campus/<str:codigo>/", views.details_campus),
    path('api/facultad/<str:codigo>/', views.details_facultad, name='detalle_facultad'),
    path('api/escuela/<str:codigo>/', views.details_escuela, name='detalle_escuela'),
    path('api/tipodocente/<str:codigo>/', views.details_tipoDocente, name='detalle_tipoDocente'),
    path('api/categoriadocente/<str:codigo>/', views.details_categoriaDocente, name='detalle_categoriaDocente'),
    path('api/docente/<str:codigo>/', views.details_docente, name='detalle_docente'),
    path('api/periodoacademico/<str:codigo>/', views.details_periodoAcademico, name='detalle_periodoAcademico'),
    path('api/asignacion/<int:pk>/', views.details_Asignacion),
    path('api/asignatura/<str:codigo>/', views.details_asignatura, name='detalle_asignatura'),
    path('api/accion/<str:codigo>', views.details_acciones, name='detalle_accion'),
    path('api/status/<str:codigo>', views.details_status, name='detalle_status'),
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
    path('export/asignatura', views.AsignaturaExport),
    # import
    path('import/asignacion', views.ImportAsignacion.as_view()),
    path('import/campus', views.ImportCampus.as_view()),
    path('import/facultad', views.ImportFacultad.as_view()),
    path('import/escuela', views.ImportEscuela.as_view()),
    path('import/docente', views.ImportDocente.as_view()),
    path('import/universidad', views.ImportUniversidad.as_view()),
    path('import/categoriaDocente', views.ImportCategoriaDocente.as_view()),
    path('import/asignatura', views.ImportAsignatura.as_view()),
    path('import/tipoDocente', views.ImportTipoDocente.as_view()),
    path('api/resumen/docente/', views.resumen_asignaciones_docente),
    path("api/dashboard/", views.dashboard_data, name="dashboard-data"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


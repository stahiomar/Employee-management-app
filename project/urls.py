from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("hello",views.hello,name="hello"),
    path("home",views.home,name="home"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("evaluateEmployees",views.evaluateEmployees,name="evaluateEmployees"),
    path("responsablePage",views.responsablePage,name="responsablePage"),
    path("allEmp",views.table,name="table"),
    path("adminLogout",views.adminLogout,name="adminLogout"),
    path("addEmployee",views.addEmployee,name="addEmployee"),
    path("removeEmployee",views.removeEmployee,name="removeEmployee"),
    path("addResponsable",views.addResponsable,name="addResponsable"),
    path("responsableLogout",views.responsableLogout,name="responsableLogout"),
    path("login",views.login,name="login"),
    path("empInfos/<int:employee_id>/", views.showEmpInfos, name="showEmpInfos"),
    path("empLogout",views.empLogout,name="empLogout"),
    path('editEmpInfos', views.editEmpInfos, name='editEmpInfos'),
    path('editEmp/<int:employee_id>/', views.editEmp, name='editEmp'),
    path('searchEmp', views.searchEmp, name='searchEmp'),
    path('addFormation', views.addFormation, name='addFormation'),
    path('empPage', views.empPage, name='empPage'),
]

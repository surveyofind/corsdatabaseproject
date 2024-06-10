
from django.urls import path
from.import views

urlpatterns = [
    path('',views.login_view,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('vender_dashboard',views.vender_dashboard,name='vender_dashboard'),
    # path('vendor_data',views.vendor_data,name='vendor_data'),
    path('control_centre_dashboard',views.control_centre_dashboard,name='control_centre_dashboard'),
    path('gdc_dashboard',views.gdc_dashboard,name='gdc_dashboard'),
    path('controlcentreform',views.controlcentreform,name='controlcentreform'),
    path('edit/<str:corsid>/', views.edit_controlcentre, name='edit_controlcentre'),
    path('edit_vendor/<str:corsid>/',views.edit_vendor_data, name='edit_vendor_data'),
    path('vendor_datalog',views.vendor_datalog, name='vendor_datalog'),
    path('edit_gdc/<str:corsid>/',views.edit_gdc_data, name='edit_gdc_data'),
    path('admin_login',views.admin_login, name='admin_login'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('vandor_admindashboard',views.vandor_admindashboard, name='vandor_admindashboard'),
    path('gdc_admindashboard',views.gdc_admindashboard, name='gdc_admindashboard'),
    path('gdc_admindashboard',views.gdc_admindashboard, name='gdc_admindashboard'),
    path('control_centerlog',views.control_centerlog, name='control_centerlog'),
    path('gdc_log',views.gdc_log, name='gdc_log'),
    path('gdc_logdownload_text_file', views.gdc_logdownload_text_file, name='download_text_file'),
    path('control_centerlogdownload', views.control_centerlogdownload, name='control_centerlogdownload'),
    path('vendor_datatext_file', views.vendor_datatext_file, name='vendor_datatext_file'),
    path('download_csv', views.vendardownload_csv, name='download_csv'),
    path('gdcdownload_csv', views.gdcdownload_csv, name='gdcdownload_csv'),
    path('control_centre_dashboard_csv', views.control_centre_dashboard_csv, name='control_centre_dashboard_csv'),
    path('approve_users', views.approve_users, name='approve_users'),
    
]

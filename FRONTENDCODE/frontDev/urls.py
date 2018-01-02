from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^admin_side/', views.admin_side, name='admin_side'),
    url(r'^kiosk/', views.kiosk, name='kiosk'),
    url(r'^port/', views.port, name='port'),

]
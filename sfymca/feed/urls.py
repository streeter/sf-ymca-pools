from django.urls import path

from sfymca.feed import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<branch_name>.ics', views.branch, name='branch_calendar'),
]

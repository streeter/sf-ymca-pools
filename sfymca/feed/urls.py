from django.urls import path

from sfymca.feed import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<branch_name>.ics", views.branch_calendar, name="branch_calendar"),
    path("<branch_name>/", views.branch, name="branch"),
]

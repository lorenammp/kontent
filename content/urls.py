from django.urls import path
from . import views

urlpatterns = [
    path("contents/", views.ContentsRoutes.as_view()),
    path("contents/<int:course_id>/", views.ContentsById.as_view()),
    path("contents/filter/", views.ContentsFilter.as_view())
]
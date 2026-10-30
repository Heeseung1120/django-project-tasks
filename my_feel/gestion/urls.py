from django.urls import path

from .views import ProjectView

urlpatterns = [
    path("projects/", ProjectView.as_view(), name="project-list"),

    path("projects/<int:pk>/", ProjectView.as_view(), name="project-detail"),
]
from django.urls import path
from .views import ProjectListView, ProjectDetailView, TaskUpdateView,TaskDeleteView, TaskDetailView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
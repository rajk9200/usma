

from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list),
    path('add/', views.task_add),
    path('tasks/', views.tasks),
    path('task_delete/<id>', views.task_delete),
]

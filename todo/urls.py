from django.urls import path
from . import views

urlpatterns = [
  #  path('', views.home, name='home'),  # Home page
  #  path('delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Delete task
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path("save_order/", views.save_order, name="save_order"),

]
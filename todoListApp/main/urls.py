
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('app/', views.app),
    path('add_todo/', views.add_todo),
    path('remove_todo/<int:todolistid>', views.remove_todo),
    path('task/<int:todolistid>', views.taskView),
    path('create_task/<int:todolistid>', views.create_task),
    path('remove_task/<int:todolistid>/<int:taskid>', views.remove_task),
    path('save_task/<int:todolistid>/<int:taskid>', views.save_task),
]

from django.urls import path

from TodoApp import views


urlpatterns = [
    path('', views.index, name="index"),
    path('creation/', views.creation, name="creation"),
    path('connexion/', views.connexion, name="connexion"),
    path('deconnexion/', views.deconnexion, name="deconnexion"),
    path('toggle_todo/', views.toggle_todo, name="toggle_todo"),
    path('toto_activees/', views.toto_activees, name="toto_activees"),
    path('toto_desactivees/', views.toto_desactivees, name="toto_desactivees"),
    path('delete_todo/<int:id>', views.delete_todo, name="delete_todo"),
    path('update_todo/<int:id>', views.update_todo, name="update_todo"),

]



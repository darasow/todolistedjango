# Create your views here.
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django .contrib .auth import authenticate, login, logout
from django.contrib .auth.models import User
from django.contrib .auth.forms import UserCreationForm
from .models import Todo
from TodoApp.forms import TodoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password, username)
        user = authenticate( username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect("index")
            else:
                messages.error(request, "Ce compte est désactivé.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'pages/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect("connexion")

def toto_activees(request):
    todos = Todo.objects.filter(statut=True, idUser = request.user) 
    # Pagination
    paginator = Paginator(todos, 4)  # 4 tâches par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/index.html', {'page_obj': page_obj})


def toto_desactivees(request):
    todos = Todo.objects.filter(statut=False, idUser = request.user) 
    # Pagination
    paginator = Paginator(todos, 4)  # 4 tâches par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/index.html', {'page_obj': page_obj})


def creation(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            messages.error(request, "Tous les champs doivent être remplis.")
            return redirect("creation")
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect("creation")
        user_existe = User.objects.filter(username=username).exists()
        if user_existe:
            messages.error(request, "L'utilisateur existe déjà.")
            return redirect("creation")
        user = User(username=username, email=email)
        user.set_password(password1)  
        user.save()
        messages.success(request, "Compte créé avec succès. Veuillez vous connecter.")
        return redirect('connexion')
    return render(request, 'pages/creationCompte.html')

def index(request):
    if not request.session.get('user_id'):
        return redirect("connexion")
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.idUser = request.user  # Associe l'utilisateur connecté
            todo.save()
            return redirect("index")
    # Filtre les tâches de l'utilisateur connecté
    todos = Todo.objects.filter(idUser=request.user)
    # Pagination
    paginator = Paginator(todos, 4)  # 4 tâches par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/index.html', {'page_obj': page_obj})


def toggle_todo(request):
    id_todo = request.POST.get('id_todo')
    todo = get_object_or_404(Todo, pk=id_todo)
    todo.statut = not todo.statut  # Inverser le statut de la todo
    todo.save()
    return redirect("index")

def update_todo(request, id):
    todo = Todo.objects.get(pk=id)
    if request.method == "POST":
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            updated_todo = form.save(commit=False)
            if 'image' in request.FILES:
                print("Nouvelle image téléchargée.")
                print(todo.image)
                if todo.image:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(todo.image))
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print("Ancienne image supprimée.")
                updated_todo.image = request.FILES['image']
            else:
                print("Aucune nouvelle image téléchargée.")
            updated_todo.save()
            return redirect("index")
    else:
        form = TodoForm(instance=todo)
    todos = Todo.objects.filter(idUser=request.user)
    # Pagination
    paginator = Paginator(todos, 4)  # 4 tâches par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/index.html', {'page_obj': page_obj, 'form': form, 'todo': todo})

def delete_todo(request, id):
    todo = Todo.objects.get(pk=id)
    if todo.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(todo.image))
        if os.path.exists(image_path):
            os.remove(image_path)
    todo.delete()
    return redirect("index")
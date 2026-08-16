from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#from django.contrib.auth.decorators import login_required
#me redirige a signin si intento ingresar desde la url a una tarea
###se añade esto a settings.py LOGIN_URL = '/signin'

def home(request):
    return render(request, "home.html")


def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "user already exists"},
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "password do not mash"},
        )
###son funciones que solo se haran si el usuario esta logueado
@login_required
def tasks(request):
    ###con el filter(user=request.user) me muestra solo las tareas del usuario actual
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html",{'tasks': tasks})
###Task es un modelo (una clase que representa una tabla en la base de datos).
###Task.objects.all() obtiene todos los registros de esa tabla y los guarda en la variable tasks.
###En otras palabras, aquí estás trayendo la lista completa de tareas almacenadas en tu base de datos.
###El primer tasks (clave del diccionario) es el nombre con el que la plantilla lo recibirá.
###El segundo tasks (variable Python) se pasa como valor en el diccionario.
###Piensa que es como decir:##"Voy a enviarle a la plantilla un paquete llamado tasks, 
###dentro de ese paquete está la variable tasks que acabo de obtener de la base de datos."
    
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ('-datecompleted')
    return render(request, "tasks.html",{'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
                })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'please provide valida data'
                ###si el campo esta vacio me dice error 
            })

        ###task_id → es el número entero capturado desde la URL (por ejemplo, tasks/5/ 
@login_required
def task_detail(request, task_id):
    ##Busca un objeto en la base de datos del modelo Task cuyo primary key (pk) coincida con task_id.
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form': form})        
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form': form, 'error': "error updating task"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
       task.delete()
    return redirect('tasks')
    
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')

    ###'task_detail.html', {'task':task, 'form':form}) 

    


###el request en parentesis me dice que recibe una peticion
def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST
            ["password"])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'username or password is incorrect'
                })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def secreta(request):
    return render(request, 'secreta.html')
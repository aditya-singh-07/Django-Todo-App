import datetime
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib import auth
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .forms import Todoform
from .models import Todo
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo/index.html')

def signupuser(request):
    if request.method == 'GET':
         if request.user.is_authenticated:
            return redirect('todopage')
         return render(request,'todo/signup.html',{'form':UserCreationForm()})
    else:

        if request.POST['password1'] == request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],'',request.POST['password1'])
                request.session['username'] = request.POST['username']
                messages.success(request, 'successfully signup.')
                user.save()
                login(request,user)
                return redirect('todopage')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': "Username has taken plzz try different username"})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error':"password not match"})
@login_required
def todopage(request):
        usersession= request.session['username']
        todolist =Todo.objects.filter(user=request.user, completed__isnull=True).order_by('-todotitle')
        return render(request, 'todo/todo.html', {'todos': todolist , 'session': usersession})
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
         if request.user.is_authenticated:
            return redirect('todopage')
         else:
            return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user= authenticate(request,username=request.POST['username'], password=request.POST['password'])
        request.session['username'] = request.POST['username']
        if user is None:
            return render(request,'todo/login.html', {'form': AuthenticationForm(),'error': 'incorrect username and password invalid'})
        else:
            messages.success(request, 'login succcess!!.')
            login(request, user)
            return redirect('todopage')
@login_required
def createtodo(request):
    if request.method == 'GET':
         return render(request,'todo/create.html', {'form': Todoform()})
    else:
        try:
           form= Todoform(request.POST)
           todocreate=form.save(commit=False)
           todocreate.user= request.user
           messages.success(request, 'successfully created.')
           todocreate.save()
           return redirect('todopage')
        except ValueError:
            return render(request, 'todo/create.html', {'form': Todoform(), 'error': 'bad data passed plzz try again'})
@login_required
def viewtodo(request, todo_pk):
    todoview = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form= Todoform(instance=todoview)
        return render(request, 'todo/viewtodo.html', {'todoview': todoview , 'form': form})
    else:
        try:
            form=Todoform(request.POST, instance=todoview)
            messages.success(request, 'successfully updated.')
            form.save()
            return redirect('todopage')
        except ValueError:
            return render(request, 'todo/create.html', {'form': Todoform, 'error': 'bad data info'})
@login_required
def completetodo(request,todo_pk):
    todocomplete = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todocomplete.completed= timezone.now()
        messages.success(request, 'successfully completed.')
        todocomplete.save()
        return redirect('todopage')
@login_required
def deletetodo(request,todo_pk):
    tododelete = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        messages.success(request, 'successfully deleted.')
        tododelete.delete()
        return redirect('todopage')

@login_required
def completed(request):
    completed = Todo.objects.filter(user=request.user, completed__isnull=False).order_by('-completed')
    return render(request, 'todo/completed.html', {'todo': completed})
@login_required
def important(request):
    important = Todo.objects.filter(user=request.user, completed__isnull=True, important=True).order_by('-important')
    return render(request, 'todo/important.html', {'importants': important})
#
# def planning(request):
#     d = datetime.today()
#     planning = Todo.objects.filter(user=request.user, completed__isnull=True,created=str(d)).order_by('-created')
#     return render(request, 'todo/planning.html', {'plannings': planning})
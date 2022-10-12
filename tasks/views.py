from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
#este modulo sirve para los temas de login y logout
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
#importamos el formulario de la carpeta forms.py
from .forms import TaskForm
#importamos las tablas de la carpeta models.py
from .models import Tasks
#modulo para saber la fecha
from django.utils import timezone
#este modulo sirve para proteger las vistas despues de que cerramos sesion
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

#vista home
def home(request):
    return render(request, 'home.html')


#vista formulario signup (registrar Usuario) en la BD
def signup(request):
    #si el metodo es GET lo que hace es que me renderiza el formulario 
    if request.method == 'GET':
        print('enviando datos')
        return render(request, 'signup.html', {
        'form': UserCreationForm,
    })
        
    #si el metodo es POST lo que hace es coger esos datos del formulario y lo enviamos a la BD con la logica de abajo, el metodo POST se ejecuta cuando le demos al boton del formulario
    else:
        if request.POST['password1'] == request.POST['password2']:
        #registrar usuario
            try:
                #recuperamos los datos del formulario y creamos el usuario con la funcion User.objects.create_user()dentro de los parentecis van los datos que se van a recuperar
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                
                #guardamos esos datos recuperados en la BD
                user.save()
                
                #creamos una sesion para que se guarde los datos ingresados
                #este metodo login(request, user), me guarda la sesion en las cookies del buscador  
                login(request, user)
                return redirect('tasks')
            
            #si el usuario que se registra ya existe se ejecuta la logica de abjo
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    
                    #ceramos un error para que se muestre en el html 
                    'error': 'El usuario ya Existe'
                })
                
        #si la contraseña no son iguales ejecuta esta logica
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'las contraseñas no conciden '
                })



#vista despues del login


#mostrar tareas que no estan completas
@login_required
def tareas(request):
    #elm metodo objects.all() me permite traer todos los datos de la base de datos
    #tareas = Tasks.objects.all()
    
    #el metodo objects.filter(user=request.user), me permite traer solo los datos de la base de datos donde el usuario consida, en este caso el user con el que iniciamos sesion, y el datecompleted__isnull=True, solo me trae las tareas que no se han completado
    tareas = Tasks.objects.filter(user = request.user, datecompleted__isnull=True)
    print(tareas)
    return render(request, 'tasks.html', {
         'tareas':tareas
    })




#vista crear tareas
@login_required
def create_task(request):
    #Si el metodo es GET, eso quiere decir que me va a mostrar el formulario con los inputs
    if request.method == 'GET':
        print('Formulario sin introducir datos')
        return render(request,'create_task.html',{
            'form': TaskForm
        })
        
    #cuando el metodo es POST, es porque el formulario esta lleno y cuando le da clik al boton, me va a mandar una solicitud con los datos del formulario
    else:
        #recuperamos esos datos con la ayuda de TaskForm la cual es la clase que creamos con anterioridad en el archivo forms.py, y los datos se recuperan con el metodo request.POST, quedando asi: TaskForm(request.POST), esta solicitud me genera un formulario
        try:
            print(request.POST)
            form = TaskForm(request.POST)
            #al momento de hacer la anterior solicitud guardada en la variable 'form', esta variable me genera un formulario, tenemos que guardar estos datos pero no como formulario, para esto utilizamos el metodo .save(commit=False), esto quiere decir que vamos a guardar los datos de la variable como datos y no formulario y tambien no los guardamos en la base de datos, por ultimo los guardamos en una nueva variable
            new_tarea = form.save(commit=False)
            
            #despues procedemos a guardar estas tareas dependiendo del usuario que la creo, yesto es gracias a que iniciamos sesion con un usuario ya creado con anterioridad y obtenemos el dato de este usuario con el metodo request.user
            new_tarea.user = request.user
            
            #despues de crear la tarea con el usuario asignado, la guardamos en la base de datos con el metodo .save()
            new_tarea.save()
            print(new_tarea)
            return redirect('tasks')
        
        except ValueError:
            return render(request,'create_task.html',{
                'form': TaskForm,
                'error': 'porfavor ingresa datos Validos',
            })
  
  
            
#vista detalles de la tarea y actulizar tarea
@login_required
def detailTask(request, task_id):
    #task = Tasks.objects.get(id=task_id)# se puede hacer de esta manera tambien 
    #lo hacemos con el metodo get_object_or_404, es porque cuando se ingresa una tarea o id equivocado salga una pagina 404, osea que no se encontro
    if request.method == "GET":
        task = get_object_or_404(Tasks, id=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{'task':task, 'form':form})   
    else:
        task = get_object_or_404(Tasks, id=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks')
 
 
    
#boton completar tarea 
@login_required 
def tarea_completa(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')  
 
 
     
#boton eliminar tarea   
@login_required
def tarea_eliminar(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')   
   
   
   
#vista Mostar todas las tareas que estan completas
@login_required
def tareas_completas(request):
    #traemos todas las tareas que en su parametro datecompleted en el modelo Tasks de models.py sea False
    tareas = Tasks.objects.filter(user = request.user, datecompleted__isnull=False)
    return render(request, 'tasks.html', {
         'tareas':tareas
    })


    


        
#vista cerra sesion
def salir(request):
    
    #traemos el metodo logout que importamos, para cerrar sesion, que esta guardado en las cookies del buscador
    logout(request)
    return redirect('home')



#vista iniciar sesion
def iniciarSesion(request):
    
    #si es el metodo GET, solo renderizamos el formulario
    if request.method == 'GET':
        return render(request, 'iniciarSesion.html', {
            'form': AuthenticationForm
        })
    
    #cuando llenamos los inputs y le damos click al boton lo que se genera es un metodo POST, obtenemos los datos de los inputs con la funcion request.POST[''], y estos los validamos con el metodo authenticate, que ayuda a validar los datos recogidos que considan en la BD y guardamos estos datos en una variable
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        
        #generamos una condicion para validar si el usuario viene con datos incorrectos o vienen vacios
        if user is None:
           return render(request, 'iniciarSesion.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o Contraseña es incorrecto'
        })
        #si el user (los datos), considen me va redirigir a otra pagina 
        else:
            #este metodo login(request, user), me guarda la sesion en las cookies del buscador  
            login(request, user)
            return redirect('tasks')
        

  
        
    
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#esta clase sirve para crear una tabla en la BD
class Tasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    #el parametro auto_now_add=True, sirve para que cuando estemos llenando la tabla si no llenamos este apartado este se completa automaticamente
    created = models.DateTimeField(auto_now_add=True)
    
    #el metodo blank=True, sirve para que el campo se opcional al momento de llenar el formulario
    datecompleted = models.DateTimeField(null=True, blank=True)
    
    #este campp de dafault=False significa que me va a marcar una tarea por defecto como "No Importante", tengo que marcarla para que se Importante 
    important = models.BooleanField(default=False)
    
    #relacionamos el usuario que anteriormente fue creado
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #metodo para mostrar la tarea con el nombre de la tarea en el panel de administrador
    def __str__(self):
        return self.title + '- by ' + self.user.username
    
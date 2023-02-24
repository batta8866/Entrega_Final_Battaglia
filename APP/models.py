from django.db import models
from django.contrib.auth.models import AbstractUser , User
from django.urls import reverse , reverse_lazy
from datetime import date , datetime
from PIL import Image


# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField (User , on_delete=models.CASCADE)
    image = models.ImageField (default="default.jpg" , upload_to="profile_pic")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self , *args , **kwargs):
        super(Profile , self).save(*args , **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


#*********************************

class sitios (models.Model):
    pais = models.CharField(max_length=40)
    ciudad = models.CharField(max_length=40)
    direccion = models.CharField(max_length=50)
    actividad_paranormal = models.CharField(max_length=50)
    datos = models.TextField(max_length=400)

class posteo (models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey (User , on_delete=models.CASCADE)
    body = models.TextField(max_length=1500)
    post_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User , related_name="like_post" , blank=True)
    

    def total_likes (self):
        return self.likes.count()

    def __str__(self):
        return self.titulo + " | " + str(self.autor)

    def get_absolute_url(self):
        return reverse("Post-detail", kwargs={'pk': self.pk})



class Coment (models.Model):
    posteo = models.ForeignKey (posteo , related_name="coments" , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = models.TextField()
    post_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" %(self.posteo.titulo , self.name)

    #def get_absolute_url (self):
    #    return reverse ("Post-detail" , kwargs={"id":self.pk})

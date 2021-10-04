from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
import math
import random

# Create your models here.

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField( max_length=50)
    city = models.CharField(max_length=50 ,null=True ,blank = True)
    image = models.ImageField(upload_to = 'images/user-profile', null = True , blank = True)
    fname = models.CharField(max_length=150,null = True ,blank = True)
    lname = models.CharField(max_length=150,null = True ,blank = True)
    number = models.IntegerField(default=1111,blank =True , null =True)


    def __str__(self):
        return str(self.author)

        

class Categories(models.Model):
    title = models.CharField( max_length=50)

    def __str__(self):
        return self.title 

class Post(models.Model):
    title = models.CharField(max_length=2000)
    subtitle = models.CharField(max_length=1000,blank = True , null = True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'images/post-img', null = True , blank = True)
    time_date = models.DateTimeField( auto_now_add=True)
    post = models.TextField()
    category = models.ManyToManyField(Categories)
    read = models.IntegerField(default = 0)
    slug = models.SlugField(null=True,blank=True,unique=True)


    def save(self, *args, **kwargs):
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])

        self.slug = slugify(self.title + "-" + random_str)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)

    def __str__(self):
        return str(self.post)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    comment = models.TextField(default = 'Good Post !')
    time_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name 


class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    replay = models.TextField()

    def __str__(self):
        return str(self.author)


class Feedback(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    feedback = models.TextField()
    rate = models.IntegerField(default=1)


    def __str__(self):
        return str(self.author)


class ContactMe(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    number = models.CharField(max_length=16,null=True,blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
    

    






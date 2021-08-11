from django.db import models
import re
import bcrypt
from .models import *

class UserManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['fname']) < 2:
            errors['fname'] = "First name must be atleast 2 characters"
        if len(post_data['lname']) < 2:
            errors['lname'] = "Last name must be atleast 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email format invalid"
        if len(post_data['email']) < 3:
            errors['username'] = "Username must be atleast 3 characters long"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters long"
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = "Password do not match"
        if len(User.objects.filter(username = post_data['username'])) > 0:
            errors['usernameexist'] = "Username already exists"
        return errors    
    def login_validator(self,post_data):
        errors = {}
        LoginUser = User.objects.filter(username = post_data['logusername'])
        if len(LoginUser) > 0:
            if bcrypt.checkpw(post_data['logpassword'].encode(), LoginUser[0].password.encode()):
                print('password matches')
            else:
                errors['logpassword'] = "Password is incorrect"
        else:
            errors['logusername'] = "Username does not exist"
        return errors

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()
    
class Message(models.Model):
    new_message = models.CharField(max_length=500)
    poster = models.ForeignKey('User', related_name='user_messages', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    new_comment = models.CharField(max_length=255)
    poster_comment=models.ForeignKey('User', related_name="user_comments", on_delete=models.CASCADE, null=True)
    message_comment=models.ForeignKey('Message', related_name="message_comments", on_delete=models.CASCADE, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

# Create your models here.

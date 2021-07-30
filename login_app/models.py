from django.contrib import messages
from django.contrib.messages.api import error
from django.db import models
import re
from datetime import datetime, timedelta
from django.shortcuts import redirect
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        NAME_REGEX= re.compile(r'^[a-zA-z]+$')
        if len(post_data['first_name']) < 2 or not NAME_REGEX.match(post_data['first_name']):
            errors['firstname']= "First name must be at least 2 characters long and only letters"
        if len(post_data['last_name']) < 2 or not NAME_REGEX.match(post_data['last_name']):
            errors['lastname']= "Last name must be at least 2 characters long and only letters"
        if len(post_data['address']) < 5:
            errors['address']= "Address must be at least 5 characters long"
        if len(post_data['city']) < 2:
            errors['city']= "City must be at least 2 characters long"
        if len(post_data['state']) != 2:
            errors['state']= "State must be selected"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address"
        check_email= User.objects.filter(email= post_data['email'])
        if check_email:
            errors['email_input']= "This email address already exists"
        if len(post_data['password']) < 8:
            errors['password']= "Password must be at least 8 characters long"
        if post_data['confirm_pw'] != post_data['password']:
            errors['confirm_pw']= "Passwords don't match"
        return errors

    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['log_email'] = "Invalid email address"
            return errors
        if len(post_data['password']) < 8:
            errors['password']= "Password must be at least 8 characters long"
        user= User.objects.filter(email=post_data['email'])
        if user:
            user= user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['log_password']= "Incorrect password"
        else:
            errors['log_email_password']= "Incorrect email"
        return errors

    def update_validator(self, post_data, user):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
            errors['password']= "Password does not match, can't update profile"
            return errors
        if post_data['first_name'] != "":    
            if len(post_data['first_name']) < 2 or len(post_data['first_name'])> 50:
                errors['firstname']= "First name must be between 2 and 50 characters long"
        else:
            errors['firstname']= "Must provide first name between 2 and 50 characters long"
        if post_data['last_name'] != "": 
            if len(post_data['last_name']) < 2 or len(post_data['last_name'])> 50:
                errors['last_name']= "Last name must be between 2 and 50 characters long"
        else:
            errors['last_name']= "Must provide last name between 2 and 50 characters long"    
        if post_data['email'] != user.email and post_data['email'] != "":
            check_email= User.objects.filter(email= post_data['email'])
            if check_email:
                errors['email_input']= "This email address already in use"
            if not EMAIL_REGEX.match(post_data['email']):
                errors['email'] = "Invalid email address"
        elif post_data['email'] == "":
            errors['email']= "Must provide email"
        if post_data['address'] != "":    
            if len(post_data['address']) < 5:
                errors['firstname']= "Address must be at least 5 characters long"
        else:
            errors['address']= "Must provide address at least 5 characters long"    
        if post_data['city'] != "":    
            if len(post_data['city']) < 2 or len(post_data['first_name'])> 50:
                errors['city']= "City must be between 2 and 50 characters long"
        else:
            errors['city']= "Must provide city name between 2 and 50 characters long"
        return errors


class User(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email= models.CharField(max_length=100, unique=True)
    address= models.CharField(max_length=255)
    city= models.CharField(max_length=50)
    state= models.CharField(max_length=2)
    password= models.CharField(max_length=60)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = UserManager()


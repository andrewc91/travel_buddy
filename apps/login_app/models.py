from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from django.core.exceptions import ObjectDoesNotExist

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, input):
        errors = []

        if len(input['first_name']) < 2:
            errors.append('First name can not be less than 2 characters')

        if len(input['last_name']) < 2:
            errors.append('Last name can not be less than 2 characters')

        if not input['first_name'].isalpha():
            errors.append('First name can contain letters only')

        if not input['last_name'].isalpha():
            errors.append('Last name can contain letters only')

        if not email_regex.match(input['email']):
            errors.append('Not a valid email')

        if len(input['email']) == 0:
            errors.append('Please enter an email')

        if input['password'] != input['confirm']:
            errors.append('Passwords do not match. Try again')

        if len(input['password']) < 8:
            errors.append('Password must be at least 8 characters')

        same = User.objects.filter(email=input['email'])
        if same:
            errors.append('Email is already in use')

        if len(errors) == 0:
            pwHash = bcrypt.hashpw(input['password'].encode(), bcrypt.gensalt().encode())
            user = User.objects.create(first_name=input['first_name'], last_name=input['last_name'], email=input['email'], password=pwHash)
            return (True, user)

        else:
            return (False, errors)

    def login(self, input):
        errors = []
        user = User.objects.filter(email=input['email'])
        if user.exists():
            HashPw = user[0].password.encode()
            InputPw = input['password'].encode()

            if bcrypt.checkpw(InputPw, HashPw):
                return (True, user[0])
            else:
                errors.append(("Email or password doesn't exist!"))
        else:
            errors.append(("Email or password doesn't exist!"))
        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

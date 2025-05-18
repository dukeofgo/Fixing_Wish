from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def user_validator(self, form_data):
        errors = {}
        if len(form_data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters!'
        if len(form_data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters!'
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = 'Email is invalid!'
        email_check = self.filter(email=form_data['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form_data['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters!'
        if form_data['password'] != form_data['confirmed_password']:
            errors['password'] = 'Confirmed password does not match!'
        return errors
    def login_validator(self, form_data):
        errors = {}
        user = User.objects.filter(email=form_data['email'])
        if not user:
            errors['email'] = "You don't have an account with us!"
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = 'Email is invalid!'
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(form_data['password'].encode(), logged_user.password.encode()):
                errors['password'] = 'You entered wrong password, please try again!'
        return errors
    def update_validator(self, form_data):
        errors = {}
        if len(form_data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters!'
        if len(form_data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters!'
        if len(form_data['password']) > 0 and len(form_data['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters!'
        if form_data['password'] != form_data['confirmed_password']:
            errors['password'] = 'Confirmed password does not match!'
        return errors

class WishManager(models.Manager):
    def basic_validator(self, form_data):
        errors = {}
        if len(form_data['item']) < 3:
            errors['item'] = 'Item should be at least 3 characters!'
        if len(form_data['description']) == 0:
            errors['description'] = 'Description must be provided'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.TextField()
    wisher = models.ForeignKey(User, related_name='wishes', on_delete=models.CASCADE)
    granter = models.ManyToManyField(User, related_name='wishes_granted')
    likers = models.ManyToManyField(User, related_name='wishes_liked')
    is_granted = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()


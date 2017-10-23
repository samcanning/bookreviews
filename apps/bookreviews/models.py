# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

class UserMgr(models.Manager):
    def regvalidator(self, postData):
        errors = {}
        emailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" #email format
        nameRegex = r"(^[a-zA-Z]+ [a-zA-Z]+$)" #letters only
        aliasRegex = r"(^[a-zA-Z0-9]+$)" #letters and numbers only
        pwRegex = r"(^[a-zA-Z0-9_.!?-]+$)" #valid password characters (alphanumeric characters or _.!?-)

        #name
        if not re.match(nameRegex, postData['name']):
            errors['name'] = "Must enter a valid name."
        else:
            if len(postData['name']) < 5:
                errors['name'] = "Name must be at least 5 characters."
            elif len(postData['name']) > 255:
                errors['name'] = "Name cannot be longer than 255 characters."
        #alias
        if not re.match(aliasRegex, postData['alias']):
            errors['alias'] = "Alias may only include letters and numbers."
        else:
            if len(postData['alias']) < 3:
                errors['alias'] = "Alias must be at least 3 characters."
            elif len(postData['alias']) > 30:
                errors['alias'] = "Alias cannot be longer than 30 characters." 
        #email
        if not re.match(emailRegex, postData['email']):
            errors['email'] = "Must be a valid email address."
        elif User.objects.filter(email=postData['email']).exists():
            errors['email'] = "This email address is already in use."
        #password
        if str.lower(str(postData['password'])) == 'password':
            errors['password'] = "Password cannot be 'password'."
        elif not re.match(pwRegex, postData['password']):
            errors['password'] = "Not a valid password."
        else:
            if len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters."
            elif postData['password'] != postData['confirmpw']:
                errors['password'] = "Passwords must match."
        return errors

    def loginvalidator(self, postData):
        errors = {}

        try:
            this = User.objects.get(email=postData['email'])
        except:
            errors['email'] = "No user found with this email address."
        
        if 'email' not in errors:
            pw_attempt = str(postData['password'])
            pw_to_check = str(this.password)
            if not bcrypt.checkpw(pw_attempt, pw_to_check):
                errors['password'] = "Incorrect password."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserMgr()

class BookMgr(models.Manager):
    def validator(self,postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Book needs a title."
        elif len(postData['title']) > 255:
            errors['title'] = "Title is too long."
        if len(postData['author']) < 1:
            errors['author'] = "Please enter an author."
        elif len(postData['author']) > 100:
            errors['author'] = "Author's name is too long."
        if len(postData['review']) < 4:
            errors['review'] = "Review is too short."
        if postData['rating'] == 'None':
            errors['rating'] = "Please give the book a rating."
        return errors

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookMgr()

class Review(models.Model):
    body = models.TextField()
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import User, Book, Author, Review

import bcrypt

def index(request):
    return render(request, 'bookreviews/index.html')

def register(request):
    errors = User.objects.regvalidator(request.POST)
    if errors:
        print "invalid"
        return redirect('/')
    else:
        temp_pw = str(request.POST['password'])
        hashed_pw = str(bcrypt.hashpw(temp_pw, bcrypt.gensalt()))
        User.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],password=hashed_pw)
        print 'success!'
        return redirect('/')

def login(request):
    errors = User.objects.loginvalidator(request.POST)
    if errors:
        print "login failed"
        return redirect('/')
    else:
        request.session['logged'] = True
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/books')

def books(request):
    if not request.session['logged']:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'bookreviews/books.html', context)

def logout(request):
    request.session['logged'] = False
    request.session['user_id'] = None
    return redirect('/')

def addbook(request):
    if not request.session['logged']:
        return redirect('/')
    context = {
        'authors': Author.objects.all().order_by('name'),
    }
    return render(request, 'bookreviews/addbook.html', context)

def submitbook(request):
    errors = Book.objects.validator(request.POST)
    if errors:
        return redirect('/books/add')
    else:
        Author.objects.create(name=request.POST['author'])
        Book.objects.create(title=request.POST['title'], author=Author.objects.last())
        Review.objects.create(body=request.POST['review'], book=Book.objects.last(), user=User.objects.get(id=request.session['user_id']), rating=request.POST['rating'])
    return redirect('/books/' + str(Book.objects.last().id))

def bookpage(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'reviews': Book.objects.get(id=book_id).reviews.all(),
        'user_id': request.session['user_id'],
    }
    return render(request, 'bookreviews/bookpage.html', context)

def addreview(request, book_id):
    Review.objects.create(body=request.POST['review'], book=Book.objects.get(id=book_id), user=User.objects.get(id=request.session['user_id']), rating=request.POST['rating'])
    return redirect('/books/' + str(book_id))

def deletereview(request, book_id, review_id):
    Review.objects.get(id=review_id).delete()
    return redirect('/books/' + str(book_id))

def userpage(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'reviews': User.objects.get(id=user_id).reviews.all(),
    }
    return render(request, 'bookreviews/userpage.html', context)
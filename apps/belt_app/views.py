# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book, Author, Review
from django.db.models import Count

# Create your views here.
def index(request):
	return render(request, 'belt_app/index.html')

def register(request):
    post_data = request.POST.copy()
    result = User.objects.register(post_data)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect(reverse('belt:index'))
    else:
        request.session['user'] = result
        return render(reverse('belt:books'))

def login(request):
    post_data = request.POST.copy()
    result = User.objects.login(post_data)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect(reverse('belt:index'))
    else:
        request.session['user'] = result
        return redirect(reverse('belt:books'))

def books(request):
	user = User.objects.get(id=request.session['user'])
	all_reviews = Review.objects.all()
	recent_reviews = all_reviews.order_by('-id')[:3]
	other_reviews = all_reviews.exclude(id__in=recent_reviews)
	context = {
		"user" : user,
		"recent_reviews" : recent_reviews,
		"other_reviews" : other_reviews
	}
	return render(request, 'belt_app/books.html', context)

def users(request, user_id):
	user = User.objects.get(id=user_id)
	reviews = Review.objects.filter(user=user)
	context = {
		'user' : user,
		'reviews' : reviews
	}
	return render(request, 'belt_app/users.html', context)

def book_id(request, book_id):
	book = Book.objects.get(id=book_id)
	users = User.objects.filter(user_reviews__book__id=book.id)
	author = Author.objects.get(all_books__id=book.id)
	reviews = Review.objects.filter(book=book)
	context = {
		"author" : author,
		"book" : book,
		"reviews" : reviews
	}
	return render(request, 'belt_app/book_id.html', context)

def add(request):
	authors = Author.objects.all()
	context = {
		"authors" : authors
	}
	return render(request, 'belt_app/add.html', context)

def post_book(request):
	post_data = request.POST.copy()
	result = Review.objects.validate(post_data, request.session['user'])
	if isinstance(result,list):
		for err in result:
			messages.error(request, err)
		return redirect(reverse('belt:add'))
	else:
		return redirect(reverse('belt:book_id', kwargs={'book_id': result.id})) #when you are looking for a named varaible like <book_id>, use kwargs

def delete(request, review_id):
	review = Review.objects.get(id=review_id)
	review.delete()
	return redirect(reverse('belt:book_id', kwargs={'book_id' : review.book.id})) #kwargs sets the named variable django is looking for to review.book.id

def update(request, book_id):
	post_data = request.POST.copy()
	result = Review.objects.update(post_data, book_id, request.session['user'])
	if isinstance(result,list):
		for err in result:
			messages.error(request, err)
	return redirect(reverse('belt:book_id', kwargs={'book_id' : book_id}))

def logout(request):
    request.session.pop('user')
    return redirect(reverse('belt:index'))
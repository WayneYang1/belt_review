# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self,data):
        errors=[]
        if not data['first_name'].isalpha():
            errors.append("First name may only be letters")
        if len(data['first_name']) < 2:
            errors.append("First name must be more than 2 letters")
        if not data['last_name'].isalpha():
            errors.append("Last name may only be letters")
        if len(data['last_name']) < 2:
            errors.append("Last name must be more than 2 letters")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Invalid email")
        try:
            User.objects.get(email = data['email'])
            errors.append("Email already registered")
        except:
            pass
        if len(data['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if data['password'] != data['confirm']:
            errors.append("Passwords do not match")
        if len(errors) == 0:
            hashed_pw=bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = data['first_name'], last_name = data['last_name'], email = data['email'], hashed_pw=hashed_pw)
            return user.id
        else:
            return errors

    def login(self,data):
        errors=[]
        try:
            current_user = User.objects.get(email = data['email'])
            encrypted_pw = bcrypt.hashpw(data['password'].encode(), current_user.hashed_pw.encode())
            if encrypted_pw != current_user.hashed_pw:
                errors.append("Incorrect Password")
                return errors
            else:
                return current_user.id
        except:
            errors.append("Email not registered")
            return errors

class ReviewManager(models.Manager):
    def validate(self,data,user_id):
        errors=[]
        if len(data['title'])==0:
            errors.append('Please enter a book title')
        try:
            title = Book.objects.get(title=data['title'])
            errors.append('Book already exists')
        except:
            pass
        if len(data['author'])==0:
            errors.append('Please enter an author')
        try:
            author = Author.objects.get(name=data['author'])
            errors.append('Author already exists. Choose from existing list')
        except:
            pass
        if len(data['content'])==0:
            errors.append('Review field is empty. Please submit a review')
        if len(data['rating'])==0:
            errors.append('Please choose a rating (1-5)')
        if len(errors) == 0:
            user = User.objects.get(id=user_id)
            author = Author.objects.create(name=data['author'])
            book = Book.objects.create(title=data['title'])
            book.author.add(author)
            review = Review.objects.create(book=book, user=user, content=data['content'], rating=data['rating'])
            return book
        else:
            return errors

    def update(self,data,book_id,user_id):
        errors=[]
        for key in data:
            if len(data[key]) == 0:
                errors.append(key.replace('_', ' ').title() + " may not be empty.")
                return errors
            else:
                user = User.objects.get(id=user_id)
                book = Book.objects.get(id=book_id)
                review = Review.objects.create(user=user, book=book, content=data['content'], rating=data['rating'])
                return review


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    hashed_pw = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Author(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.ManyToManyField(Author, related_name='all_books')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
	book = models.ForeignKey(Book, related_name='book_reviews')
	user = models.ForeignKey(User, related_name='user_reviews')
	content = models.TextField()
	rating = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = ReviewManager()


from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
	def validateUser(self, post_data):
		print post_data

		is_valid = True
		errors = []
		#check if name and username are valid(at least 3 characters, name must be alpha)
		if len(post_data.get('name')) and len(post_data.get('username')) < 3:
			is_valid = False
			errors.append('name field and username must be more than 3 characters')
		if not post_data.get('name').isalpha():
			is_valid = False
			errors.append('name field must be only alphabetical letters')
		#check that date field is not empty
		if len(post_data.get('date_hired')) == 0: 
			is_valid = False
			errors.append('Please enter a date')
		#if password is greater than 8 characters, matches password confirmation
		if len(post_data.get('password')) < 8:
			is_valid = False
			errors.append('password must be at least 8 characters')
		if post_data.get('password_confirmation') != post_data.get('password'):
			is_valid = False
			errors.append('password and password confirmation must match')

		print (is_valid, errors)
		return (is_valid, errors)


class User(models.Model):
	name = models.CharField(max_length = 45)
	username = models.CharField(max_length = 45)
	password = models.CharField(max_length = 255)
	date_hired = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

	def __str__(self):
		return "name:{}, username:{}, password:{}, created_at:{}, updated_at:{}".format(self.name, self.username, self.password, self.created_at, self.updated_at)

class ProductManager(models.Manager):
	def validateProduct(self, post_data):
		print post_data
		is_valid = True
		errors = []
		#check if product name is more than 3 characters
		if len(post_data.get('name')) < 3:
			is_valid = False
			errors.append('Product must be more than 3 characters')

		print (is_valid, errors)
		return (is_valid, errors)

class Product(models.Model):
	name = models.TextField(max_length = 45)
	created_by = models.ForeignKey(User, related_name = "created_items")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = ProductManager()

class Wishlist(models.Model):
	products = models.ForeignKey(Product, related_name = 'wish_items')
	user = models.ForeignKey(User, related_name = 'wish_items')








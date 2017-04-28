from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
import bcrypt
import pytz
utc = pytz.utc

# Create your views here.
def current_user(request):
	return User.objects.get(id = request.session['user_id'])

def index(request):
	return render(request, 'wish_app/index.html')

def register(request):
	check = User.objects.validateUser(request.POST)
	if request.method != 'POST':
		return redirect('/')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="registration")
			return redirect('/')
	if check[0] == True:
		#has password
		hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())

		#create user
	user = User.objects.create(
		name = request.POST.get('name'),
		username = request.POST.get('username'),
		password = hashed_pw,
		date_hired = request.POST.get('date_hired')
	)
	#add user to session, logging them in
	request.session['user_id'] = user.id
	#route to dashboard page
	return redirect('/dashboard')

def login(request):
	#find user
	user = User.objects.filter(username = request.POST.get('username')).first()
	#Check user credentials
	#add them to session and log in or add error message and route to dashboard page
	if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
		request.session['user_id'] = user.id
		return redirect('/dashboard')
	else: 
		messages.add_message(request, messages.INFO, 'invalid credentials', extra_tags="login")
		return redirect('/')
	return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect('/')

def dashboard(request):
	user = current_user(request)

	product_ids = []
	for wish in user.wish_items.all():
		if wish.products.id not in product_ids:
			product_ids.append(wish.products.id)

	context = {
		'current_user': user,
		'products': Product.objects.all(),
		'wishes': Wishlist.objects.all(),
		'other_products': Product.objects.exclude(id__in = product_ids)
	}
	return render(request, 'wish_app/dashboard.html', context)

def delete(request, id):
	product = Product.objects.get(id=id)
	product.delete()

	return redirect('/dashboard')

def remove(request, id):
	##Remove from wishlist
	wish_item = Wishlist.objects.get(id = id)
	wish_item.delete()
	return redirect('/dashboard')

def add_wish(request, id):
	##add to user's wishlist
	product = Product.objects.get(id=id)
	wish = Wishlist.objects.create(
		products = product,
		user = current_user(request)
		)
	print wish.user
	return redirect('/dashboard')

def create(request):
	##renders page to add a product
	return render(request, 'wish_app/create.html')

def add_item(request):
	##adds item to products and user's wishlist
	check = Product.objects.validateProduct(request.POST)
	if request.method != 'POST':
		return redirect('/create')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="add_item")
			return redirect('/create')
	if check[0] == True:

		product = Product.objects.create(
			name = request.POST.get('name'),
			created_by = current_user(request),
			)
		wishlist = Wishlist.objects.create(
			products = product,
			user = current_user(request)
			)

		return redirect('/dashboard')

def show_product(request, id):
 	product =  Product.objects.get(id = id)
	context = {
		'product': product,
		'wishes':  product.wish_items.all()			
	}

	return render(request, 'wish_app/show.html', context)







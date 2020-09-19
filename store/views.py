from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.urls import reverse
from django.http import JsonResponse
import json
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .filters import ItemFilter, CategoryFilter, TagFilter, SearchCat, SearchTag
from staff.filters import OrderFilterC
from .forms import CreateUserForm, CreateCustomerForm, CustomerForm, ReviewForm, UserForm
from .decorators import unauthenticated_user

def index(request):
    return render(request, "store/index.html")
    
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('store:index'))
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, "store/login.html")

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:login'))

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    formC = CreateCustomerForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        formC = CreateCustomerForm(request.POST)
        if form.is_valid() and formC.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            phone = formC.cleaned_data.get('phone')
            customer, created = Customer.objects.get_or_create(
                email=email,
            )

            customer.user = User.objects.get(username=user)
            customer.first_name = first_name
            customer.last_name = last_name
            customer.phone = phone
            customer.is_user = True
            customer.save()

            messages.success(request, 'Account was created for ' + user)
            return HttpResponseRedirect(reverse('store:login'))

    context = {
        'form': form,
        'formC': formC
    }
    return render(request, "store/register.html", context)

@login_required(login_url='store:login')
def userProfile(request, pk):

    data = cartData(request)

    cartItems = data['cartItems']

    user = User.objects.get(id=pk)
    customer = Customer.objects.get(user=user)

    try:
        orders = customer.order_set.filter(complete=True).order_by('-id')
        count = orders.count()
        address = ShippingAddress.objects.filter(customer=customer).last()
        
        filterOrderC = OrderFilterC(request.GET, queryset=orders)
        orders = filterOrderC.qs

        orderitems = OrderItem.objects.all()    

        filterItem = ItemFilter(request.GET, queryset=orderitems)
        orderitems = filterItem.qs
    except:
        orders = {}
        count = 0
        address = {},
        filterOrderC = {}
        filterItem = {}

    context = {
        'user': user,
        'customer': customer,
        'count': count,
        'orders': orders,
        'address': address,
        'filterOrderC': filterOrderC,
        'filterItem': filterItem,
        'cartItems': cartItems
    }
    return render(request, 'store/profile.html', context)

@login_required(login_url='store:login')
def userSettings(request, pk):
    data = cartData(request)

    cartItems = data['cartItems']

    user = User.objects.get(id=pk)
    customer = Customer.objects.get(user=user)
    form = CustomerForm(instance=customer)

    formU = UserForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid:
            form.save()

    context = {
        'user': user,
        'form': form,
        'formU': formU,
        'cartItems': cartItems
    }
    return render(request, 'store/settings.html', context)

@login_required(login_url='store:login')
def passwordChange(request, pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse("store:settings", args=(pk,)))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'store/change_password.html', {
        'form': form
    })

def products(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    itemNumber = 0

    products = Product.objects.all().order_by('-date_created')

    filterItem = ItemFilter(request.GET, queryset=products)
    products = filterItem.qs
    
    paginatedProduct = Paginator(filterItem.qs, 8)
    product_page_number = request.GET.get('page')
    product_page_obj = paginatedProduct.get_page(product_page_number)

    if request.user.is_authenticated:
        for product in product_page_obj:
            for item in items:  
                if product == item.product:
                    product.in_cart = True
                    productItems = product.orderitem_set.filter(order=order)
                    itemNumber = sum([item.quantity for item in productItems])
            user = request.user
            favs = Favourite.objects.filter(user=user)
            for fav in favs:
                if product == fav.product:
                    product.in_fav = True
   
    else:
        for product in product_page_obj:
            for item in items:  
                if product.id == item['id']:
                    product.in_cart = True
                    itemNumber = item['quantity']
                
    context = {
        'products': products,
        'cartItems': cartItems,
        'order': order,
        'items': items,
        'itemNumber': itemNumber,
        'filterItem': filterItem,
        'product_page_obj': product_page_obj
    }
    return render(request, 'store/products.html', context)

def product_details(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    try:
        count = Review.objects.filter(user=user, product=product)
    except:
        count=False
    
    if request.method == "POST":
        rating = request.POST["rating"]
        text = request.POST["text"]

        if count:
            count=True

        review = Review.objects.create(user=user, product=product, text=text, rating=rating)
        review.save()
        return HttpResponseRedirect(reverse("store:product_details", args=(id,)))

    reviews = Review.objects.filter(product=product).order_by('-date_created')

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    itemNumber = 0

    if request.user.is_authenticated:
        for item in items:  
            if product == item.product:
                product.in_cart = True
                productItems = product.orderitem_set.filter(order=order)
                itemNumber = sum([item.quantity for item in productItems])
    else:
        for item in items:  
            if product.id == item['id']:
                product.in_cart = True
                itemNumber = item['quantity']

    context = {
        'product': product,
        'cartItems': cartItems,
        'order': order,
        'items': items,
        'itemNumber': itemNumber,
        'reviews': reviews,
        'count': count
    }
    return render(request, "store/product_details.html", context)

@login_required(login_url='store:login')
def updateReview(request, pk, id):
    review = Review.objects.get(id=id)
    form = ReviewForm(instance=review)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("store:product_details", args=(pk,)))

    context = {
        'form': form,
        'review': review
    }
    return render(request, 'store/update_review.html', context)

@login_required(login_url='store:login')
def deleteReview(request):
    data = json.loads(request.body)
    reviewId = data['reviewId']
    action = data['action']

    print('reviewId:', reviewId, 'Action:', action)
          
    review = Review.objects.get(id=reviewId)

    if action == 'delete':
        review.delete()

    return JsonResponse('Review was deleted', safe=False)

def categories(request):
    categories = Category.objects.all().order_by('name')

    filterCategory = SearchCat(request.GET, queryset=categories)
    categories = filterCategory.qs

    data = cartData(request)

    cartItems = data['cartItems']
            
    context = {
        'categories': categories,
        'cartItems': cartItems,
        'filterCategory': filterCategory
    }
    return render(request, "store/categories.html", context)

def category_products(request, id):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category).order_by('-date_created')

    filterCategory = CategoryFilter(request.GET, queryset=products)
    products = filterCategory.qs

    paginatedProduct = Paginator(filterCategory.qs, 8)
    product_page_number = request.GET.get('page')
    product_page_obj = paginatedProduct.get_page(product_page_number)

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    itemNumber = 0

    if request.user.is_authenticated:
        for product in product_page_obj:
            for item in items:  
                if product == item.product:
                    product.in_cart = True
                    productItems = product.orderitem_set.filter(order=order)
                    itemNumber = sum([item.quantity for item in productItems])
    else:
        for product in product_page_obj:
            for item in items:  
                if product.id == item['id']:
                    product.in_cart = True
                    itemNumber = item['quantity']

    context = {
        'products': products,
        'category': category,
        'cartItems': cartItems,
        'itemNumber': itemNumber,
        'filterItem': filterCategory,
        'product_page_obj': product_page_obj
    }
    return render(request, "store/category_products.html", context)

def tags(request):
    tags = Tag.objects.all().order_by('name')

    filterTag = SearchTag(request.GET, queryset=tags)
    tags = filterTag.qs

    data = cartData(request)

    cartItems = data['cartItems']

    context = {
        'tags': tags,
        'cartItems': cartItems,
        'filterTag': filterTag
    }
    return render(request, "store/tags.html", context)

def tag_products(request, id):
    tag = Tag.objects.get(id=id)
    products = Product.objects.filter(tag=tag).order_by('-date_created')

    filterTag = TagFilter(request.GET, queryset=products)
    products = filterTag.qs

    paginatedProduct = Paginator(filterTag.qs, 8)
    product_page_number = request.GET.get('page')
    product_page_obj = paginatedProduct.get_page(product_page_number)

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    itemNumber = 0
    
    if request.user.is_authenticated:
        for product in product_page_obj:
            for item in items:  
                if product == item.product:
                    product.in_cart = True
                    productItems = product.orderitem_set.filter(order=order)
                    itemNumber = sum([item.quantity for item in productItems])
    else:
        for product in product_page_obj:
            for item in items:  
                if product.id == item['id']:
                    product.in_cart = True
                    itemNumber = item['quantity']

    context = {
        'products': products,
        'tag': tag,
        'cartItems': cartItems,
        'itemNumber': itemNumber,
        'filterItem': filterTag,
        'product_page_obj': product_page_obj
    }
    return render(request, "store/tag_products.html", context)

@login_required(login_url='store:login')
def favourites(request, pk):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    itemNumber = 0

    user = User.objects.get(id=pk)
    favs = Favourite.objects.filter(user=user)

    filterItem = ItemFilter(request.GET, queryset=favs)
    products = filterItem.qs
    
    paginatedProduct = Paginator(filterItem.qs, 8)
    product_page_number = request.GET.get('page')
    product_page_obj = paginatedProduct.get_page(product_page_number)

    if request.user.is_authenticated:
        for product in product_page_obj:
            for item in items:  
                if product.product == item.product:
                    product.product.in_cart = True
                    productItems = product.product.orderitem_set.filter(order=order)
                    itemNumber = sum([item.quantity for item in productItems])
    else:
        for product in product_page_obj:
            for item in items:  
                if product.product.id == item['id']:
                    product.product.in_cart = True
                    itemNumber = item['quantity']
	
    context = {
        'cartItems': cartItems,
        'product_page_obj': product_page_obj,
        'itemNumber': itemNumber
    }
    return render(request, "store/favourites.html", context)

@login_required(login_url='store:login')
def updateFav(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId:', productId)
    
    user = request.user
    product = Product.objects.get(id=productId)
      
    fav, created= Favourite.objects.get_or_create(user=user, product=product)
    fav.save()

    if action == 'delete':
        fav.delete()

    return JsonResponse('Item was added', safe=False)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'store/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId:', productId)
    print('Action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def updateItemQuantity(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']

    print('ProductId:', productId)
    print('Action:', action)
    print('Quantity:', quantity)    

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + int(quantity))
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - int(quantity))

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def checkout(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'store/checkout.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
    	customer = request.user.customer
    	order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
    	customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id
    status = Order.STATUS[0][0]
    order.status = status

    if int(total) == int(order.get_cart_total):
    	order.complete = True

    order.save()

    if order.shipping == True:
    	ShippingAddress.objects.create(
    	customer=customer,
    	order=order,
        country=data['shipping']['country'],
    	address=data['shipping']['address'],
    	city=data['shipping']['city'],
    	province=data['shipping']['province'],
    	zipcode=data['shipping']['zipcode'],
    	)

    return JsonResponse('Payment submitted..', safe=False)

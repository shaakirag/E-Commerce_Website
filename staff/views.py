from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from store.models import *
from .forms import ProductForm, OrderForm, ImageForm
from .filters import OrderFilter, OrderFilterC, ItemFilter, ProductFilter, SearchRegistered, SearchGuest
from store.decorators import unauthenticated_user

# Create your views here.

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('staff:index'))
        else:
            messages.info(request, 'Username or password is incorrect.')
    return render(request, "staff/login.html")

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('staff:login'))

@staff_member_required(login_url='staff:login')
def index(request):

    orders = Order.objects.filter(complete=True).order_by('-date_ordered')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    filterOrder = OrderFilter(request.GET, queryset=orders)
    orders = filterOrder.qs
    
    paginatedOrder = Paginator(filterOrder.qs, 3)
    order_page_number = request.GET.get('page')
    order_page_obj = paginatedOrder.get_page(order_page_number)

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'filterOrder': filterOrder,
        'order_page_obj': order_page_obj
    }
    return render(request, 'staff/index.html', context)

@staff_member_required(login_url='staff:login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return HttpResponseRedirect(reverse('staff:index'))

    context = {
        'order': order
    }
    return render(request, 'staff/delete_order.html', context)

@staff_member_required(login_url='staff:login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff:index'))

    context = {
        'form': form,
        'order': order
    }
    return render(request, 'staff/update_order.html', context)

@staff_member_required(login_url='staff:login')
def customers(request):
    registered = User.objects.exclude(is_staff=True).order_by('-id')
    guest = Customer.objects.exclude(is_user=True).order_by('-id')
    staff = User.objects.filter(is_staff=True)
    
    filterRegistered = SearchRegistered(request.GET, queryset=registered)
    registered = filterRegistered.qs

    filterGuest = SearchGuest(request.GET, queryset=guest)
    guest = filterGuest.qs

    paginatedRegistered = Paginator(filterRegistered.qs, 5)
    registered_page_number = request.GET.get('page')
    registered_page_obj = paginatedRegistered.get_page(registered_page_number)

    paginatedGuest = Paginator(filterGuest.qs, 5)
    guest_page_number = request.GET.get('page')
    guest_page_obj = paginatedGuest.get_page(guest_page_number)

    context = {
        'registered': registered,
        'guest': guest,
        'staff': staff,
        'filterRegistered': filterRegistered,
        'filterGuest': filterGuest,
        'registered_page_obj': registered_page_obj,
        'guest_page_obj': guest_page_obj
    }
    return render(request, 'staff/customer.html', context)

@staff_member_required(login_url='staff:login')
def registered_profile(request, pk):
    user = User.objects.get(id=pk)
    customer = Customer.objects.get(user=user)

    try:
        orders = customer.order_set.filter(complete=True).order_by('-id')
        count = orders.count()
        address = ShippingAddress.objects.filter(customer=customer).last()
        
        filterOrderC = OrderFilterC(request.GET, queryset=orders)
        orders = filterOrderC.qs         

        #orderitems = OrderItem.objects.all()   

        #filterItem = ItemFilter(request.GET, queryset=orderitems)
        #orderitems = filterItem.qs
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
        'filterOrderC': filterOrderC
        #'filterItem': filterItem
    }
    return render(request, 'staff/registered_profile.html', context)

@staff_member_required(login_url='staff:login')
def guest_profile(request, pk):
    guest = Customer.objects.get(id=pk)

    try:
        orders = guest.order_set.filter(complete=True).order_by('-id')
        count = orders.count()
        address = ShippingAddress.objects.filter(customer=guest).last()

        filterOrderC = OrderFilterC(request.GET, queryset=orders)
        orders = filterOrderC.qs

        #orderitems = OrderItem.objects.all()    

        #filterItem = ItemFilter(request.GET, queryset=orderitems)
        #orderitems = filterItem.qs
    except:
        orders = {}
        count = 0
        address = {}
        filterItem = {}
        filterOrderC = {}

    context = {
        'guest': guest,
        'count': count,
        'orders': orders,
        'address': address,
        'filterOrderC': filterOrderC
        #'filterItem': filterItem
    }

    return render(request, 'staff/guest_profile.html', context)

@staff_member_required(login_url='staff:login')
def createProduct(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff:products'))

    context = {
        'form': form
    }
    return render(request, 'staff/crud.html', context)

@staff_member_required(login_url='staff:login')
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff:products'))

    context = {
        'form': form
    }
    return render(request, 'staff/crud.html', context)

@staff_member_required(login_url='staff:login')
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(reverse('staff:products'))

    context = {
        'product': product
    }
    return render(request, 'staff/delete_product.html', context)

@staff_member_required(login_url='staff:login')
def products(request):
    products = Product.objects.all().order_by('-date_created')

    filterProduct = ProductFilter(request.GET, queryset=products)
    products = filterProduct.qs

    paginatedProduct = Paginator(filterProduct.qs, 5)
    product_page_number = request.GET.get('page')
    product_page_obj = paginatedProduct.get_page(product_page_number)

    context = {
        'products': products,
        'filterProduct': filterProduct,
        'product_page_obj': product_page_obj
    }
    return render(request, 'staff/products.html', context)

@staff_member_required(login_url='staff:login')
def product_details(request, pk):
    product = Product.objects.get(id=pk)
        
    context = {
        'product': product
    }
    return render(request, "staff/product_details.html", context)

@staff_member_required(login_url='staff:login')
def addImages(request, pk):
    ImageFormSet = inlineformset_factory(Product, Image, fields=('image',), extra=5)
    product = Product.objects.get(id=pk)
    formset = ImageFormSet(instance=product)

    if request.method == "POST":
        formset = ImageFormSet(request.POST, request.FILES, instance=product)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('staff:products'))

    context = {
        'formset': formset
    }
    return render(request, 'staff/add_images.html', context)

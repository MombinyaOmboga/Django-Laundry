from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import AddServiceForm, AddToCartForm, AddServiceToCartForm
from .models import Cart, ServiceCart


def home(request):
    context = {}
    return render(request, 'laundry/home.html', context)

def landing(request):
    context = {}
    return render(request, 'laundry/landing.html', context)

def about(request):
    context={}
    return render(request, 'laundry/about.html', context)

from django.contrib import messages


def add_service(request):
    if request.method == 'POST':
        form = AddServiceForm(request.POST)

        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.save()
            messages.success(request, 'New service added successfully!')
            return redirect('add-service')
        else:
            messages.warning(request, 'Sorry, something went wrong.')
            return redirect('add-service')
    else:
        form = AddServiceForm()
        context = {'form': form}
        return render(request, 'laundry/add_service.html', context)


def add_to_cart(request):
    if request.method == 'POST':

        form = AddToCartForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.save()
            request.session['cart_id'] = var.id
            return redirect('add-service-to-cart')
        else:
            messages.warning(request, 'Sorry, Something went wrong!')
            return redirect('add-to-cart')
        
    else:
        form = AddToCartForm()
        context = {'form': form}
        return render(request, 'laundry/add_to_cart.html', context)

def add_services_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            cart = Cart.objects.get(id=request.session['cart_id'])
            var.cart = cart
            var.save()
            get_obj = ServiceCart.objects.filter(cart=cart)
            count = 0
            for obj in get_obj:
                calc = obj.service.price * cart.clothes_amount
                count = count+calc
                cart.total_amount = count
                cart.save 

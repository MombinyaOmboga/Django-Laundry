from django.contrib import messages
from django.shortcuts import redirect, render

from payment.models import Wallet

from .forms import AddServiceForm, AddServiceToCartForm, AddToCartForm, CheckOutForm
from .models import Cart, Checkout, ServiceCart


def home(request):
    context = {}
    return render(request, 'laundry/home.html', context)

def landing(request):
    context = {}
    return render(request, 'laundry/landing.html', context)

def about(request):
    context = {}
    return render(request, 'laundry/about.html', context)

def add_service(request):
    if request.method == 'POST':
        form = AddServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
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
            cart_item = form.save(commit=False)
            cart_item.user = request.user
            cart_item.save()
            request.session['cart_id'] = cart_item.id
            return redirect('add-services-to-cart')
        else:
            messages.warning(request, 'Sorry, Something went wrong!')
            return redirect('add-to-cart')
        
    else:
        form = AddToCartForm()
        context = {'form': form}
        return render(request, 'laundry/add_to_cart.html', context)

from django.db.models import Sum


def add_services_to_cart(request):
    if request.method == 'POST':
        form = AddServiceToCartForm(request.POST)
        if form.is_valid():
            service_cart_item = form.save(commit=False)
            service_cart_item.user = request.user
            cart = Cart.objects.get(id=request.session['cart_id'])
            service_cart_item.cart = cart
            service_cart_item.save()
            messages.info(request, 'A service has been added to your cart')
            return redirect('add-services-to-cart')
        else:
            print(form.errors)
            messages.warning(request, 'Something went wrong')
            return redirect('add-services-to-cart')

    else:
        form = AddServiceToCartForm()
        cart = Cart.objects.get(id=request.session['cart_id'])
        get_obj = ServiceCart.objects.filter(cart=cart)
        
        # Calculate the total amount
        total_amount = get_obj.aggregate(Sum('service__price'))['service__price__sum']
        cart.total_amount = total_amount or 0
        cart.save()
        
        context = {'form': form, 'get_obj': get_obj}
        return render(request, 'laundry/add_service_to_cart.html', context)

def delete_service_from_cart(request, pk):
    service_cart_item = ServiceCart.objects.get(pk=pk)
    service_cart_item.delete()

    cart = Cart.objects.get(id=request.session['cart_id'])
    get_obj = ServiceCart.objects.filter(cart=cart)
    count = 0
    for obj in get_obj:
        calc = obj.service.price * cart.clothes_amount
        count += calc
    cart.total_amount = count
    cart.save()
    return redirect('add-services-to-cart')

def checkout_here(request):
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            cart_id = request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
            var.cart = cart
            var.save()
            context = {'cart':cart}
            return render(request, 'payment/make_payment_from_wallet.html')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('checkout-here')
    else:
        form = CheckOutForm()
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        get_obj = ServiceCart.objects.filter(cart=cart)
        context = {'form': form, 'cart': cart, 'get_obj': get_obj}
        return render(request, 'laundry/checkout_here.html', context)
     
def pay_for_laundry(request):
    cart = Cart.objects.get(id=request.session['cart_id'])
    wallet = Wallet.objects.get(user=request.user)
    if wallet.balance >= wallet.balance:
        wallet.balance = wallet.balance - cart.total_amount
        cart.is_verified = True
        cart.save()
        wallet.save()
        messages.info(request, 'Payment completed!, Laundry Process has been Initiated')
        return redirect('home')
    
    else:
        messages.warning(request, 'Sorry, insufficient funds in your wallet!')

    
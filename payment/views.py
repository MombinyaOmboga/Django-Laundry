from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Payment, Wallet


def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        email = request.POST.GET('email')

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()

        context = {
            'payment':payment,
            'paystack_pub_key':pk,
            'amount_value':payment.amount_value(),
        }

        return render(request, 'payment/make_payment.html', context)
    return render(request, 'payment/pre_payment.html')
def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance = wallet.balance + payment.amount
        wallet.save()
        messages.info(request, f'Your wallet has been funded KSH:{payment.amount}')
        return redirect('home')
    else:
        messages.warning(request, 'something went wrong, try again')
        return redirect('home')
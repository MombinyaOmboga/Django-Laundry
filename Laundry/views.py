from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddServiceForm

def add_service(request):
    if request.method == 'POST':
        form = AddServiceForm(request.POST)

        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.save()
            messages.info(request, 'New service Added!')
            return redirect('add-service')
    
        else:
            messages.warning(request, 'sorry. Something went Wrong')
            return redirect('add-service')
    
    else:
        form = AddServiceForm()
        context = {'form': form}
        return render(request, 'Laundry/add_service.html', context)

def add_to_cart(request):
    pass
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from users.form import RegisterUserForm


def register_user(request):
    print("Inside register_user view")  # Debug statement

    if request.method == 'POST':
        print("POST request received")  # Debug statement

        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug statement

            form.save()
            messages.info(request, 'Account created. Please login')
            return redirect('login')
        else:
            print("Form is invalid")  # Debug statement

            messages.warning(request, "Sorry. Something went wrong")
    else:
        print("GET request received")  # Debug statement

        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

    
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')
        
        else:
            messages.warning(request, 'Sorry, something went wrong')
            return redirect('login')
        
    else:
        return render(request, 'users/login.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')

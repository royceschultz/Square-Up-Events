from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        filled_form = UserRegisterForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            username = filled_form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
        else:
            messages.warning(request,'Something is wrong with your form')
            return render(request,'register.html',{'form':filled_form})
    else:
        form = UserRegisterForm()
    return render(request, 'register.html',{'form':form})

@login_required
def profile(request):
    return render(request, 'profile.html')

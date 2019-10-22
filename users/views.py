from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, EditProfileForm

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
            return render(request,'users/register.html',{'form':filled_form})
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def edit_profile():
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            return redirect('users/profile.html')

        else:
            form = EditProfileForm(instance = request.user)
            args = {'form' : form}
            return render(request, 'users/edit_profile.html', args)

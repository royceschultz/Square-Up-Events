from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404

from.models import User
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
def profile(request, id):
    try:
        user = User.objects.get(id=id)
        print(user)
    except User.DoesNotExist:
        raise Http404('Could not find user')
    return render(request, 'users/profile.html',{'userProfile':user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            messages.success(request,f'Changes have been made to your form')
            return redirect('/profile')
        else:
            messages.warning(request,'Something is wrong with your form')
            return render(request, 'users/edit_profile.html', {'form' : form})

    else:
        form = EditProfileForm(instance = request.user)
        args = {'form' : form}
        return render(request, 'users/edit_profile.html', args)

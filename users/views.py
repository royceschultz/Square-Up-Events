from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from.models import User
from .forms import (
    UserRegisterForm,
    EditProfileForm,
    ProfileUpdateForm,

)

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
def change_password(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(data = request.POST, user = request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.info(request, 'Your password has been changed successfully!')
            return redirect('profile', request.user.id)

        else:
            messages.warning(request,'Something is wrong with your form')
            return redirect('change password')


    else:
        pass_form = PasswordChangeForm(user = request.user)
        args = {'pass_form': pass_form}
        return render(request, 'users/change_password.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = EditProfileForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Changes have been made to your form')
            return redirect('profile', request.user.id)
        else:
            messages.warning(request,'Something is wrong with your form')
            #return render(request, 'users/edit_profile.html', {'form' : form})

    else:
        u_form = EditProfileForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    args = {'u_form' : u_form,
            'p_form' : p_form}
    return render(request, 'users/edit_profile.html', args)

def about(request):
    return render(request, 'about.html')

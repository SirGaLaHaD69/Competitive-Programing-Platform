from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import DetailView
from . import models
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.forms import formset_factory
from cp_app.models import UserProfileInfo,Problem,Tag,Author
from cp_app.forms import UserForm, UserProfileInfoForm
import random
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
def is_valid_queryparam(param):
    return param != '' and param is not None

# Create your views here.
# @login_required
# def add_problems(request):
#     name=request.GET.get('title_of_problem')
#     author=request.GET.get('author')
#     rating=request.GET.get('rating')
#     desc=request.GET.get('description')
#     link=request.GET.get('link')
#     tag='Stack'

@login_required
def index(request):
    # form = SearchForm()
    q2 = Tag.objects.all()
    q1 = Problem.objects.all()
    q3= Author.objects.all()
    # form = SearchForm(request.POST or None)
    tag=request.POST.get('tag_query')
    problem_name=request.POST.get('title_query')
    author=request.POST.get('author_query')
    rating=request.POST.get('rating_query')
    sort_by_rating = request.POST.get('rating_sort')
    print(request.POST)
    if is_valid_queryparam(tag):
        q1 = q1.filter(tag__name__iexact=tag)
    if is_valid_queryparam(problem_name):
        q1 = q1.filter(title__icontains=problem_name)
    if is_valid_queryparam(author):
        q1 = q1.filter(author__name__iexact=author)
    if is_valid_queryparam(rating):
        q1 = q1.filter(rating__iexact=rating)
    if sort_by_rating=='up':
        print('hi')
        q1=q1.order_by('rating')
    elif sort_by_rating=='down':
        q1=q1.order_by('-rating')
    return render(request,'index.html',{ 'problems':q1,'tags':q2,'authors':q3})
def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print("ERROR")
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'register.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})
def discuss(request):
    return render(request,'discuss.html')
def home(request):
    return render(request,'home.html')
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponse("ACCOUNT NOT ACTIVE")
            else:
                messages.error(request,'Username or Password not correct! Try Again!')
                return render(request, 'login.html',{})
        else:
            return render(request, 'login.html',{})
    else:
        return HttpResponseRedirect(reverse('home'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('cp_app:user_login'))

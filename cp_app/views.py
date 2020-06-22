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
from cp_app.models import UserProfileInfo,Problem,Tag,Author,Comment
from cp_app.forms import UserForm,CommentForm, UserProfileInfoForm
import random
import datetime
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
def is_valid_queryparam(param):
    return param != '' and param is not None

# Create your views here.
@login_required
def add_problems(request):
    a1=Author.objects.all()
    t1=Tag.objects.all()
    if request.method=='POST':
        print(request.POST)
        Title=request.POST.get('title_query')
        Auth=request.POST.get('author_query')
        Rat=request.POST.get('rating_query')
        desc=request.POST.get('descript')
        Link=request.POST.get('link_query')
        tag_def=request.POST.getlist('tag_list')
        verified_auth=Author.objects.filter(name__iexact=Auth)
        verified_auth= verified_auth[0]
        p1=Problem(
        title=Title,
        author=verified_auth,
        rating=int(Rat),
        description=desc,
        link=Link,
        reviewed=False,
        )
        p1.save()
        for x in tag_def:
            tn=Tag.objects.filter(name__iexact=x)
            tn=tn[0]
            p1.tag.add(tn)
        p1.save()

    return render(request,'add_problems.html',{ 'authors':a1,'tags':t1})

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
        print(request.POST)
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
# def discuss(request):
#     return render(request,'discuss.html')
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

class ProblemDetailView(DetailView,LoginRequiredMixin):
    model = Problem
    login_url = '/cp_app/login/'
    redirect_field_name='login.html'
    #check

@login_required
def add_comment_to_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.problem = problem
            comment.user=request.user
            comment.save()
            return redirect('cp_app:problem_detail', pk=problem.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    problem_pk = comment.problem.pk
    comment.delete()
    return redirect('cp_app:problem_detail', pk=problem_pk)

from django.db import models
from django.db.models import fields
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView,CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from . models import Task



# Create your views here.
class CustomLoginView(LoginView):
    template_name= 'base/login.html'
    fields='__all__'
    redirect_authenticated_user= True
    
    def get_success_url(self):
        return reverse_lazy('task')


class RegisterPage(FormView):
    template_name='base/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user= True
    success_url = reverse_lazy ('task')

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage,self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin,ListView):
    model= Task
    context_object_name='task'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['task']=context['task'].filter(user=self.request.user)
        context['count']=context['task'].filter(complete=False).count()
        search_input= self.request.GET.get('search-area') or ''
        if search_input:
            context ['task']=context['task'].filter(title__startswith=search_input)

        context['search_input']= search_input
        return context


class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields= ['title','description','complete']
    success_url= reverse_lazy('task')

    def form_valid(self, form) :
        form.instance.user= self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields= ['title','description','complete']
    success_url= reverse_lazy('task')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url= reverse_lazy('task')
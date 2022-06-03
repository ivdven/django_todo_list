from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import Task


class UserRegisterView(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    # If form is valid, logs in user
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)


class UserLoginView(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    template_name = 'app/logout.html'


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'app/home.html'
    context_object_name = 'tasks'

    # Gets user specific data
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['tasks'].filter(
            complete=False).count()  # Counts incomplete tasks

        # Searchbar functionality
        search_input = self.request.GET.get(
            'search-bar') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)
        context['search_input'] = search_input
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'app/forms.html'
    fields = [
        'title',
        'complete'
    ]
    success_url = reverse_lazy('home')

    # Let user create their own tasks
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'app/task_update.html'
    fields = [
        'title',
        'complete'
    ]
    success_url = reverse_lazy('home')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'app/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('home')

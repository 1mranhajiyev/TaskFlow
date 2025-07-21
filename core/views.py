from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,UpdateView,DeleteView
from django.urls import reverse
from .models import Project , Task
from .forms import TaskForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(LoginRequiredMixin,DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # GET istəyi üçün kontekstə boş bir forma əlavə edirik
        context['task_form'] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        # Forma istifadəçinin göndərdiyi POST məlumatları ilə doldurulur
        form = TaskForm(request.POST)

        if form.is_valid():
            # Formanı hələ databazaya yazma, çünki project sahəsi boşdur
            new_task = form.save(commit=False)
            # Project-i URL-dən gələn obyektdən götürüb təyin et
            new_task.project = self.get_object()
            # İndi tam məlumatlı obyekti databazaya yaz
            new_task.assignee = request.user
            new_task.save()
            messages.success(request, f"'{new_task.title}' adlı tapşırıq uğurla yaradıldı.")
            # İstifadəçini yenidən həmin səhifəyə yönləndir (yeni tapşırığı görsün)
            return redirect('project-detail', pk=self.get_object().pk)
        else:
            # Əgər forma düzgün deyilsə, səhifəni yenidən göstər
            # Amma bu dəfə kontekstə səhvləri olan formanı göndər
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            context['task_form'] = form
            return self.render_to_response(context)
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.assignee

    def form_valid(self, form):
        messages.success(self.request, f"'{form.instance.title}' adlı tapşırıq uğurla yeniləndi.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.project.pk})


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'core/task_confirm_delete.html'

    # success_message atributunu buradan silirik

    # Mesajı dinamik yaratmaq üçün bu metodu əlavə edirik
    def get_success_message(self, cleaned_data):
        # self.object burada silinməkdə olan tapşırıqdır
        return f"'{self.object.title}' adlı tapşırıq uğurla silindi."

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.assignee

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.project.pk})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # İstifadəçini databazada yarat
            login(request, user)  # Yaratdıqdan dərhal sonra sistemə daxil et
            return redirect('project-list')  # Layihə siyahısına yönləndir
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'core/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        # Yalnız tapşırığın təyin edildiyi şəxs baxa bilər
        task = self.get_object()
        return self.request.user == task.assignee
    
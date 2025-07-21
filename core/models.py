from django.db import models
from django.contrib.auth.models import User # Django-nun daxili istifadəçi modelini import edirik

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Layihənin Adı")
    description = models.TextField(verbose_name="Açıqlama", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Layihə"
        verbose_name_plural = "Layihələr"
        ordering = ['-created_at']


class Task(models.Model):
    # Status üçün seçimlər (best practice)
    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'

    STATUS_CHOICES = [
        (STATUS_TODO, 'Ediləcək'),
        (STATUS_IN_PROGRESS, 'İcra edilir'),
        (STATUS_DONE, 'Tamamlanıb'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name="Layihə")
    title = models.CharField(max_length=255, verbose_name="Tapşırıq Başlığı")
    description = models.TextField(verbose_name="Açıqlama")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', verbose_name="İstifadəçi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    due_date = models.DateField(verbose_name="Son İcra Tarixi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tapşırıq"
        verbose_name_plural = "Tapşırıqlar"
        ordering = ['-created_at']



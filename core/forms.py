from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # 'status'-u bura əlavə edirik ki, potensial olaraq istifadə edə bilək
        fields = ['title', 'description', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Başlıq',
            'description': 'Açıqlama',
            'status': 'Status',
            'due_date': 'Son İcra Tarixi',
        }

    def __init__(self, *args, **kwargs):
        # Əvvəlcə formanın standart qurulumunu çağırırıq
        super().__init__(*args, **kwargs)

        # Yoxlayırıq: forma mövcud bir obyekt üçün yaradılıb (redaktə) yoxsa yeni (yaratmaq)?
        # `self.instance.pk` o deməkdir ki, bu obyekt artıq databazada var və bir ID-si var.
        if self.instance and self.instance.pk:
            # Bu, redaktə formasıdır. Status sahəsi olduğu kimi qalsın.
            pass
        else:
            # Bu, yeni tapşırıq yaratma formasıdır.
            # Ona görə də 'status' sahəsini formadan silirik.
            del self.fields['status']
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
from .models import Enrollment

class EnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student')
        super().__init__(*args, **kwargs)
        enrolled_ids = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
        self.fields['course'].queryset = Course.objects.exclude(id__in=enrolled_ids)
        
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'marks', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher')
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(teacher=teacher)
        self.fields['student'].queryset = Enrollment.objects.filter(
            course__teacher=teacher
        ).values_list('student', flat=True)
        from accounts.models import User
        self.fields['student'].queryset = User.objects.filter(
            id__in=self.fields['student'].queryset
        )
        
from .models import Routine

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['course', 'day', 'start_time', 'end_time']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher')
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(teacher=teacher)
        
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'message', 'course']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher')
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(teacher=teacher)
        self.fields['course'].required = False
        
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'resource_link', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resource_link': forms.URLInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
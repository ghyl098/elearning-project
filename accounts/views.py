from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import RegisterForm
from courses.models import Course, Enrollment, Grade, Routine

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'home'


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
        context = {
            'total_courses': courses.count(),
            'total_students': Enrollment.objects.filter(course__in=courses).values('student').distinct().count(),
            'total_routines': Routine.objects.filter(course__in=courses).count(),
        }
        return render(request, 'accounts/teacher_dashboard.html', context)
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        context = {
            'total_courses': enrolled_ids.count(),
            'total_grades': Grade.objects.filter(student=request.user).count(),
            'total_routines': Routine.objects.filter(course_id__in=enrolled_ids).count(),
        }
        return render(request, 'accounts/student_dashboard.html', context)
    

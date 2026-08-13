from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Enrollment, Grade, Routine
from .forms import CourseForm

@login_required
def course_list(request):
    if request.user.role == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=enrolled_ids)
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_create(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can create courses.")
        return redirect('course_list')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

from .forms import EnrollForm

@login_required
def enroll_view(request):
    if request.user.role != 'student':
        messages.error(request, "Only students can enroll.")
        return redirect('course_list')
    if request.method == 'POST':
        form = EnrollForm(request.POST, student=request.user)
        if form.is_valid():
            Enrollment.objects.create(student=request.user, course=form.cleaned_data['course'])
            messages.success(request, "Enrolled successfully!")
            return redirect('course_list')
    else:
        form = EnrollForm(student=request.user)
    return render(request, 'courses/enroll_form.html', {'form': form})

from .forms import GradeForm

@login_required
def grade_add(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can add grades.")
        return redirect('course_list')
    if request.method == 'POST':
        form = GradeForm(request.POST, teacher=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade added successfully!")
            return redirect('grade_list')
    else:
        form = GradeForm(teacher=request.user)
    return render(request, 'courses/grade_form.html', {'form': form})

@login_required
def grade_list(request):
    if request.user.role == 'teacher':
        grades = Grade.objects.filter(course__teacher=request.user)
    else:
        grades = Grade.objects.filter(student=request.user)
    return render(request, 'courses/grade_list.html', {'grades': grades})

from .forms import RoutineForm

@login_required
def routine_add(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can add routines.")
        return redirect('course_list')
    if request.method == 'POST':
        form = RoutineForm(request.POST, teacher=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Routine added successfully!")
            return redirect('routine_list')
    else:
        form = RoutineForm(teacher=request.user)
    return render(request, 'courses/routine_form.html', {'form': form})

@login_required
def routine_list(request):
    if request.user.role == 'teacher':
        routines = Routine.objects.filter(course__teacher=request.user)
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        routines = Routine.objects.filter(course_id__in=enrolled_ids)
    return render(request, 'courses/routine_list.html', {'routines': routines})
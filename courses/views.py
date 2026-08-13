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

from .forms import NoticeForm
from .models import Notice

@login_required
def notice_list(request):
    if request.user.role == 'teacher':
        notices = Notice.objects.filter(posted_by=request.user)
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        from django.db.models import Q
        notices = Notice.objects.filter(Q(course_id__in=enrolled_ids) | Q(course__isnull=True))
    return render(request, 'courses/notice_list.html', {'notices': notices})

@login_required
def notice_add(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can post notices.")
        return redirect('notice_list')
    if request.method == 'POST':
        form = NoticeForm(request.POST, teacher=request.user)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.save()
            messages.success(request, "Notice posted successfully!")
            return redirect('notice_list')
    else:
        form = NoticeForm(teacher=request.user)
    return render(request, 'courses/notice_form.html', {'form': form})

@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk, posted_by=request.user)
    notice.delete()
    messages.success(request, "Notice deleted.")
    return redirect('notice_list')

from .models import Lesson
from .forms import LessonForm

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'teacher' and course.teacher != request.user:
        messages.error(request, "You don't have access to this course.")
        return redirect('course_list')
    if request.user.role == 'student' and not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')

    lessons = course.lessons.all()
    enrolled_students = None
    if request.user.role == 'teacher':
        enrolled_students = Enrollment.objects.filter(course=course).select_related('student')

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'enrolled_students': enrolled_students,
    })

@login_required
def lesson_add(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson added successfully!")
            return redirect('course_detail', pk=course.pk)
    else:
        form = LessonForm()
    return render(request, 'courses/lesson_form.html', {'form': form, 'course': course})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'editing': True})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    course.delete()
    messages.success(request, "Course deleted.")
    return redirect('course_list')

@login_required
def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk, course__teacher=request.user)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade, teacher=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade updated successfully!")
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade, teacher=request.user)
    return render(request, 'courses/grade_form.html', {'form': form, 'editing': True})

@login_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk, course__teacher=request.user)
    grade.delete()
    messages.success(request, "Grade deleted.")
    return redirect('grade_list')

@login_required
def routine_edit(request, pk):
    routine = get_object_or_404(Routine, pk=pk, course__teacher=request.user)
    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=routine, teacher=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Routine updated successfully!")
            return redirect('routine_list')
    else:
        form = RoutineForm(instance=routine, teacher=request.user)
    return render(request, 'courses/routine_form.html', {'form': form, 'editing': True})

@login_required
def routine_delete(request, pk):
    routine = get_object_or_404(Routine, pk=pk, course__teacher=request.user)
    routine.delete()
    messages.success(request, "Routine deleted.")
    return redirect('routine_list')
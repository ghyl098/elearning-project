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

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    grouped = {}
    for r in routines:
        day_name = r.get_day_display()
        grouped.setdefault(day_name, []).append(r)

    schedule_by_day = []
    for day in day_order:
        if day in grouped:
            day_routines = sorted(grouped[day], key=lambda r: r.start_time)
            schedule_by_day.append({'day': day, 'routines': day_routines})

    return render(request, 'courses/routine_list.html', {
        'routines': routines,
        'schedule_by_day': schedule_by_day,
    })

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

from .models import Lesson, Assignment, Submission
from .forms import LessonForm, AssignmentForm, SubmissionForm

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
    assignments = course.assignments.all()
    enrolled_students = None
    student_submissions = {}

    if request.user.role == 'teacher':
        enrolled_students = Enrollment.objects.filter(course=course).select_related('student')
    else:
        subs = Submission.objects.filter(assignment__course=course, student=request.user)
        student_submissions = {s.assignment_id: s for s in subs}

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'assignments': assignments,
        'student_submissions': student_submissions,
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

@login_required
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk, course__teacher=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully!")
            return redirect('course_detail', pk=lesson.course.pk)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/lesson_form.html', {'form': form, 'course': lesson.course, 'editing': True})

@login_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk, course__teacher=request.user)
    course_pk = lesson.course.pk
    lesson.delete()
    messages.success(request, "Lesson deleted.")
    return redirect('course_detail', pk=course_pk)

@login_required
def assignment_add(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can add assignments.")
        return redirect('course_list')
    if request.method == 'POST':
        form = AssignmentForm(request.POST, teacher=request.user)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, "Assignment added successfully!")
            return redirect('course_detail', pk=assignment.course.pk)
    else:
        form = AssignmentForm(teacher=request.user)
    return render(request, 'courses/assignment_form.html', {'form': form})

@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__teacher=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment, teacher=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully!")
            return redirect('course_detail', pk=assignment.course.pk)
    else:
        form = AssignmentForm(instance=assignment, teacher=request.user)
    return render(request, 'courses/assignment_form.html', {'form': form, 'editing': True})

@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__teacher=request.user)
    course_pk = assignment.course.pk
    assignment.delete()
    messages.success(request, "Assignment deleted.")
    return redirect('course_detail', pk=course_pk)

@login_required
def submission_add(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.user.role != 'student':
        messages.error(request, "Only students can submit assignments.")
        return redirect('course_list')
    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=existing)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect('course_detail', pk=assignment.course.pk)
    else:
        form = SubmissionForm(instance=existing)
    return render(request, 'courses/submission_form.html', {'form': form, 'assignment': assignment})

from django.utils import timezone
from .forms import GradeSubmissionForm

@login_required
def submission_list(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__teacher=request.user)
    submissions = assignment.submissions.select_related('student')
    return render(request, 'courses/submission_list.html', {
        'assignment': assignment,
        'submissions': submissions,
    })

@login_required
def submission_grade(request, pk):
    submission = get_object_or_404(Submission, pk=pk, assignment__course__teacher=request.user)
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            graded = form.save(commit=False)
            graded.graded_at = timezone.now()
            graded.save()
            messages.success(request, "Feedback saved successfully!")
            return redirect('submission_list', pk=submission.assignment.pk)
    else:
        form = GradeSubmissionForm(instance=submission)
    return render(request, 'courses/submission_grade.html', {'form': form, 'submission': submission})

from .models import Attendance
from .forms import AttendanceFilterForm

@login_required
def attendance_select(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can mark attendance.")
        return redirect('course_list')
    if request.method == 'POST':
        form = AttendanceFilterForm(request.POST, teacher=request.user)
        if form.is_valid():
            course = form.cleaned_data['course']
            date = form.cleaned_data['date']
            return redirect('attendance_mark', pk=course.pk, date_str=date.strftime('%Y-%m-%d'))
    else:
        form = AttendanceFilterForm(teacher=request.user)
    return render(request, 'courses/attendance_select.html', {'form': form})


@login_required
def attendance_mark(request, pk, date_str):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    enrolled_students = Enrollment.objects.filter(course=course).select_related('student')

    existing = Attendance.objects.filter(course=course, date=date_str)
    existing_map = {a.student_id: a.status for a in existing}

    if request.method == 'POST':
        for enrollment in enrolled_students:
            status = request.POST.get(f'status_{enrollment.student.id}', 'absent')
            Attendance.objects.update_or_create(
                course=course, student=enrollment.student, date=date_str,
                defaults={'status': status}
            )
        messages.success(request, "Attendance saved successfully!")
        return redirect('attendance_select')

    attendance_rows = []
    for enrollment in enrolled_students:
        current_status = existing_map.get(enrollment.student.id, 'present')
        attendance_rows.append({
            'student': enrollment.student,
            'is_present': current_status == 'present',
        })

    return render(request, 'courses/attendance_mark.html', {
        'course': course,
        'date_str': date_str,
        'attendance_rows': attendance_rows,
    })


@login_required
def attendance_report(request):
    if request.user.role == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
        course_data = []
        for course in courses:
            total = Attendance.objects.filter(course=course).values('date').distinct().count()
            course_data.append({'course': course, 'total_days': total})
        return render(request, 'courses/attendance_report.html', {'course_data': course_data, 'is_teacher': True})
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=enrolled_ids)
        course_data = []
        for course in courses:
            records = Attendance.objects.filter(course=course, student=request.user)
            total = records.count()
            present = records.filter(status='present').count()
            percent = round((present / total) * 100, 1) if total > 0 else 0
            course_data.append({'course': course, 'total': total, 'present': present, 'percent': percent})
        return render(request, 'courses/attendance_report.html', {'course_data': course_data, 'is_teacher': False})
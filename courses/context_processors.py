from django.db.models import Q
from .models import Notice, Enrollment

def navbar_notices(request):
    if not request.user.is_authenticated:
        return {}
    if request.user.role == 'teacher':
        notices = Notice.objects.filter(posted_by=request.user)[:5]
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        notices = Notice.objects.filter(Q(course_id__in=enrolled_ids) | Q(course__isnull=True))[:5]
    return {'navbar_notices': notices}
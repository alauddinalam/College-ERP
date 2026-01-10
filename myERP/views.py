from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Profile   # optional, if still needed elsewhere
from .models import StudentProfile, Attendance, Subject, StudentSubject, FeeStructure, FeePayment, Notice
from django import forms
from .forms import ProfileForm
from django.db.models import Count, Q, Sum
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models


def attendance(request):
    # Get student's profile
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('myERP:dashboard')

    # Create sample attendance data if none exists
    if not Attendance.objects.filter(student=student_profile).exists():
        subjects = ['Mathematics', 'Physics', 'Computer Science', 'Chemistry', 'English']
        base_date = timezone.now().date() - timedelta(days=60)

        for i in range(60):
            current_date = base_date + timedelta(days=i)
            if current_date.weekday() < 5:  # Monday to Friday
                for subject in subjects:
                    # Random attendance with bias towards present
                    import random
                    status = 'present' if random.random() > 0.15 else ('absent' if random.random() > 0.5 else 'late')
                    time_slot = {'Mathematics': '09:00', 'Physics': '10:30', 'Computer Science': '14:00', 'Chemistry': '11:30', 'English': '13:00'}[subject]

                    Attendance.objects.create(
                        student=student_profile,
                        subject=subject,
                        date=current_date,
                        status=status,
                        time=datetime.strptime(time_slot, '%H:%M').time(),
                        remarks='On time' if status == 'present' else ('Medical leave' if status == 'absent' else 'Late by 10 min')
                    )

    # Get attendance data
    attendance_records = Attendance.objects.filter(student=student_profile).order_by('-date')

    # Calculate statistics
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='present').count()
    absent_days = attendance_records.filter(status='absent').count()
    late_days = attendance_records.filter(status='late').count()

    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    # Subject-wise attendance
    subject_stats = attendance_records.values('subject').annotate(
        total=Count('id'),
        present=Count('id', filter=Q(status='present')),
        absent=Count('id', filter=Q(status='absent')),
        late=Count('id', filter=Q(status='late'))
    ).order_by('subject')

    # Calculate percentages for each subject
    for stat in subject_stats:
        stat['percentage'] = (stat['present'] / stat['total'] * 100) if stat['total'] > 0 else 0
        stat['status'] = 'Excellent' if stat['percentage'] >= 90 else 'Good' if stat['percentage'] >= 80 else 'Low' if stat['percentage'] >= 75 else 'Critical'

    # Monthly data for chart (last 8 months)
    today = timezone.now().date()
    monthly_data = []
    labels = []
    for i in range(7, -1, -1):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)  # last day of month
        month_end = month_end - timedelta(days=month_end.day)

        month_records = attendance_records.filter(date__range=[month_start, month_end])
        if month_records.exists():
            month_present = month_records.filter(status='present').count()
            month_total = month_records.count()
            percentage = (month_present / month_total * 100) if month_total > 0 else 0
        else:
            percentage = 0

        monthly_data.append(round(percentage, 1))
        labels.append(month_start.strftime('%b'))

    # Current streak
    current_streak = 0
    check_date = today
    while True:
        day_records = attendance_records.filter(date=check_date, status='present')
        if day_records.exists():
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    context = {
        'attendance_records': attendance_records[:20],  # Last 20 records
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'late_days': late_days,
        'attendance_percentage': round(attendance_percentage, 1),
        'subject_stats': subject_stats,
        'monthly_labels': labels,
        'monthly_data': monthly_data,
        'current_streak': current_streak,
        'today': today,
    }

    return render(request, 'attendance.html', context)


@login_required
def fee(request):
    # Get student's profile
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('myERP:dashboard')

    # Create sample fee structure if none exists
    if not FeeStructure.objects.exists():
        fee_data = [
            {'semester': 1, 'total_fee': 50000, 'tuition_fee': 35000, 'exam_fee': 5000, 'library_fee': 2000, 'other_fees': 8000, 'academic_year': '2025-26'},
            {'semester': 2, 'total_fee': 55000, 'tuition_fee': 38000, 'exam_fee': 5500, 'library_fee': 2200, 'other_fees': 9300, 'academic_year': '2025-26'},
            {'semester': 3, 'total_fee': 55000, 'tuition_fee': 38000, 'exam_fee': 5500, 'library_fee': 2200, 'other_fees': 9300, 'academic_year': '2025-26'},
            {'semester': 4, 'total_fee': 60000, 'tuition_fee': 41000, 'exam_fee': 6000, 'library_fee': 2400, 'other_fees': 10600, 'academic_year': '2025-26'},
        ]

        for fee in fee_data:
            FeeStructure.objects.create(**fee)

    # Create sample payments if none exist
    if not FeePayment.objects.filter(student=student_profile).exists():
        from datetime import date
        payments_data = [
            {'semester': 1, 'amount': 50000, 'payment_date': date(2025, 8, 1), 'payment_method': 'online', 'transaction_id': 'TXN001'},
            {'semester': 2, 'amount': 40000, 'payment_date': date(2025, 8, 15), 'payment_method': 'bank_transfer', 'transaction_id': 'TXN002'},
            {'semester': 3, 'amount': 50000, 'payment_date': date(2025, 9, 1), 'payment_method': 'online', 'transaction_id': 'TXN003'},
        ]

        for payment in payments_data:
            FeePayment.objects.create(student=student_profile, **payment)

    # Get fee data
    fee_structures = FeeStructure.objects.all()
    payments = FeePayment.objects.filter(student=student_profile)

    # Calculate totals
    total_fee = sum(fee.total_fee for fee in fee_structures)
    total_paid = sum(payment.amount for payment in payments)
    total_due = total_fee - total_paid

    # Semester-wise breakdown
    semester_data = []
    for fee in fee_structures:
        paid = payments.filter(semester=fee.semester).aggregate(total=Sum('amount'))['total'] or 0
        due = fee.total_fee - paid
        semester_data.append({
            'semester': fee.semester,
            'total_fee': fee.total_fee,
            'paid': paid,
            'due': due,
            'percentage': (paid / fee.total_fee * 100) if fee.total_fee > 0 else 0
        })

    # Recent payments
    recent_payments = payments.order_by('-payment_date')[:5]

    context = {
        'total_fee': total_fee,
        'total_paid': total_paid,
        'total_due': total_due,
        'semester_data': semester_data,
        'recent_payments': recent_payments,
        'payment_percentage': (total_paid / total_fee * 100) if total_fee > 0 else 0,
    }

    return render(request, 'fee.html', context)


@login_required
def subjects(request):
    # Get student's profile
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('myERP:dashboard')

    # Create sample subjects if none exist
    if not Subject.objects.exists():
        subjects_data = [
            {'name': 'Computer Science', 'code': 'CS101', 'credits': 4, 'instructor': 'Dr. Smith', 'description': 'Introduction to Programming', 'semester': 1},
            {'name': 'Data Structures', 'code': 'CS201', 'credits': 3, 'instructor': 'Prof. Johnson', 'description': 'Algorithms and Data Structures', 'semester': 2},
            {'name': 'Web Development', 'code': 'CS301', 'credits': 4, 'instructor': 'Ms. Davis', 'description': 'Full Stack Web Development', 'semester': 3},
            {'name': 'AI & ML', 'code': 'CS401', 'credits': 3, 'instructor': 'Dr. Wilson', 'description': 'Artificial Intelligence', 'semester': 4},
            {'name': 'Cyber Security', 'code': 'CS501', 'credits': 3, 'instructor': 'Prof. Brown', 'description': 'Network Security', 'semester': 5},
            {'name': 'Mobile App Dev', 'code': 'CS601', 'credits': 4, 'instructor': 'Mr. Taylor', 'description': 'Android Development', 'semester': 6},
        ]

        for subj_data in subjects_data:
            Subject.objects.create(**subj_data)

    # Get or create student subjects
    all_subjects = Subject.objects.all()
    student_subjects = []
    for subject in all_subjects:
        student_subj, created = StudentSubject.objects.get_or_create(
            student=student_profile,
            subject=subject
        )
        student_subjects.append(student_subj)

    # Calculate subject statistics
    subject_stats = []
    for student_subj in student_subjects:
        attendance_count = Attendance.objects.filter(
            student=student_profile,
            subject=student_subj.subject.name
        ).count()

        present_count = Attendance.objects.filter(
            student=student_profile,
            subject=student_subj.subject.name,
            status='present'
        ).count()

        attendance_percentage = (present_count / attendance_count * 100) if attendance_count > 0 else 0

        subject_stats.append({
            'subject': student_subj.subject,
            'enrolled_date': student_subj.enrolled_date,
            'attendance_count': attendance_count,
            'present_count': present_count,
            'attendance_percentage': round(attendance_percentage, 1),
            'grade': student_subj.grade,
        })

    context = {
        'student_subjects': student_subjects,
        'subject_stats': subject_stats,
        'total_subjects': len(student_subjects),
        'current_semester': student_profile.semester or 1,
    }

    return render(request, 'subjects.html', context)


@login_required
def notices(request):
    return render(request, 'notices.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# ✅ Dynamic ModelForm for StudentProfile
# ProfileForm = forms.modelform_factory(StudentProfile, exclude=['user'])


@login_required
def profile(request):
    # ✅ Get or create profile for the logged-in user
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # ✅ Handle file uploads (profile image)
        form = ProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('myERP:profile')  # Refresh page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=student_profile)

    # ✅ Prepare data for profile.html
    context = {
        'form': form,
        'profile': student_profile,
        'name': student_profile.full_name or request.user.get_full_name() or request.user.username,
        'email': student_profile.email or request.user.email,
        'roll_no': student_profile.roll_no,
        'dob': student_profile.dob,
        'gender': student_profile.gender,
        'blood_group': student_profile.blood_group,
        'course': student_profile.course,
        'branch': student_profile.branch,
        'semester': student_profile.semester,
        'cgpa': student_profile.cgpa,
        'phone': student_profile.phone,
        'address': student_profile.address,
        'about_me': student_profile.about_me,
        'profile_image': student_profile.profile_image.url if student_profile.profile_image else None,
    }

    return render(request, 'profile.html', context)

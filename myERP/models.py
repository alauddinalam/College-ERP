from django.db import models
from django.contrib.auth.models import User
import os


def user_profile_image_path(instance, filename):
    """
    Save profile images to MEDIA_ROOT/profile_images/<username>/<filename>
    """
    return os.path.join('profile_images', instance.user.username, filename)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Personal Details
    full_name = models.CharField(max_length=100, blank=True, null=True)
    roll_no = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    
    # Academic Details
    course = models.CharField(max_length=50, blank=True, null=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)
    cgpa = models.FloatField(blank=True, null=True)
    
    # Contact Details
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # About
    about_me = models.TextField(blank=True, null=True)

    # ✅ Profile image setup
    profile_image = models.ImageField(
        upload_to=user_profile_image_path,
        default='profile_images/avatar.png',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name or self.user.username


class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ])
    time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'subject', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField()
    instructor = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    semester = models.IntegerField()
    department = models.CharField(max_length=50, default='Computer Science')

    def __str__(self):
        return f"{self.code} - {self.name}"


class StudentSubject(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        unique_together = ['student', 'subject']

    def __str__(self):
        return f"{self.student} - {self.subject}"


class FeeStructure(models.Model):
    semester = models.IntegerField()
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2)
    other_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    academic_year = models.CharField(max_length=20)

    def __str__(self):
        return f"Semester {self.semester} - {self.academic_year}"


class FeePayment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    semester = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=[
        ('online', 'Online'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque')
    ])
    transaction_id = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - Sem {self.semester} - ₹{self.amount}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority')
    ], default='medium')
    category = models.CharField(max_length=50, choices=[
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('events', 'Events'),
        ('maintenance', 'Maintenance'),
        ('general', 'General')
    ], default='general')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    contact_info = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return self.title

    def is_expired(self):
        if self.expiry_date:
            from django.utils import timezone
            return timezone.now() > self.expiry_date
        return False

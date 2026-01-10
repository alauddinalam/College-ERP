from django.contrib import admin
from .models import StudentProfile, Attendance, Subject, StudentSubject, FeeStructure, FeePayment, Notice

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_no', 'course', 'branch', 'semester', 'email', 'phone')
    search_fields = ('full_name', 'roll_no', 'email', 'user__username')
    list_filter = ('course', 'branch', 'semester', 'gender')
    ordering = ('full_name',)
    readonly_fields = ('user',)

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'roll_no')
        }),
        ('Personal Details', {
            'fields': ('dob', 'gender', 'blood_group', 'profile_image')
        }),
        ('Academic Details', {
            'fields': ('course', 'branch', 'semester', 'cgpa')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'address')
        }),
        ('About', {
            'fields': ('about_me',)
        }),
    )

# Register your models here.
# admin.site.register(StudentProfile)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'time')
    search_fields = ('student__full_name', 'subject', 'status')
    list_filter = ('status', 'date', 'subject')
    ordering = ('-date',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits', 'instructor', 'semester', 'department')
    search_fields = ('name', 'code', 'instructor')
    list_filter = ('semester', 'department', 'credits')

@admin.register(StudentSubject)
class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'enrolled_date', 'grade')
    search_fields = ('student__full_name', 'subject__name')
    list_filter = ('enrolled_date', 'grade')

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('semester', 'total_fee', 'academic_year')
    search_fields = ('academic_year', 'semester')
    list_filter = ('academic_year', 'semester')

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'amount', 'payment_date', 'payment_method')
    search_fields = ('student__full_name', 'transaction_id')
    list_filter = ('payment_method', 'payment_date', 'semester')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'category', 'posted_by', 'posted_date', 'is_active')
    search_fields = ('title', 'content', 'posted_by__username')
    list_filter = ('priority', 'category', 'is_active', 'posted_date')
    ordering = ('-posted_date',)
    readonly_fields = ('posted_date',)
from django import forms
from .models import StudentProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile  
        exclude = ['user']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select'),
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other', 'Other'),
                ('Prefer not to say', 'Prefer not to say'),
            ]),
            'blood_group': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select'),
                ('A+', 'A+'),
                ('A-', 'A-'),
                ('B+', 'B+'),
                ('B-', 'B-'),
                ('AB+', 'AB+'),
                ('AB-', 'AB-'),
                ('O+', 'O+'),
                ('O-', 'O-'),
            ]),
            'course': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select'),
                ('BCA', 'BCA'),
                ('B.Tech', 'B.Tech'),
                ('BBA', 'BBA'),
                ('MCA', 'MCA'),
            ]),
            'branch': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select'),
                ('CS', 'Computer Science'),
                ('IT', 'Information Technology'),
                ('AI/ML', 'AI/ML'),
                ('EC', 'Electronics and Communication'),
            ]),
            'semester': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select'),
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),
                (6, '6'),
                (7, '7'),
                (8, '8'),
            ]),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

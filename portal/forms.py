from django import forms
from .models import Student


class ApplicationForm(forms.Form):
    """The form a student fills to apply for an internship."""
    student = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('roll_no'),
        empty_label='Select your roll number',
    )
    resume_file = forms.FileField(
        required=False,
        label='Upload your resume (optional if you already uploaded one)',
    )
    cover_letter = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label='Short cover letter (optional)',
    )

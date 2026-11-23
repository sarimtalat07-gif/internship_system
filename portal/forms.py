from django import forms
from django.core.validators import FileExtensionValidator

from .models import Student

MAX_RESUME_MB = 5


class ApplicationForm(forms.Form):
    """The form a student fills to apply for an internship."""
    student = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('roll_no'),
        empty_label='Select your roll number',
    )
    resume_file = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(['pdf'])],
        label='Upload your resume as PDF (optional - your latest saved resume is used if you skip this)',
    )
    cover_letter = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label='Short cover letter (optional)',
    )

    def clean_resume_file(self):
        f = self.cleaned_data.get('resume_file')
        if f and f.size > MAX_RESUME_MB * 1024 * 1024:
            raise forms.ValidationError(f'Resume must be under {MAX_RESUME_MB} MB.')
        return f

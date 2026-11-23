"""
Views = the Python functions that run when someone opens a page.
Each view receives the request, talks to the database if needed,
and returns an HTML page.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import (
    Internship, Student, Application, ApplicationStatus,
    ApplicationStatusHistory, Resume, Company,
)
from .forms import ApplicationForm


def home(request):
    """Home page with a few summary numbers."""
    context = {
        'total_students': Student.objects.count(),
        'total_companies': Company.objects.count(),
        'open_internships': Internship.objects.filter(status='Open').count(),
        'total_applications': Application.objects.count(),
    }
    return render(request, 'portal/home.html', context)


def internship_list(request):
    """Show all open internships so students can browse them."""
    internships = Internship.objects.filter(status='Open').order_by('deadline')
    return render(request, 'portal/internships.html', {'internships': internships})


def internship_detail(request, internship_id):
    """One internship with full details."""
    internship = get_object_or_404(Internship, pk=internship_id)
    return render(request, 'portal/internship_detail.html', {'internship': internship})


def apply(request, internship_id):
    """Handle the apply form. Shows the form (GET) or saves the application (POST)."""
    internship = get_object_or_404(Internship, pk=internship_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.cleaned_data['student']

            # duplicate check: proposal says prevent duplicate applications
            if Application.objects.filter(student=student, internship=internship).exists():
                messages.error(request, 'You already applied for this internship.')
                return redirect('internship_detail', internship_id=internship.id)

            # if a resume file was uploaded, store it first
            resume = None
            uploaded_file = form.cleaned_data.get('resume_file')
            if uploaded_file:
                resume = Resume.objects.create(
                    student=student,
                    title=uploaded_file.name,
                    file=uploaded_file,
                )

            # create the application
            application = Application.objects.create(
                student=student,
                internship=internship,
                resume=resume,
                cover_letter=form.cleaned_data['cover_letter'],
            )

            # record the first status in the history table
            submitted_status = ApplicationStatus.objects.get(name='Submitted')
            ApplicationStatusHistory.objects.create(
                application=application,
                status=submitted_status,
                note='Application submitted by student',
            )

            return render(request, 'portal/success.html', {'application': application})
    else:
        form = ApplicationForm()

    return render(request, 'portal/apply.html', {'form': form, 'internship': internship})

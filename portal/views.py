"""
Views = the Python functions that run when someone opens a page.
Each view receives the request, talks to the database if needed,
and returns an HTML page.
"""
import datetime

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ApplicationForm
from .models import (
    Application, ApplicationStatus, ApplicationStatusHistory,
    Company, Internship, Resume, Student,
)


def _open_internships():
    """Internships that are marked Open AND whose deadline has not passed."""
    return Internship.objects.filter(
        status='Open', deadline__gte=datetime.date.today())


def home(request):
    """Home page with a few summary numbers."""
    context = {
        'total_students': Student.objects.count(),
        'total_companies': Company.objects.count(),
        'open_internships': _open_internships().count(),
        'total_applications': Application.objects.count(),
    }
    return render(request, 'portal/home.html', context)


def internship_list(request):
    """Show all open internships so students can browse them."""
    internships = (_open_internships()
                   .select_related('company')
                   .order_by('deadline'))
    return render(request, 'portal/internships.html', {'internships': internships})


def internship_detail(request, internship_id):
    """One internship with full details."""
    internship = get_object_or_404(
        Internship.objects.select_related('company')
                          .prefetch_related('internshipskill_set__skill'),
        pk=internship_id)
    is_open = (internship.status == 'Open'
               and internship.deadline >= datetime.date.today())
    return render(request, 'portal/internship_detail.html',
                  {'internship': internship, 'is_open': is_open})


def apply(request, internship_id):
    """Handle the apply form. Shows the form (GET) or saves the application (POST)."""
    internship = get_object_or_404(Internship.objects.select_related('company'),
                                   pk=internship_id)

    # closed / expired internships cannot receive applications
    if not _open_internships().filter(pk=internship.pk).exists():
        messages.error(request, 'This internship is closed and no longer accepts applications.')
        return redirect('internship_detail', internship_id=internship.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.cleaned_data['student']

            # duplicate check: proposal says prevent duplicate applications
            if Application.objects.filter(student=student, internship=internship).exists():
                messages.error(request, 'You already applied for this internship.')
                return redirect('internship_detail', internship_id=internship.id)

            try:
                # all-or-nothing: no orphan resume / application if something fails
                with transaction.atomic():
                    uploaded_file = form.cleaned_data.get('resume_file')
                    if uploaded_file:
                        resume = Resume.objects.create(
                            student=student, title=uploaded_file.name, file=uploaded_file)
                    else:
                        # fall back to the student's most recent saved resume (may be None)
                        resume = (Resume.objects.filter(student=student)
                                  .order_by('-uploaded_at').first())

                    application = Application.objects.create(
                        student=student,
                        internship=internship,
                        resume=resume,
                        cover_letter=form.cleaned_data['cover_letter'],
                    )

                    # record the first status in the history table
                    submitted_status, _ = ApplicationStatus.objects.get_or_create(
                        name='Submitted')
                    ApplicationStatusHistory.objects.create(
                        application=application,
                        status=submitted_status,
                        note='Application submitted by student',
                    )
            except IntegrityError:
                # two simultaneous submissions hit the unique (student, internship) rule
                messages.error(request, 'You already applied for this internship.')
                return redirect('internship_detail', internship_id=internship.id)

            # Post/Redirect/Get: refreshing the success page must not re-submit
            request.session['last_application_id'] = application.id
            return redirect('application_success')
    else:
        form = ApplicationForm()

    return render(request, 'portal/apply.html', {'form': form, 'internship': internship})


def application_success(request):
    """Confirmation page shown after a successful application."""
    app_id = request.session.get('last_application_id')
    application = (Application.objects
                   .select_related('student', 'internship')
                   .filter(pk=app_id).first()) if app_id else None
    if application is None:
        return redirect('internship_list')
    return render(request, 'portal/success.html', {'application': application})

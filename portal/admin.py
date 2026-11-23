"""
Registering our tables here makes them appear on the ready-made admin
website (/admin) so records can be added/edited/deleted like filling a form.
"""
from django.contrib import admin
from .models import (
    Department, Program, Student, Skill, StudentSkill,
    Company, CompanyContact, Internship, InternshipSkill,
    Resume, Application, ApplicationStatus, ApplicationStatusHistory,
    Interview, Offer, Placement,
)


class StatusHistoryInline(admin.TabularInline):
    """Lets an admin change an application's status by adding a history row
    right on the application page."""
    model = ApplicationStatusHistory
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'email', 'cgpa', 'program')
    list_filter = ('program',)
    search_fields = ('roll_no', 'name', 'email')


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'stipend', 'deadline', 'status')
    list_filter = ('status', 'company', 'location')
    search_fields = ('title', 'company__name')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'internship', 'applied_at')
    list_filter = ('internship__company',)
    search_fields = ('student__roll_no', 'student__name', 'internship__title')
    inlines = [StatusHistoryInline]


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interview_date', 'mode', 'result')
    list_filter = ('mode', 'result')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('application', 'stipend', 'offer_date', 'status')
    list_filter = ('status',)


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('offer', 'start_date', 'end_date', 'status')
    list_filter = ('status',)


for model in (Department, Program, Skill, StudentSkill, Company, CompanyContact,
              InternshipSkill, Resume, ApplicationStatus, ApplicationStatusHistory):
    admin.site.register(model)

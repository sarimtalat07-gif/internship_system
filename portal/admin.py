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

admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Student)
admin.site.register(Skill)
admin.site.register(StudentSkill)
admin.site.register(Company)
admin.site.register(CompanyContact)
admin.site.register(Internship)
admin.site.register(InternshipSkill)
admin.site.register(Resume)
admin.site.register(Application)
admin.site.register(ApplicationStatus)
admin.site.register(ApplicationStatusHistory)
admin.site.register(Interview)
admin.site.register(Offer)
admin.site.register(Placement)

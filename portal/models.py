"""
All 15 tables from our proposal, as Python classes.

Learning note: each class below = one table in Oracle. Each variable inside
a class = one column. 'ForeignKey' = a link to another table (like the
lines in an ERD diagram).
"""
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# ---------- ACADEMIC MANAGEMENT ----------
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    duration_years = models.IntegerField(default=4)

    class Meta:
        db_table = 'program'

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    cgpa = models.DecimalField(
        max_digits=3, decimal_places=2,  # e.g. 3.45
        validators=[MinValueValidator(0), MaxValueValidator(4)])
    program = models.ForeignKey(Program, on_delete=models.PROTECT)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.roll_no + ' - ' + self.name


# ---------- SKILL MANAGEMENT ----------
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'skill'

    def __str__(self):
        return self.name


class StudentSkill(models.Model):
    # junction table: which student has which skill
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=15, choices=PROFICIENCY_CHOICES, default='Beginner')

    class Meta:
        db_table = 'student_skill'
        unique_together = ('student', 'skill')  # a student can't have the same skill twice

    def __str__(self):
        return str(self.student) + ' -> ' + str(self.skill)


# ---------- COMPANY & INTERNSHIP MANAGEMENT ----------
class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    industry = models.CharField(max_length=100)
    website = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        db_table = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class CompanyContact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    class Meta:
        db_table = 'company_contact'

    def __str__(self):
        return self.person_name + ' (' + str(self.company) + ')'


class Internship(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=100)
    stipend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')

    class Meta:
        db_table = 'internship'

    def __str__(self):
        return self.title + ' @ ' + str(self.company)


class InternshipSkill(models.Model):
    # junction table: which skills an internship requires
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = 'internship_skill'
        unique_together = ('internship', 'skill')

    def __str__(self):
        return str(self.internship) + ' needs ' + str(self.skill)


# ---------- APPLICATION MANAGEMENT ----------
class Resume(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)          # e.g. "Resume - final version"
    file = models.FileField(upload_to='resumes/')      # saved under media/resumes/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resume'

    def __str__(self):
        return self.title


class ApplicationStatus(models.Model):
    # lookup table: the possible stages of an application
    name = models.CharField(max_length=30, unique=True)  # Submitted, Shortlisted, ...

    class Meta:
        db_table = 'application_status'

    def __str__(self):
        return self.name


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'application'
        unique_together = ('student', 'internship')  # prevents duplicate applications!

    def __str__(self):
        return str(self.student) + ' applied to ' + str(self.internship)


class ApplicationStatusHistory(models.Model):
    # every time an application's status changes, we add a row here
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    status = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'application_status_history'
        ordering = ['changed_at', 'id']

    def __str__(self):
        return str(self.application) + ' -> ' + str(self.status)


# ---------- RECRUITMENT & PLACEMENT ----------
class Interview(models.Model):
    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Onsite', 'Onsite'),
    ]
    RESULT_CHOICES = [
        ('Pending', 'Pending'),
        ('Passed', 'Passed'),
        ('Failed', 'Failed'),
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='Online')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, default='Pending')

    class Meta:
        db_table = 'interview'

    def __str__(self):
        return 'Interview for ' + str(self.application)


class Offer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    application = models.OneToOneField(Application, on_delete=models.CASCADE)  # one offer per application
    stipend = models.DecimalField(max_digits=10, decimal_places=2)
    offer_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = 'offer'

    def __str__(self):
        return 'Offer for ' + str(self.application)


class Placement(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE)  # one accepted offer = one placement
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ongoing')

    class Meta:
        db_table = 'placement'

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError('End date cannot be before start date.')

    def __str__(self):
        return 'Placement from ' + str(self.offer)

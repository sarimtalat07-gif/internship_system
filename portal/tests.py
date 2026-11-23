import datetime
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import (
    Application, ApplicationStatusHistory, Company, Department,
    Internship, Program, Resume, Student,
)

TODAY = datetime.date.today()


def make_internship(days=10, status='Open', title='Dev Intern'):
    company, _ = Company.objects.get_or_create(name='Acme', defaults={'industry': 'IT'})
    return Internship.objects.create(
        company=company, title=title, description='d', location='Lahore',
        stipend=Decimal('1000'), deadline=TODAY + datetime.timedelta(days=days),
        status=status)


class ApplyTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='CS')
        prog = Program.objects.create(name='BSCS', department=dept)
        self.student = Student.objects.create(
            name='A', roll_no='R1', email='a@x.com', cgpa=Decimal('3.5'), program=prog)
        self.internship = make_internship()
        self.url = reverse('apply', args=[self.internship.id])

    def post(self, **extra):
        data = {'student': self.student.id, 'cover_letter': 'hi'}
        data.update(extra)
        return self.client.post(self.url, data)

    def test_successful_application_creates_history_without_seed_data(self):
        resp = self.post()
        self.assertRedirects(resp, reverse('application_success'))
        app = Application.objects.get()
        self.assertEqual(ApplicationStatusHistory.objects.get(application=app).status.name,
                         'Submitted')

    def test_duplicate_application_rejected(self):
        self.post()
        resp = self.post()
        self.assertRedirects(resp, reverse('internship_detail', args=[self.internship.id]))
        self.assertEqual(Application.objects.count(), 1)

    def test_closed_internship_rejects_application(self):
        self.internship.status = 'Closed'
        self.internship.save()
        self.post()
        self.assertEqual(Application.objects.count(), 0)

    def test_expired_internship_rejects_application(self):
        self.internship.deadline = TODAY - datetime.timedelta(days=1)
        self.internship.save()
        self.post()
        self.assertEqual(Application.objects.count(), 0)

    def test_non_pdf_resume_rejected(self):
        f = SimpleUploadedFile('evil.html', b'<script></script>')
        resp = self.post(resume_file=f)
        self.assertEqual(resp.status_code, 200)  # form re-shown with errors
        self.assertEqual(Application.objects.count(), 0)
        self.assertEqual(Resume.objects.count(), 0)

    def test_latest_saved_resume_is_reused(self):
        r = Resume.objects.create(student=self.student, title='old', file='resumes/old.pdf')
        self.post()
        self.assertEqual(Application.objects.get().resume, r)

    def test_success_page_without_session_redirects(self):
        resp = self.client.get(reverse('application_success'))
        self.assertRedirects(resp, reverse('internship_list'))


class ListTests(TestCase):
    def test_expired_and_closed_hidden_from_list(self):
        make_internship(title='Visible')
        make_internship(days=-1, title='Expired')
        make_internship(status='Closed', title='Closed one')
        resp = self.client.get(reverse('internship_list'))
        titles = [i.title for i in resp.context['internships']]
        self.assertEqual(titles, ['Visible'])

    def test_home_and_detail_render(self):
        i = make_internship()
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('internship_detail', args=[i.id])).status_code, 200)

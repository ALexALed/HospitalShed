from django.test import TestCase

from .models import Doctor


class TestDoctors(TestCase):

    def test_models_str(self):
        doctor = Doctor(first_name='John', last_name='Smith')
        self.assertEquals(str(doctor), 'John Smith')

    def test_create_doctor(self):
        self.assertEquals(Doctor.objects.count(), 0)
        Doctor.objects.create(first_name='John', last_name='Smith')
        self.assertEquals(Doctor.objects.count(), 1)

    def test_update_doctor(self):
        Doctor.objects.create(first_name='John', last_name='Smith')
        doctor = Doctor.objects.get(pk=1)
        doctor.first_name = 'JJ'
        doctor.save()
        doctor = Doctor.objects.get(pk=1)
        self.assertEquals(str(doctor), 'JJ Smith')

    def test_delete(self):
        self.assertEquals(Doctor.objects.count(), 0)
        Doctor.objects.create(first_name='John', last_name='Smith')
        self.assertEquals(Doctor.objects.count(), 1)
        doctor = Doctor.objects.get(pk=1)
        doctor.delete()
        self.assertEquals(Doctor.objects.count(), 0)

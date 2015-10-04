from django.test import TestCase

from .models import Doctors


class TestDoctors(TestCase):

    def test_models_str(self):
        doctor = Doctors(first_name='John', last_name='Smith')
        self.assertEquals(str(doctor), 'John Smith')

    def test_create_doctor(self):
        self.assertEquals(Doctors.objects.count(), 0)
        Doctors.objects.create(first_name='John', last_name='Smith')
        self.assertEquals(Doctors.objects.count(), 1)

    def test_update_doctor(self):
        Doctors.objects.create(first_name='John', last_name='Smith')
        doctor = Doctors.objects.get(pk=1)
        doctor.first_name = 'JJ'
        doctor.save()
        doctor = Doctors.objects.get(pk=1)
        self.assertEquals(str(doctor), 'JJ Smith')

    def test_delete(self):
        self.assertEquals(Doctors.objects.count(), 0)
        Doctors.objects.create(first_name='John', last_name='Smith')
        self.assertEquals(Doctors.objects.count(), 1)
        doctor = Doctors.objects.get(pk=1)
        doctor.delete()
        self.assertEquals(Doctors.objects.count(), 0)

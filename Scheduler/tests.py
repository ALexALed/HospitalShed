import datetime
from django.test import TestCase
from django.test.client import Client
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from .models import Doctor, Schedule
from .forms import ReceptionForm


class TestSchedulerBackend(TestCase):

    def create_doctor_and_schedule(self, reception_date=datetime.date(2015, 10, 5),
                                   reception_time=datetime.time(10), save_schedule=True):
        doctor = Doctor.objects.create(first_name='John', last_name='Smith')
        if save_schedule:
            schedule = Schedule.objects.create(doctor=doctor,
                                               patient='Jack Daniel',
                                               reception_date=reception_date,
                                               reception_time=reception_time)
        else:
            schedule = Schedule(doctor=doctor,
                                patient='Jack Daniel',
                                reception_date=reception_date,
                                reception_time=reception_time)
        return schedule

    def test_models_str(self):
        schedule = self.create_doctor_and_schedule()
        self.assertEquals(str(schedule), 'John Smith-Jack Daniel-2015-10-05-10:00:00')

    def test_schedule_create(self):
        self.assertEquals(Schedule.objects.count(), 0)
        self.create_doctor_and_schedule()
        self.assertEquals(Schedule.objects.count(), 1)

    def test_schedule_update(self):
        self.assertEquals(Schedule.objects.count(), 0)
        self.create_doctor_and_schedule()
        self.assertEquals(Schedule.objects.count(), 1)
        schedule = Schedule.objects.get(pk=1)
        schedule.patient = 'JJ Daniel'
        schedule.save()

        schedule = Schedule.objects.get(pk=1)
        self.assertEquals(schedule.patient, 'JJ Daniel')

    def test_schedule_delete(self):
        self.assertEquals(Schedule.objects.count(), 0)
        self.create_doctor_and_schedule()
        self.assertEquals(Schedule.objects.count(), 1)
        schedule = Schedule.objects.get(pk=1)
        schedule.delete()
        self.assertEquals(Schedule.objects.count(), 0)

    def test_reception_impossibly_holiday(self):
        schedule = self.create_doctor_and_schedule(reception_date=datetime.date(2015, 10, 10),
                                                   reception_time=datetime.time(10))
        reception_result = Schedule.objects.reception_is_possibly(schedule.doctor,
                                                                  schedule.reception_date,
                                                                  schedule.reception_time)
        self.assertEquals(reception_result, False)

    def test_reception_impossibly_another_reception(self):
        self.create_doctor_and_schedule()
        schedule1 = self.create_doctor_and_schedule()
        reception_result = Schedule.objects.reception_is_possibly(schedule1.doctor,
                                                                  schedule1.reception_date,
                                                                  schedule1.reception_time)
        self.assertEquals(reception_result, False)

    def test_reception_possibly(self):
        schedule = self.create_doctor_and_schedule(reception_time=datetime.time(11),
                                                   save_schedule=False)
        reception_result = Schedule.objects.reception_is_possibly(schedule.doctor,
                                                                  schedule.reception_date,
                                                                  schedule.reception_time)
        self.assertEquals(reception_result, True)


class TestSchedulerFrontend(TestCase):

    def create_doctor(self):
        doctor = Doctor.objects.create(first_name='John',
                                       last_name='Smith')
        return doctor

    def test_add_reception_view(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добавить прием")
        self.assertEquals(
            response.context['form'].fields['doctor'].queryset.count(), 0)
        self.create_doctor()
        response = client.get('/')
        self.assertEquals(
            response.context['form'].fields['doctor'].queryset.count(), 1)

    def test_add_reception_new(self):
        self.create_doctor()
        client = Client()
        response = client.post('/', {'doctor': '1',
                                     'patient': 'John',
                                     'reception_date': '2015-10-05',
                                     'reception_time': '12:00',
                                     })

        self.assertEqual(response.status_code, 200)
        form = ReceptionForm(response.context[0].request.POST)
        self.assertEqual(form.is_valid(), True)

    def test_add_reception_impossibly(self):
        self.create_doctor()
        client = Client()
        response = client.post('/', {'doctor': '1',
                                     'patient': 'John',
                                     'reception_date': '2015-10-05',
                                     'reception_time': '23:00',
                                     })

        self.assertEqual(response.status_code, 200)
        form = ReceptionForm(response.context[0].request.POST)
        self.assertEqual(form.is_valid(), True)

    def test_add_reception_invalid(self):
        client = Client()
        response = client.post('/', {'doctor': '99999999',
                                     'patient': 'John',
                                     'reception_date': '2015-10-05',
                                     'reception_time': '12:00',
                                     })

        self.assertEqual(response.status_code, 200)
        form = ReceptionForm(response.context[0].request.POST)
        self.assertEqual(form.is_valid(), False)


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def create_doctor(self):
        doctor = Doctor.objects.create(first_name='John',
                                       last_name='Smith')
        return doctor

    def test_add_reception(self):
        self.assertEquals(Schedule.objects.count(), 0)
        self.create_doctor()
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        select = Select(self.selenium.find_element_by_id('id_doctor'))
        select.select_by_visible_text('John Smith')
        self.selenium.find_element_by_id('id_patient').send_keys('Patient')
        self.selenium.find_element_by_id('id_reception_date').clear()
        self.selenium.find_element_by_id(
            'id_reception_date').send_keys('2015-10-05')
        select = Select(self.selenium.find_element_by_id('id_reception_time'))
        select.select_by_visible_text('11:00')
        self.selenium.find_element_by_id('receptionSubmit').click()
        self.assertEquals(Schedule.objects.count(), 1)

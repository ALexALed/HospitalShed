from django.db import models
from django.conf import settings

from Doctors.models import Doctor


class ScheduleManager(models.Manager):
    """
    Schedule model manager
    """

    def reception_is_possibly(self, doctor, reception_date, reception_time):
        """
        Tested the possibility of receiving
        """
        result = False
        hospital_schedule = settings.HOSPITAL_WORK_SCHEDULE
        work_hours = hospital_schedule[reception_date.weekday()]

        # hour - reception duration
        if work_hours['start'] <= reception_time.hour <= work_hours['end']-1:
            exist_reception = self.filter(doctor=doctor,
                                          reception_time=reception_time).count()
            if not exist_reception:
                result = True
        return result


class Schedule(models.Model):
    """
    Model for storing schedules doctors reception
    """
    doctor = models.ForeignKey(Doctor, verbose_name='Доктор')
    patient = models.CharField('Пациент', max_length=255)
    reception_date = models.DateField('Дата приема')
    reception_time = models.TimeField('Время приема')

    objects = ScheduleManager()

    def __str__(self):
        return '{0}-{1}-{2}-{3}'.format(self.doctor,
                                        self.patient,
                                        self.reception_date,
                                        self.reception_time)

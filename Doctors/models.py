from django.db import models


class Doctor(models.Model):
    """
    Model for storing doctors info
    """
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

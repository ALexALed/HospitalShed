from django.db import models


class Doctors(models.Model):
    """
    model for storing doctors info
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

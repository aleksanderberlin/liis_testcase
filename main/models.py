from django.db import models
from django.utils import timezone

# Create your models here.


class Workplace(models.Model):
    room = models.CharField(max_length=50, verbose_name='Кабинет')
    created_at = models.DateTimeField(blank=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(blank=True, verbose_name='Дата обновления')
    removed_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        current_timestamp = timezone.now()
        if not self.id:
            self.created_at = current_timestamp
        self.updated_at = current_timestamp
        return super(Workplace, self).save(*args, **kwargs)


class Booking(models.Model):
    workplace = models.ForeignKey(Workplace, on_delete=models.RESTRICT)
    booking_begin = models.DateTimeField(verbose_name='Начало брони')
    booking_end = models.DateTimeField(verbose_name='Конец брони')
    created_at = models.DateTimeField(blank=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(blank=True, verbose_name='Дата обновления')
    removed_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        current_timestamp = timezone.now()
        if not self.id:
            self.created_at = current_timestamp
        self.updated_at = current_timestamp
        return super(Booking, self).save(*args, **kwargs)

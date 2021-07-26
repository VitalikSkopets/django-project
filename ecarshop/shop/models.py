from django.db import models
from django.urls import reverse


class Type(models.Model):
    class Meta:
        db_table = 'types'
        verbose_name = 'Type'
        verbose_name_plural = 'Types'
        ordering = ['id']

    title = models.CharField(max_length=100, db_index=True, verbose_name='vehicle type')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='slug')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:type_detail', kwargs={'type_slug': self.slug})


class Vehicle(models.Model):
    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        ordering = ['make', 'model', 'time_create']
        index_together = (('id', 'slug'),)

    type = models.ForeignKey(Type, related_name='vehicles', on_delete=models.PROTECT)
    make = models.CharField(max_length=100, verbose_name='make')
    model = models.CharField(max_length=100, db_index=True, verbose_name='model')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    description = models.TextField(blank=True, default='descriptions exist', verbose_name='short description')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='price USD')
    image = models.ImageField(upload_to='cars', blank=True, verbose_name='upload image')
    power = models.CharField(max_length=20, verbose_name='engine power')
    battery = models.CharField(max_length=20, verbose_name='battery energy')
    range = models.CharField(max_length=20, verbose_name='pure electric range')
    charging_time = models.CharField(max_length=20, verbose_name='charging time')
    type_of_battery = models.CharField(max_length=100, default='lithium-ion', verbose_name='type of battery')
    from_0_to_100 = models.CharField(max_length=20, verbose_name='0 to 100 km/h')
    max_speed = models.CharField(max_length=20, verbose_name='max speed')
    torque = models.CharField(max_length=20, verbose_name='torque')
    type_of_drive = models.CharField(max_length=20, blank=True, verbose_name='type of drive')
    in_storage = models.PositiveIntegerField(default=1, verbose_name='in storage')
    available = models.BooleanField(default=True, verbose_name='vehicle available')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make} {self.model}"

    def get_absolute_url(self):
        return reverse('shop:vehicle_detail', kwargs={'vehicle_slug': self.slug})

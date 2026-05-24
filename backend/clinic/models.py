from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Patient(models.Model):
    class Sex(models.TextChoices):
        UNKNOWN = 'unknown', 'Не вказано'
        MALE = 'male', 'Самець'
        FEMALE = 'female', 'Самка'

    name = models.CharField('Кличка', max_length=120)
    species = models.CharField('Вид тварини', max_length=100)
    breed = models.CharField('Порода', max_length=120, blank=True)
    sex = models.CharField('Стать', max_length=20, choices=Sex.choices, default=Sex.UNKNOWN)
    birth_date = models.DateField('Дата народження', null=True, blank=True)
    age_text = models.CharField('Вік', max_length=80, blank=True)
    features = models.TextField('Особливості', blank=True)
    comment = models.TextField('Коментар', blank=True)
    owner_full_name = models.CharField('ПІБ власника', max_length=160)
    owner_phone = models.CharField('Телефон власника', max_length=40)
    owner_comment = models.TextField('Коментар власника', blank=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Пацієнт'
        verbose_name_plural = 'Пацієнти'

    def __str__(self):
        return f'{self.name} ({self.species})'

    def get_absolute_url(self):
        return reverse('patient_detail', kwargs={'pk': self.pk})


class Visit(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visits',
        verbose_name='Пацієнт',
    )
    date = models.DateField('Дата прийому', default=timezone.localdate)
    short_description = models.CharField('Короткий опис', max_length=255)
    treatment = models.TextField('Лікування / призначення', blank=True)

    class Meta:
        ordering = ['-date', '-id']
        verbose_name = 'Прийом'
        verbose_name_plural = 'Прийоми'

    def __str__(self):
        return f'{self.patient.name} - {self.date}'


class Vaccination(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='vaccinations',
        verbose_name='Пацієнт',
    )
    vaccine_name = models.CharField('Назва вакцини', max_length=160)
    vaccination_date = models.DateField('Дата вакцинації')
    next_vaccination_date = models.DateField('Дата наступної вакцинації')

    class Meta:
        ordering = ['next_vaccination_date']
        verbose_name = 'Вакцинація'
        verbose_name_plural = 'Вакцинації'

    def __str__(self):
        return f'{self.patient.name} - {self.vaccine_name}'

    @property
    def status(self):
        today = timezone.localdate()
        if self.next_vaccination_date < today:
            return 'overdue'
        if self.next_vaccination_date <= today + timedelta(days=30):
            return 'soon'
        return 'active'

    @property
    def status_label(self):
        return {
            'active': 'Актуальна',
            'soon': 'Скоро',
            'overdue': 'Прострочена',
        }[self.status]


class InventoryItem(models.Model):
    name = models.CharField('Назва товару', max_length=160, unique=True)
    stock = models.PositiveIntegerField('Залишок', default=0)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар складу'
        verbose_name_plural = 'Склад'

    def __str__(self):
        return f'{self.name}: {self.stock}'

    def buy(self, quantity):
        self.stock += quantity
        self.save(update_fields=['stock', 'updated_at'])

    def sell(self, quantity):
        if quantity > self.stock:
            raise ValidationError('Не можна продати більше, ніж є в залишку.')
        self.stock -= quantity
        self.save(update_fields=['stock', 'updated_at'])

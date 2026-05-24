from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import InventoryItem, Patient, Vaccination


class ClinicMvpTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
        )
        self.patient = Patient.objects.create(
            name='Рекс',
            species='Собака',
            owner_full_name='Олена Коваленко',
            owner_phone='+380501112233',
        )

    def test_vaccination_statuses(self):
        today = timezone.localdate()
        overdue = Vaccination.objects.create(
            patient=self.patient,
            vaccine_name='Rabies',
            vaccination_date=today - timedelta(days=370),
            next_vaccination_date=today - timedelta(days=1),
        )
        soon = Vaccination.objects.create(
            patient=self.patient,
            vaccine_name='DHPP',
            vaccination_date=today,
            next_vaccination_date=today + timedelta(days=10),
        )
        active = Vaccination.objects.create(
            patient=self.patient,
            vaccine_name='Lepto',
            vaccination_date=today,
            next_vaccination_date=today + timedelta(days=90),
        )

        self.assertEqual(overdue.status, 'overdue')
        self.assertEqual(soon.status, 'soon')
        self.assertEqual(active.status, 'active')

    def test_inventory_cannot_sell_more_than_stock(self):
        item = InventoryItem.objects.create(name='Бинт', stock=2)

        with self.assertRaises(ValidationError):
            item.sell(3)

        item.refresh_from_db()
        self.assertEqual(item.stock, 2)

    def test_main_pages_open(self):
        self.client.force_login(self.user)
        paths = [
            reverse('home'),
            reverse('patient_list'),
            reverse('patient_detail', kwargs={'pk': self.patient.pk}),
            reverse('vaccination_list'),
            reverse('inventory_list'),
        ]

        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_home_requires_login(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

# Create your tests here.

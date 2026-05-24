from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import (
    InventoryAdjustmentForm,
    InventoryItemForm,
    PatientForm,
    VaccinationForm,
    VisitForm,
)
from .models import InventoryItem, Patient, Vaccination, Visit


@login_required
def home(request):
    today = timezone.localdate()
    vaccinations = Vaccination.objects.select_related('patient')
    context = {
        'patients_count': Patient.objects.count(),
        'inventory_count': InventoryItem.objects.count(),
        'overdue_vaccinations': [v for v in vaccinations if v.status == 'overdue'],
        'soon_vaccinations': [v for v in vaccinations if v.status == 'soon'],
        'today': today,
    }
    return render(request, 'clinic/home.html', context)


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'clinic/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(owner_phone__icontains=query)
                | Q(owner_full_name__icontains=query)
            )
        return queryset.distinct()


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'clinic/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visits'] = self.object.visits.all()
        context['vaccinations'] = self.object.vaccinations.all()
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'clinic/patient_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Пацієнта створено.')
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'clinic/patient_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Картку пацієнта оновлено.')
        return super().form_valid(form)


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'clinic/confirm_delete.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        messages.success(self.request, 'Пацієнта видалено.')
        return super().form_valid(form)


@login_required
def visit_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = VisitForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        visit = form.save(commit=False)
        visit.patient = patient
        visit.save()
        messages.success(request, 'Прийом додано.')
        return redirect(patient)
    return render(request, 'clinic/visit_form.html', {'form': form, 'patient': patient})


class VisitUpdateView(LoginRequiredMixin, UpdateView):
    model = Visit
    form_class = VisitForm
    template_name = 'clinic/visit_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context

    def get_success_url(self):
        messages.success(self.request, 'Прийом оновлено.')
        return self.object.patient.get_absolute_url()


class VisitDeleteView(LoginRequiredMixin, DeleteView):
    model = Visit
    template_name = 'clinic/confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Прийом видалено.')
        return self.object.patient.get_absolute_url()


class VaccinationListView(LoginRequiredMixin, ListView):
    model = Vaccination
    template_name = 'clinic/vaccination_list.html'
    context_object_name = 'vaccinations'

    def get_queryset(self):
        return Vaccination.objects.select_related('patient')


@login_required
def vaccination_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = VaccinationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        vaccination = form.save(commit=False)
        vaccination.patient = patient
        vaccination.save()
        messages.success(request, 'Вакцинацію додано.')
        return redirect(patient)
    return render(request, 'clinic/vaccination_form.html', {'form': form, 'patient': patient})


class VaccinationUpdateView(LoginRequiredMixin, UpdateView):
    model = Vaccination
    form_class = VaccinationForm
    template_name = 'clinic/vaccination_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context

    def get_success_url(self):
        messages.success(self.request, 'Вакцинацію оновлено.')
        return self.object.patient.get_absolute_url()


class VaccinationDeleteView(LoginRequiredMixin, DeleteView):
    model = Vaccination
    template_name = 'clinic/confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Вакцинацію видалено.')
        return self.object.patient.get_absolute_url()


class InventoryListView(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'clinic/inventory_list.html'
    context_object_name = 'items'


class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'clinic/inventory_form.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        messages.success(self.request, 'Товар створено.')
        return super().form_valid(form)


class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'clinic/inventory_form.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        messages.success(self.request, 'Товар оновлено.')
        return super().form_valid(form)


class InventoryDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'clinic/confirm_delete.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        messages.success(self.request, 'Товар видалено.')
        return super().form_valid(form)


@login_required
def inventory_adjust(request, pk, action):
    item = get_object_or_404(InventoryItem, pk=pk)
    form = InventoryAdjustmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        quantity = form.cleaned_data['quantity']
        try:
            if action == 'buy':
                item.buy(quantity)
                messages.success(request, 'Залишок збільшено.')
            elif action == 'sell':
                item.sell(quantity)
                messages.success(request, 'Залишок зменшено.')
            else:
                messages.error(request, 'Невідома дія.')
        except ValidationError as exc:
            messages.error(request, exc.message)
    return redirect('inventory_list')

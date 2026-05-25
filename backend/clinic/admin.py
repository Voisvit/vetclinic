from django.contrib import admin

from .models import InventoryItem, Patient, Vaccination, Visit


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0


class VaccinationInline(admin.TabularInline):
    model = Vaccination
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'species', 'display_owner_full_name', 'owner_phone')
    search_fields = ('name', 'species', 'breed', 'owner_full_name', 'owner_phone')
    list_filter = ('species', 'sex')
    inlines = [VisitInline, VaccinationInline]

    @admin.display(description='Кличка', ordering='name')
    def display_name(self, obj):
        return obj.display_name

    @admin.display(description='ПІБ власника', ordering='owner_full_name')
    def display_owner_full_name(self, obj):
        return obj.display_owner_full_name


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'short_description')
    search_fields = ('patient__name', 'short_description', 'treatment')
    list_filter = ('date',)


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'vaccine_name', 'vaccination_date', 'next_vaccination_date', 'status_label')
    search_fields = ('patient__name', 'vaccine_name')
    list_filter = ('next_vaccination_date',)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'updated_at')
    search_fields = ('name',)

# Register your models here.

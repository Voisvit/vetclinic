from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/new/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('patients/<int:patient_pk>/visits/new/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/edit/', views.VisitUpdateView.as_view(), name='visit_update'),
    path('visits/<int:pk>/delete/', views.VisitDeleteView.as_view(), name='visit_delete'),
    path('vaccinations/', views.VaccinationListView.as_view(), name='vaccination_list'),
    path('patients/<int:patient_pk>/vaccinations/new/', views.vaccination_create, name='vaccination_create'),
    path('vaccinations/<int:pk>/edit/', views.VaccinationUpdateView.as_view(), name='vaccination_update'),
    path('vaccinations/<int:pk>/delete/', views.VaccinationDeleteView.as_view(), name='vaccination_delete'),
    path('inventory/', views.InventoryListView.as_view(), name='inventory_list'),
    path('inventory/new/', views.InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/edit/', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.InventoryDeleteView.as_view(), name='inventory_delete'),
    path('inventory/<int:pk>/<str:action>/', views.inventory_adjust, name='inventory_adjust'),
]

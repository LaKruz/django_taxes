from django.urls import path, include

urlpatterns = [
    path('', include('income_tax.urls')),
]

from django.urls import path
from income_tax.views import IncomeView

urlpatterns = [
    path('', IncomeView.as_view())
]

from django.views import View
from django.shortcuts import render
from django.http import FileResponse, HttpRequest, HttpResponse
from .forms import UploadFileForm
from .business_logic.writer import get_tax


class IncomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = UploadFileForm()
        return render(request, 'base.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result = get_tax(request.FILES['file'])
            return FileResponse(result, as_attachment=True, filename='result.xlsx')
        return render(request, 'base.html', {'form': form})

from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }))

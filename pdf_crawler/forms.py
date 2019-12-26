from django import forms


class UploadFileForm(forms.Form):
    pdf = forms.FileField()

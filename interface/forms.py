from django import forms
from interface.models import *

class FormUpdate(forms.ModelForm):
    class Meta:
        model = tbl_berita
        fields = ('url_berita','judul', 'isi_berita', 'time_publiserby', 'sumber_berita','status_berita')



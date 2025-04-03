from django import forms
from dal import autocomplete
from .models import Student
from app_common.models import Department, Faculty

class StudentForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        widget=autocomplete.ModelSelect2(
            url='app_student:department-autocomplete',  # URL autocomplete untuk department
            forward=['faculty']  # Kirim faculty_id untuk memfilter department
        )
    )
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'faculty': autocomplete.ModelSelect2(url='app_student:faculty-autocomplete'),
            'department':autocomplete.ModelSelect2(url='app_student:department-autocomplete', forward=['faculty'])
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.faculty:
            # Jika Faculty sudah dipilih, tampilkan Department sesuai Faculty
            self.fields['department'].queryset = Department.objects.filter(faculty=self.instance.faculty)
        else:
            # Jika Faculty belum dipilih, kosongkan queryset department
            self.fields['department'].queryset = Department.objects.none()
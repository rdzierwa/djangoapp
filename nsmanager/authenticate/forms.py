from django import forms
from productapp.models import User, Company, Warehouse

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField(required=True)
    warehouse_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['login', 'password', 'company_name', 'warehouse_name', 'privilege']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                # Tworzenie firmy
                company = Company(name=self.cleaned_data['company_name'])
                company.save()
                
                # Tworzenie magazynu
                warehouse = Warehouse(
                    name=self.cleaned_data['warehouse_name'],
                    url='some_url',  # dostarcz wartość dla url
                    credentials={}  # dostarcz wartość dla credentials, pusty słownik JSON
                )
                warehouse.save()
                
                # Przypisanie użytkownika do firmy i magazynu
                user.company = company
                user.save()
                warehouse.users.add(user)
            return user


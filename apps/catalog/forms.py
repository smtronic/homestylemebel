from django import forms
from apps.catalog.models import Product
from apps.catalog.services.product_services import ProductServices


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        try:
            ProductServices.prepare_for_save(self.instance)
        except Exception as e:
            self.add_error(None, str(e))
        return cleaned_data

from django import forms
from .models import Quote, Source

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ["name", "type"]

class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(
        required=False,
        help_text="Если хотите создать новый источник, заполните это поле (иначе выберите существующий ниже)."
    )

    class Meta:
        model = Quote
        fields = ["source", "text", "weight", "author", "language", "year"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
            "year": forms.NumberInput(attrs={"min": 0, "max": 2100}),
        }

    def clean(self):
        cleaned = super().clean()
        source = cleaned.get("source")
        source_name = cleaned.get("source_name")
        if not source and not source_name:
            raise forms.ValidationError("Укажите существующий источник или введите новый.")
        return cleaned

    def save(self, commit=True):
        source = self.cleaned_data.get("source")
        source_name = self.cleaned_data.get("source_name")
        if not source and source_name:
            source = Source.objects.create(name=source_name.strip())
        self.instance.source = source
        return super().save(commit=commit)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["source"].required = False

    def clean(self):
        cleaned = super().clean()
        source = cleaned.get("source")
        source_name = cleaned.get("source_name")

        if not source and not source_name:
            raise forms.ValidationError("Укажите существующий источник или введите новый.")
        # Нормализуем source_name
        if source_name is not None:
            source_name = source_name.strip()
            cleaned["source_name"] = source_name
            if not source and source_name == "":
                raise forms.ValidationError("Название нового источника не может быть пустым.")
        return cleaned

    def save(self, commit=True):
        source = self.cleaned_data.get("source")
        source_name = self.cleaned_data.get("source_name")

        # Если выбран существующий источник — используем его и игнорируем source_name
        if not source:
            # Если введено имя — переиспользуем существующий или создаём новый
            if source_name:
                source, _ = Source.objects.get_or_create(
                    name=source_name,
                    defaults={"type": "other"}
                )
            else:
                # Теоретически не должно случиться из-за clean(), но на всякий случай
                raise forms.ValidationError("Не удалось определить источник.")
        self.instance.source = source
        return super().save(commit=commit)
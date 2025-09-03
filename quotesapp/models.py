from django.db import models
from django.core.exceptions import ValidationError

class Source(models.Model):
    SOURCE_TYPES = [
        ("movie", "Фильм"),
        ("book", "Книга"),
        ("other", "Другое"),
    ]
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=SOURCE_TYPES, default="other")

    def __str__(self):
        return self.name

class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="quotes")
    text = models.TextField(unique=True)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=8, default="ru", help_text="Код языка, напр. ru, en")
    year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-likes", "-created_at"]
        indexes = [
            models.Index(fields=["language"]),
            models.Index(fields=["source"]),
        ]

    def clean(self):
        if self.source_id:
            qs = Quote.objects.filter(source=self.source).exclude(pk=self.pk)
            if qs.count() >= 3:
                raise ValidationError("У данного источника уже 3 цитаты. Сначала удалите или измените существующие.")
        if self.weight <= 0:
            raise ValidationError("Вес должен быть положительным.")
        if self.year and (self.year < 0 or self.year > 2100):
            raise ValidationError("Некорректный год.")

    def __str__(self):
        return f"{self.text[:40]}..."

    @property
    def rating(self):
        return self.likes - self.dislikes
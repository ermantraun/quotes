from django.contrib import admin
from .models import Quote, Source

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    search_fields = ("name",)
    list_filter = ("type",)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("short_text", "source", "author", "language", "year", "weight", "likes", "dislikes", "views", "created_at")
    search_fields = ("text", "source__name", "author")
    list_filter = ("source__type", "language")
    ordering = ("-likes",)

    def short_text(self, obj):
        return obj.text[:60] + ("..." if len(obj.text) > 60 else "")
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("quotesapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="quote",
            name="author",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="quote",
            name="language",
            field=models.CharField(default="ru", help_text="Код языка, напр. ru, en", max_length=8),
        ),

        migrations.AddIndex(
            model_name="quote",
            index=models.Index(fields=["language"], name="quotesapp_q_language_idx"),
        ),
        migrations.AddIndex(
            model_name="quote",
            index=models.Index(fields=["source"], name="quotesapp_q_source_id_idx"),
        ),
    ]
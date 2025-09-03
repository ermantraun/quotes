from django.test import TestCase
from django.core.exceptions import ValidationError
from quotesapp.models import Source, Quote

class QuoteModelTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(name="Test Movie", type="movie")

    def test_limit_three_quotes_per_source(self):
        for i in range(3):
            Quote.objects.create(source=self.source, text=f"Q{i}", weight=1)
        q4 = Quote(source=self.source, text="Q3", weight=1)
        with self.assertRaises(ValidationError):
            q4.clean()

    def test_unique_text(self):
        Quote.objects.create(source=self.source, text="Hello", weight=1)
        with self.assertRaises(Exception):
            Quote.objects.create(source=self.source, text="Hello", weight=1)

    def test_year_validation(self):
        q = Quote(source=self.source, text="Year test", weight=1, year=2500)
        with self.assertRaises(ValidationError):
            q.clean()
from django.test import TestCase
from django.urls import reverse
from quotesapp.models import Source, Quote

class ViewTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(name="S1")
        Quote.objects.create(source=self.source, text="Quote 1", weight=5, author="Auth", language="ru", year=2020)

    def test_index(self):
        r = self.client.get(reverse("index"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Quote 1")

    def test_add_quote(self):
        r = self.client.post(reverse("add_quote"), {
            "source": "",
            "source_name": "S2",
            "text": "New Quote",
            "weight": 2,
            "author": "Author 2",
            "language": "en",
            "year": 1999
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Quote.objects.filter(text="New Quote", language="en").exists())

    def test_like(self):
        q = Quote.objects.first()
        r = self.client.post(reverse("like_quote", args=[q.id]), {"action": "like"})
        self.assertEqual(r.status_code, 200)
        q.refresh_from_db()
        self.assertEqual(q.likes, 1)

    def test_top_filters(self):
        r = self.client.get(reverse("top_quotes"), {"lang": "ru"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Quote 1")
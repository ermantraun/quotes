import random
from .models import Quote

def get_weighted_random_quote():
    quotes = list(Quote.objects.all().values("id", "weight"))
    if not quotes:
        return None
    total_weight = sum(q["weight"] for q in quotes)
    r = random.randint(1, total_weight)
    cumulative = 0
    selected_id = None
    for q in quotes:
        cumulative += q["weight"]
        if r <= cumulative:
            selected_id = q["id"]
            break
    if selected_id is None:
        selected_id = quotes[-1]["id"]
    return Quote.objects.get(pk=selected_id)
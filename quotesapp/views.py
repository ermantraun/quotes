from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Count, Sum
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import QuoteForm
from .models import Quote, Source
from .services import get_weighted_random_quote

def index(request):
    quote = get_weighted_random_quote()
    if quote:
        Quote.objects.filter(pk=quote.pk).update(views=F("views") + 1)
        quote.refresh_from_db(fields=["views"])
    return render(request, "quotesapp/index.html", {"quote": quote})

def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Цитата добавлена.")
                return redirect("index")
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = QuoteForm()
    return render(request, "quotesapp/add_quote.html", {"form": form})

def top_quotes(request):
    qs = Quote.objects.all()
    source_id = request.GET.get("source")
    source_type = request.GET.get("type")
    language = request.GET.get("lang")

    if source_id:
        qs = qs.filter(source_id=source_id)
    if source_type:
        qs = qs.filter(source__type=source_type)
    if language:
        qs = qs.filter(language=language)

    qs = qs.order_by("-likes", "dislikes", "-views")

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    sources = Source.objects.order_by("name")
    languages = Quote.objects.values_list("language", flat=True).distinct().order_by("language")

    context = {
        "page_obj": page_obj,
        "sources": sources,
        "languages": languages,
        "current_source": source_id or "",
        "current_type": source_type or "",
        "current_lang": language or "",
    }
    return render(request, "quotesapp/top_quotes.html", context)

def dashboard(request):
    total_quotes = Quote.objects.count()
    total_sources = Source.objects.count()
    total_views = Quote.objects.aggregate(s=Sum("views"))["s"] or 0
    top_source = (
        Source.objects.annotate(c=Count("quotes"))
        .order_by("-c")
        .first()
    )
    return render(
        request,
        "quotesapp/dashboard.html",
        {
            "total_quotes": total_quotes,
            "total_sources": total_sources,
            "total_views": total_views,
            "top_source": top_source,
        },
    )

@require_POST
def like_quote(request, pk):
    action = request.POST.get("action")
    quote = get_object_or_404(Quote, pk=pk)
    if action not in ("like", "dislike"):
        return HttpResponseBadRequest("Invalid action")
    if action == "like":
        Quote.objects.filter(pk=quote.pk).update(likes=F("likes") + 1)
    else:
        Quote.objects.filter(pk=quote.pk).update(dislikes=F("dislikes") + 1)
    quote.refresh_from_db(fields=["likes", "dislikes"])
    return JsonResponse({"likes": quote.likes, "dislikes": quote.dislikes, "rating": quote.rating})
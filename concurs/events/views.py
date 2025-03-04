from django.db.models import Q
from django.shortcuts import render
from django.views import View

from events.forms import SearchForm
from events.models import EventModel, HistoryModel


class AllHistoriesView(View):
    def get(self, request):
        histories = HistoryModel.objects.all()
        context = {
            "histories": histories,
        }

        return render(
            request,
            "events/all_histories.html",
            context=context,
        )


class AllEventsByHistoryView(View):
    def get(self, request, history_id):
        form_for_search = SearchForm()
        context = {
            "events": EventModel.objects.filter(
                history_id=history_id,
            ),
            "history": HistoryModel.objects.get(id=history_id),
            "form_for_search": form_for_search,
        }

        return render(
            request,
            "events/all_events.html",
            context=context,
        )

    def post(self, request, history_id):
        form_for_search = SearchForm(request.POST)
        if form_for_search.is_valid():
            print("1" * 100)
            search_content = form_for_search.cleaned_data.get(
                "request_content",
            )
            condition_for_search = Q()
            condition_for_search |= Q(date__icontains=search_content)
            condition_for_search |= Q(content__icontains=search_content)
            context = {
                "events": EventModel.objects.filter(
                    condition_for_search,
                    history_id=history_id,
                ),
                "history": HistoryModel.objects.get(id=history_id),
                "form_for_search": form_for_search,
            }
            return render(
                request,
                "events/all_events.html",
                context=context,
            )
        context = {
            "events": EventModel.objects.filter(
                history_id=history_id,
            ),
            "history": HistoryModel.objects.get(id=history_id),
            "form_for_search": form_for_search,
        }

        return render(
            request,
            "events/all_events.html",
            context=context,
        )


class AboutEventView(View):
    def get(self, request, history_id, event_id):
        context = {
            "event": EventModel.objects.get(id=event_id),
            "history": HistoryModel.objects.get(id=history_id),
        }

        return render(
            request,
            "events/about_event.html",
            context=context,
        )

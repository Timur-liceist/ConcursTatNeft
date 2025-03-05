import json

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from events.forms import SearchForm
from events.models import EventModel, HistoryModel
from events.utils import (
    get_csv_events_from_db_with_django,
    yandex_gpt,
)


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


@method_decorator(csrf_exempt, name="dispatch")
class ChatAIView(View):
    def post(self, request, history_id):
        try:
            data = json.loads(request.body)
            user_message = data.get(
                "message",
                "",
            )
            if not user_message.strip():
                return JsonResponse(
                    {
                        "error": "Сообщение не может быть пустым",
                    },
                    status=400,
                )

            csv_events = get_csv_events_from_db_with_django(
                history_id=history_id,
            )

            messages = []

            messages.append(
                {
                    "role": "system",
                    # "text": f"{settings.SYSTEM_ROLE_START_TEXT}\n{csv_events}",
                    "text": f"{settings.SYSTEM_ROLE_START_TEXT}",
                },
            )
            for event in csv_events.split("\n"):
                messages.append(  # noqa: PERF401
                    {
                        "role": "system",
                        "text": event,
                    },
                )
            messages.append(
                {
                    "role": "user",
                    "text": user_message,
                },
            )

            answer_gpt = yandex_gpt(
                messages=messages,
            )

            return JsonResponse(
                {
                    "response": answer_gpt,
                },
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "error": "Некорректный JSON",
                },
                status=400,
            )

from django.urls import path

from events import views

app_name = "events"

urlpatterns = [
    path(
        "history",
        views.AllHistoriesView.as_view(),
        name="all_histories",
    ),
    path(
        "history/<int:history_id>",
        views.AllEventsByHistoryView.as_view(),
        name="all_events",
    ),
    path(
        "history/<int:history_id>/event/<int:event_id>",
        views.AboutEventView.as_view(),
        name="about_event",
    ),
    path(
        "history/<int:history_id>/chat_ai",
        views.ChatAIView.as_view(),
        name="chat_ai",
    ),
]

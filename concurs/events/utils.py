import requests
from django.conf import settings

from events.models import EventModel


def yandex_gpt(messages):
    prompt = {
        "modelUri": f"gpt://{settings.ID_CATALOG_YANDEX_GPT}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "2000",
        },
        "messages": messages,
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {settings.IAM_TOKEN_YANDEX_GPT}",
    }

    response = requests.post(
        url,
        headers=headers,
        json=prompt,
        timeout=200,
    )
    result = response.json().get("result")

    return result["alternatives"][0]["message"]["text"]


def get_csv_events_from_db_with_django(history_id):
    events = EventModel.objects.filter(
        history_id=history_id,
    ).only(
        "date",
        "content",
    )

    content_csv = "Дата;Событие"

    for event in events:
        content_csv += f"\n{event.date};{event.content}"

    return content_csv

import requests

from events.models import EventModel


def gpt(messages):
    prompt = {
        "modelUri": "gpt://b1ghnehmnn3n3dvbqi90/yandexgpt",
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
        "Authorization": "Api-Key AQVNz9XUQGq4KhejXKZ-8PLoDVwLZrPGARRazGnK",
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
        content_csv += f"{event.date};{event.content}"

    return content_csv


def make_request_yandexgpt(messages, message):
    messages.append(
        {
            "role": "user",
            "content": message,
        },
    )

    return gpt(messages)

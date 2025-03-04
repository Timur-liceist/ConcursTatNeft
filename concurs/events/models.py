from django.db import models


class HistoryModel(models.Model):
    title = models.CharField(
        verbose_name="название истории",
        max_length=255,
    )

    class Meta:
        verbose_name = "история"
        verbose_name_plural = "истории"

    def __str__(self) -> str:
        return self.title


class EventModel(models.Model):
    history = models.ForeignKey(
        HistoryModel,
        verbose_name="история",
        on_delete=models.CASCADE,
    )

    date = models.CharField(
        verbose_name="дата",
        max_length=100,
    )
    content = models.TextField(
        verbose_name="событие",
    )

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"

    def __str__(self) -> str:
        return self.date

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Inmate(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    patronymic = models.TextField(blank=True)
    birth_date = models.DateField()
    metadata = models.JSONField(default=dict)

    def __str__(self) -> str:
        return (
            f"{self.last_name} {self.first_name} {self.patronymic} ({self.birth_date})"
        )


class Prison(models.Model):
    name = models.TextField(unique=True)
    address = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} ({self.address})"


TIME_PRECISION_CHOICES = list(
    enumerate(
        [
            "1 minute",
            "5 minutes",
            "10 minutes",
            "30 minutes",
            "1 hour",
            "2 hours",
            "3 hours",
        ]
    )
)


class Detention(models.Model):
    inmate = models.ForeignKey(Inmate, models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField(null=True)
    time_precision = models.IntegerField(choices=TIME_PRECISION_CHOICES, null=True)
    details = models.TextField(default="")
    location = models.TextField(default="")
    punishment = models.IntegerField()
    court = models.TextField(default="")
    judge = models.TextField(default="")
    articles = ArrayField(models.TextField(max_length=10))
    freed_date = models.DateTimeField(null=True)


class Imprisonment(models.Model):
    detention = models.ForeignKey(Detention, models.CASCADE)
    prison = models.ForeignKey(Prison, models.CASCADE)
    cells = ArrayField(models.IntegerField(), blank=True, default=list)
    date = models.DateTimeField(null=True)


class List(models.Model):
    date = models.DateField(null=True, blank=True)
    prison = models.ForeignKey(Prison, models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    origin = models.TextField()
    metadata = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"{self.origin} [{self.date or '<Unknown>'}]"


class ListItem(models.Model):
    list = models.ForeignKey(List, models.CASCADE, related_name="items")
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    patronymic = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    inmate = models.ForeignKey(Inmate, models.SET_NULL, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    # TODO should be discrete for simplicity
    match_confidence = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return (
            f"{self.last_name} {self.first_name} {self.patronymic} ({self.birth_date})"
        )

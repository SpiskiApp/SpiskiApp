# Generated by Django 3.1 on 2020-11-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cage", "0005_inmate_patronymic_blank"),
    ]

    operations = [
        migrations.AddField(
            model_name="listitem",
            name="comments",
            field=models.TextField(blank=True, null=True),
        ),
    ]
# Generated by Django 3.1 on 2020-10-29 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cage", "0003_blank_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
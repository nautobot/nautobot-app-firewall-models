# Generated by Django 3.2.13 on 2022-06-20 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nautobot_firewall_models", "0004_capircapolicy"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="capircapolicy",
            options={"ordering": ["device"], "verbose_name_plural": "Capirca Policies"},
        ),
    ]

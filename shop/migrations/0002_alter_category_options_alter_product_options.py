# Generated by Django 5.0 on 2024-01-30 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ("name",),
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ("name",),
                "verbose_name": "product",
                "verbose_name_plural": "products",
            },
        ),
    ]
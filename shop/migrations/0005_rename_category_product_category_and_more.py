# Generated by Django 5.0 on 2024-01-31 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_cart_cartitem"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product", old_name="Category", new_name="category",
        ),
        migrations.RenameField(
            model_name="product", old_name="Created", new_name="created",
        ),
    ]

from django.db import migrations

DEFAULT_CATEGORIES = [
    "餐廳",
    "咖啡廳",
    "酒吧",
    "景點",
    "博物館",
    "公園",
    "夜市",
    "購物",
    "電影院",
    "住宿",
    "甜點",
    "其他",
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("places", "Category")
    for name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0011_alter_category_name_alter_favoriteplace_created_at_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]

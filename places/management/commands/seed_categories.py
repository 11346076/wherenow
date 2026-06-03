from django.core.management.base import BaseCommand

from places.models import Category

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


class Command(BaseCommand):
    help = "建立預設地點分類（可在 Django Admin 再調整）"

    def handle(self, *args, **options):
        created = 0
        for name in DEFAULT_CATEGORIES:
            _, was_created = Category.objects.get_or_create(name=name)
            if was_created:
                created += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"分類就緒：新增 {created} 筆，共 {Category.objects.count()} 筆"
            )
        )

#!/usr/bin/env python
"""Quick verification for i18n, templates, and category seed."""
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wherenow.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.template.loader import get_template
from django.utils import translation
from places.models import Category

TEMPLATES = [
    "places/random_pick.html",
    "places/random_pick_history.html",
    "places/place_form.html",
    "memories/memory_create.html",
    "memories/memory_edit.html",
    "couples/couple_home.html",
    "couples/couple_status.html",
    "couples/send_invitation.html",
    "couples/received_invitations.html",
    "couples/edit_anniversary.html",
    "base.html",
]

errors = []

for name in TEMPLATES:
    try:
        get_template(name)
    except Exception as exc:
        errors.append(f"template {name}: {exc}")

category_count = Category.objects.count()
if category_count < 12:
    errors.append(f"categories: expected >= 12, got {category_count}")

translation.activate("en")
from django.utils.translation import gettext as _

samples = [
    _("首頁"),
    _("隨機抽選歷史"),
    _("新增回憶"),
    _("情侶首頁"),
]
for text in samples:
    if text and any("\u4e00" <= ch <= "\u9fff" for ch in text):
        errors.append(f"i18n still Chinese for sample: {text}")

translation.deactivate()

if errors:
    print("VERIFY FAILED:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print("VERIFY OK")
print(f"  templates: {len(TEMPLATES)}")
print(f"  categories: {category_count}")
print(f"  en sample Home: {samples[0]}")

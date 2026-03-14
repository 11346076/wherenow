# 第 2 週

## 目標
完成核心 Models 與 Django Admin 設定。

---

## 本週必做

- 建立 `Profile` model
- 建立 `CoupleInvitation` model
- 建立 `CoupleRelationship` model
- 建立 `Category` model
- 建立 `Tag` model
- 建立 `Place` model
- 建立 `PlaceTag` model
- 建立 `Memory` model
- 建立 `MemoryPhoto` model
- 在 Admin 後台完成註冊與確認

> 以下步驟大致相同：  
> 1. 撰寫 model  
> 2. 執行 migration  
> 3. 註冊 admin  
> 4. 執行伺服器檢查成果

---

# 一、建立 `Profile` model

建立檔案：`users/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.nickname
```

## 欄位說明

| 欄位 | 用途 |
|---|---|
| user | 連接 Django User |
| nickname | 使用者暱稱 |
| avatar | 頭像圖片 |
| bio | 自我介紹 |

執行：

```bash
python manage.py makemigrations
python manage.py migrate
```

建立檔案：`users/admin.py`

```python
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
```

建立管理員帳號：

```bash
python manage.py createsuperuser
```

啟動伺服器：

```bash
python manage.py runserver
```

登入後台：

```text
http://127.0.0.1:8000/admin/
```

---

# 二、建立 `CoupleInvitation` model

建立檔案：`couples/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class CoupleInvitation(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invitations"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_invitations"
    )
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"
```

## 說明

- `sender`：送出邀請的人
- `receiver`：收到邀請的人
- `status`：邀請狀態，預設為 `pending`
- `created_at`：建立時間

執行：

```bash
python manage.py makemigrations couples
python manage.py migrate
```

建立檔案：`couples/admin.py`

```python
from django.contrib import admin
from .models import CoupleInvitation

admin.site.register(CoupleInvitation)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# 三、建立 `CoupleRelationship` model

修改檔案：`couples/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class CoupleInvitation(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invitations"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_invitations"
    )
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"


class CoupleRelationship(models.Model):
    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="relationship_user1"
    )
    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="relationship_user2"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_1} ❤️ {self.user_2}"
```

執行：

```bash
python manage.py makemigrations couples
python manage.py migrate
```

修改檔案：`couples/admin.py`

```python
from django.contrib import admin
from .models import CoupleInvitation, CoupleRelationship

admin.site.register(CoupleInvitation)
admin.site.register(CoupleRelationship)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# 四、建立 `Category` model

修改檔案：`places/models.py`

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

執行：

```bash
python manage.py makemigrations places
python manage.py migrate
```

建立檔案：`places/admin.py`

```python
from django.contrib import admin
from .models import Category

admin.site.register(Category)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# 五、建立 `Tag` model

修改檔案：`places/models.py`

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

執行：

```bash
python manage.py makemigrations places
python manage.py migrate
```

修改檔案：`places/admin.py`

```python
from django.contrib import admin
from .models import Category, Tag

admin.site.register(Category)
admin.site.register(Tag)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# 六、建立 `Place` model

修改檔案：`places/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)

    google_map_link = models.URLField(blank=True)
    note = models.TextField(blank=True)
    budget = models.CharField(max_length=50, blank=True)

    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

執行：

```bash
python manage.py makemigrations places
python manage.py migrate
```

修改檔案：`places/admin.py`

```python
from django.contrib import admin
from .models import Category, Tag, Place

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Place)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# 七、建立 `PlaceTag` model

修改檔案：`places/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)

    google_map_link = models.URLField(blank=True)
    note = models.TextField(blank=True)
    budget = models.CharField(max_length=50, blank=True)

    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PlaceTag(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.place} - {self.tag}"
```

執行：

```bash
python manage.py makemigrations places
python manage.py migrate
```

修改檔案：`places/admin.py`

```python
from django.contrib import admin
from .models import Category, Tag, Place, PlaceTag

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(PlaceTag)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# 八、建立 `Memory` model

修改檔案：`memories/models.py`

```python
from django.db import models
from django.contrib.auth.models import User
from places.models import Place

class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    visit_date = models.DateField()
    comment = models.TextField(blank=True)

    rating = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.place}"
```

執行：

```bash
python manage.py makemigrations memories
python manage.py migrate
```

修改檔案：`memories/admin.py`

```python
from django.contrib import admin
from .models import Memory

admin.site.register(Memory)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# 九、建立 `MemoryPhoto` model

修改檔案：`memories/models.py`

```python
from django.db import models
from django.contrib.auth.models import User
from places.models import Place


class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    visit_date = models.DateField()
    comment = models.TextField(blank=True)

    rating = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.place}"

class MemoryPhoto(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="memory_photos/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.memory}"

```

執行：

```bash
python manage.py makemigrations memories
python manage.py migrate
```

修改檔案：`memories/admin.py`

```python
from django.contrib import admin
from .models import Memory, MemoryPhoto

admin.site.register(Memory)
admin.site.register(MemoryPhoto)
```

啟動伺服器：

```bash
python manage.py runserver
```

---

# Admin 後台確認項目

在 admin 中應可管理以下資料：

- [x] User
- [x] Profile
- [x] Couple Invitation
- [x] Couple Relationship
- [x] Category
- [x] Tag
- [x] Place
- [x] PlaceTag
- [x] Memory
- [x] MemoryPhoto

請確認以上項目都有出現在：

```text
http://127.0.0.1:8000/admin/
```

---

# 本週成果

本週已完成核心資料表與後台管理設定，為後續功能開發奠定基礎。

完成內容包含：

- 使用者個人資料模型
- 情侶邀請與關係模型
- 地點分類與標籤模型
- 地點資料模型
- 回憶紀錄與照片模型
- Django Admin 管理介面註冊

# 第 2 週

## 目標
完成 WhereNow 系統的核心資料模型（Models）建立，並在 Django Admin 後台註冊與測試資料表。

本週主要建立系統的基礎資料結構，包括：

- 使用者個人資料
- 情侶邀請與關係
- 地點分類與標籤
- 地點清單
- 回憶紀錄與照片

這些資料模型將作為後續功能開發的基礎。

---

# 本週完成內容

本週完成以下 Models 建立：

- `Profile`
- `CoupleInvitation`
- `CoupleRelationship`
- `Category`
- `Tag`
- `Place`
- `PlaceTag`
- `Memory`
- `MemoryPhoto`

並完成：

- Django Admin 註冊
- 資料表 migration
- Admin 後台測試

---

# 一、建立 Profile Model

檔案位置

```
users/models.py
```

程式碼：

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

### 欄位說明

| 欄位 | 說明 |
|-----|-----|
| user | 連結 Django 內建 User |
| nickname | 使用者暱稱 |
| avatar | 使用者頭像 |
| bio | 自我介紹 |

---

# 二、建立 CoupleInvitation Model

檔案位置

```
couples/models.py
```

程式碼：

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

### 功能說明

此模型用來記錄情侶邀請。

| 欄位 | 說明 |
|-----|-----|
| sender | 發送邀請的使用者 |
| receiver | 接收邀請的使用者 |
| status | 邀請狀態 |
| created_at | 建立時間 |

---

# 三、建立 CoupleRelationship Model

檔案位置

```
couples/models.py
```

程式碼：

```python
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

### 功能說明

此模型用來記錄情侶關係。

| 欄位 | 說明 |
|-----|-----|
| user_1 | 情侶其中一方 |
| user_2 | 情侶另一方 |
| is_active | 是否仍為情侶關係 |
| created_at | 建立時間 |

---

# 四、建立 Category Model

檔案位置

```
places/models.py
```

程式碼：

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

### 功能說明

用來分類地點，例如：

- 餐廳
- 咖啡廳
- 景點
- 旅遊地

---

# 五、建立 Tag Model

檔案位置

```
places/models.py
```

程式碼：

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

### 功能說明

Tag 用來描述地點特性，例如：

- 約會
- 夜景
- 平價
- 拍照

---

# 六、建立 Place Model

檔案位置

```
places/models.py
```

程式碼：

```python
from django.contrib.auth.models import User


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

### 功能說明

Place 用來記錄使用者想去或去過的地點。

---

# 七、建立 PlaceTag Model

檔案位置

```
places/models.py
```

程式碼：

```python
class PlaceTag(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.place} - {self.tag}"
```

### 功能說明

此模型用來建立 **Place 與 Tag 的多對多關係**。

---

# 八、建立 Memory Model

檔案位置

```
memories/models.py
```

程式碼：

```python
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

### 功能說明

Memory 用來記錄使用者在某個地點的回憶。

---

# 九、建立 MemoryPhoto Model

檔案位置

```
memories/models.py
```

程式碼：

```python
class MemoryPhoto(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="memory_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.memory}"
```

### 功能說明

此模型用來儲存回憶照片。

---

# 十、Migration 與 Admin 設定

建立資料表：

```
python manage.py makemigrations
python manage.py migrate
```

建立管理員帳號：

```
python manage.py createsuperuser
```

啟動伺服器：

```
python manage.py runserver
```

登入 Admin：

```
http://127.0.0.1:8000/admin/
```

---

# Admin 後台確認

Admin 中應可管理以下資料：

- User
- Profile
- CoupleInvitation
- CoupleRelationship
- Category
- Tag
- Place
- PlaceTag
- Memory
- MemoryPhoto

---

# 本週成果

本週完成 WhereNow 系統的核心資料模型設計與建立，包括：

- 使用者個人資料模型
- 情侶邀請與關係模型
- 地點分類與標籤模型
- 地點清單模型
- 回憶紀錄模型
- 回憶照片模型

並成功在 Django Admin 後台完成註冊與測試，確認資料表可正常建立與管理。

這些資料模型將作為後續功能開發（例如地點管理、回憶功能與情侶共享功能）的基礎。

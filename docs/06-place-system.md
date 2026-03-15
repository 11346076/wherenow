# Place System（地點管理系統）

## 開發時間
2026/03/15

---

# 系統目標

建立地點管理功能，讓使用者可以記錄曾經去過或想去的地點。

每個使用者可以建立自己的地點清單，並記錄地點相關資訊，例如：

- 地點名稱
- 地區
- 地點分類
- Google Map 連結
- 預算
- 備註
- 是否公開

本模組同時也是 **Memory 回憶功能的基礎模組**，未來回憶資料會與地點進行關聯。

---

# 資料模型

本模組包含四個主要資料表：

- Category（地點分類）
- Tag（地點標籤）
- Place（地點資料）
- PlaceTag（地點標籤關聯）

---

# Category

用途：紀錄地點分類

```python
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

## 欄位說明

| 欄位 | 用途 |
|-----|------|
| name | 地點分類名稱 |

### 範例資料

- 咖啡廳
- 景觀餐廳
- 甜點店
- 約會景點

---

# Tag

用途：紀錄地點標籤

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

## 欄位說明

| 欄位 | 用途 |
|-----|------|
| name | 標籤名稱 |

### 範例資料

- 浪漫
- 夜景
- 平價
- 室內

---

# Place

用途：紀錄使用者建立的地點資料

```python
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

## 欄位說明

| 欄位 | 用途 |
|-----|------|
| user | 建立地點的使用者 |
| category | 地點分類 |
| name | 地點名稱 |
| region | 地區 |
| google_map_link | Google Map 連結 |
| note | 備註 |
| budget | 預算 |
| is_public | 是否公開 |
| created_at | 建立時間 |

---

# PlaceTag

用途：建立地點與標籤之間的關聯。

一個地點可以有多個標籤，因此透過關聯表實現多對多關係。

```python
class PlaceTag(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.place} - {self.tag}"
```

## 欄位說明

| 欄位 | 用途 |
|-----|------|
| place | 地點 |
| tag | 標籤 |

---

# 功能一：新增地點

登入使用者可以新增地點資料。

## URL

```
/places/create/
```

## 功能流程

1. 使用者填寫地點資料
2. 提交表單
3. 系統建立 Place 資料
4. 導向地點列表頁

## 表單

```python
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            "category",
            "name",
            "region",
            "google_map_link",
            "note",
            "budget",
            "is_public"
        ]
```

---

# 功能二：查看地點列表

使用者可以查看自己建立的所有地點。

## URL

```
/places/
```

## 頁面顯示

```
我的地點列表

林昕玫
分類：景觀餐廳
地區：TW
預算：500
公開：True
建立時間：2026/03/15
```

---

# 功能三：查看地點詳細資料

使用者可以查看地點完整資訊。

## URL

```
/places/<place_id>/
```

## 顯示內容

- 地點名稱
- 地點分類
- 地區
- Google Map 連結
- 備註
- 預算
- 是否公開
- 建立時間

---

# 功能四：編輯地點

使用者可以修改自己建立的地點資料。

## URL

```
/places/<place_id>/edit/
```

## View 邏輯

```python
@login_required
def place_update(request, pk):
    place = get_object_or_404(
        Place,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        form = PlaceForm(request.POST, instance=place)

        if form.is_valid():
            form.save()
            return redirect("place_detail", pk=place.pk)

    else:
        form = PlaceForm(instance=place)

    return render(request, "places/place_form.html", {"form": form})
```

---

# 功能五：刪除地點

使用者可以刪除自己建立的地點。

## URL

```
/places/<place_id>/delete/
```

## View 邏輯

```python
@login_required
def place_delete(request, pk):
    place = get_object_or_404(
        Place,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        place.delete()
        return redirect("place_list")

    return render(
        request,
        "places/place_confirm_delete.html",
        {"place": place}
    )
```

---

# 系統流程

```
User
 │
 │ 新增地點
 ▼
Place
 │
 ├── 查看列表
 │
 ├── 查看詳細
 │
 ├── 編輯
 │
 └── 刪除
```

---

# Admin 後台確認

在 Django Admin 中可以查看：

- Categories
- Tags
- Places
- PlaceTags

範例資料：

```
林昕玫
分類：景觀餐廳
地區：TW
預算：500
公開：True
```

---

# 本模組成果

本模組完成以下功能：

- 地點分類系統
- 地點新增
- 地點列表
- 地點詳細頁
- 地點編輯
- 地點刪除
- Django Admin 管理

地點系統完成後，系統已具備 **地點資料管理能力**，並可支援後續功能：

- Memory 回憶系統
- 收藏地點
- 情侶共享地點
- 公開地點探索

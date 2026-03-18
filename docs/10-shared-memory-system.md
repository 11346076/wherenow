# Shared Memory System（情侶共享回憶系統）

## 開發時間
2026/03/18

---

# 系統目標

建立情侶共享回憶功能，讓已建立情侶關係的使用者，可以將自己的回憶資料分享給對方查看。

本模組與以下系統整合：

- Couple 情侶關係系統
- Memory 回憶系統
- Place 地點系統

系統提供以下功能：

- 建立回憶時可選擇是否與情侶共享
- 查看自己與情侶共享的回憶列表
- 查看共享回憶詳細內容
- 編輯回憶時可修改共享狀態
- 解除情侶關係後不再顯示對方共享回憶

---

# 資料模型

本模組延伸既有資料表：

- Memory（回憶資料）

新增欄位：

- shared_with_couple（是否與情侶共享）

---

# Memory

用途：紀錄使用者的地點回憶資料，並可設定是否共享給情侶。

```python
from django.core.validators import MinValueValidator, MaxValueValidator

class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='memories')

    visit_date = models.DateField()
    comment = models.TextField(blank=True)

    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    cost = models.IntegerField(default=0)

    recommended = models.BooleanField(default=False)
    shared_with_couple = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.place.name} - {self.visit_date}"
```

---

## 欄位說明

| 欄位 | 用途 |
|------|------|
| user | 建立回憶的使用者 |
| place | 關聯的地點 |
| visit_date | 造訪日期 |
| comment | 回憶心得 |
| rating | 評分（0～5） |
| cost | 花費 |
| recommended | 是否推薦 |
| shared_with_couple | 是否與情侶共享 |
| created_at | 建立時間 |

---

# 功能一：查看共享回憶列表

使用者可在回憶列表中，同時查看：

- 自己建立的所有回憶
- 情侶建立且有共享的回憶

---

## URL

```
/memories/
```

---

## 功能流程

1. 使用者進入回憶列表頁面  
2. 系統判斷是否存在有效情侶關係  
3. 若有情侶：
   - 顯示自己的回憶
   - 顯示對方 shared_with_couple=True 的回憶  
4. 若沒有情侶：
   - 只顯示自己的回憶  
5. 依照建立時間排序  

---

## View 邏輯

```python
from django.db.models import Q

@login_required
def memory_list(request):
    partner = get_partner(request.user)

    if partner:
        memories = Memory.objects.filter(
            Q(user=request.user) |
            Q(user=partner, shared_with_couple=True)
        ).order_by('-created_at')
    else:
        memories = Memory.objects.filter(
            user=request.user
        ).order_by('-created_at')

    return render(request, 'memories/memory_list.html', {
        'memories': memories,
        'partner': partner
    })
```

---

# 功能二：建立共享回憶

使用者建立回憶時，可勾選是否與情侶共享。

---

## URL

```
/memories/create/
```

---

## View 邏輯

```python
@login_required
def memory_create(request):
    if request.method == 'POST':
        place_id = request.POST.get('place')
        place = Place.objects.get(id=place_id)

        memory = Memory.objects.create(
            user=request.user,
            place=place,
            visit_date=request.POST.get('visit_date'),
            comment=request.POST.get('comment'),
            rating=request.POST.get('rating') or 0,
            cost=request.POST.get('cost') or 0,
            recommended=True if request.POST.get('recommended') else False,
            shared_with_couple=True if request.POST.get('shared_with_couple') else False,
        )

        for image in request.FILES.getlist('images'):
            MemoryPhoto.objects.create(
                memory=memory,
                image=image
            )

        return redirect('memory_detail', pk=memory.pk)

    places = Place.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'memories/memory_create.html', {'places': places})
```

---

# 功能三：查看共享回憶詳細頁

---

## URL

```
/memories/<id>/
```

---

## 權限規則

- 自己建立的回憶 → 可查看  
- 情侶建立且 shared_with_couple=True → 可查看  
- 其他 → 拒絕存取  

---

## View 邏輯

```python
from django.http import Http404

@login_required
def memory_detail(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    partner = get_partner(request.user)

    can_view = False

    if memory.user == request.user:
        can_view = True
    elif partner and memory.user == partner and memory.shared_with_couple:
        can_view = True

    if not can_view:
        raise Http404("你沒有權限查看這個回憶")

    photos = memory.photos.all()

    return render(request, 'memories/memory_detail.html', {
        'memory': memory,
        'photos': photos,
    })
```

---

# 功能四：編輯回憶共享狀態

---

## URL

```
/memories/<id>/edit/
```

---

## View 邏輯

```python
@login_required
def memory_edit(request, pk):
    memory = get_object_or_404(Memory, pk=pk, user=request.user)

    if request.method == 'POST':
        place_id = request.POST.get('place')
        memory.place = Place.objects.get(id=place_id)
        memory.visit_date = request.POST.get('visit_date')
        memory.comment = request.POST.get('comment')
        memory.rating = request.POST.get('rating') or 0
        memory.cost = request.POST.get('cost') or 0
        memory.recommended = True if request.POST.get('recommended') else False
        memory.shared_with_couple = True if request.POST.get('shared_with_couple') else False
        memory.save()

        for image in request.FILES.getlist('images'):
            MemoryPhoto.objects.create(
                memory=memory,
                image=image
            )

        return redirect('memory_detail', pk=memory.pk)

    places = Place.objects.filter(user=request.user).order_by('-created_at')
    photos = memory.photos.all()

    return render(request, 'memories/memory_edit.html', {
        'memory': memory,
        'places': places,
        'photos': photos,
    })
```

---

# 功能五：解除情侶後停止共享

本模組依賴 CoupleRelationship 的 `is_active=True` 判斷共享關係。

## 規則

- 解除情侶後：
  - 對方共享回憶不再顯示
  - 自己資料仍保留
  - 回憶資料不刪除

---

# 系統流程

```
User
 │
 │ 進入 Memory List
 ▼
讀取 CoupleRelationship
 │
 ├─ 有情侶 → 顯示雙方共享資料
 └─ 無情侶 → 只顯示自己資料
```

---

# 功能限制

- 必須登入才能使用
- 只有建立者可編輯與刪除回憶
- 只有建立者可刪除照片
- 詳細頁需通過共享權限檢查
- 共享僅限 shared_with_couple=True
- 解除情侶後停止共享

---

# 與其他模組整合

## Couple 模組

- 判斷是否有情侶
- 取得 partner
- 控制共享顯示

## Place 模組

- 回憶需關聯地點
- 顯示地點資訊

## MemoryPhoto 模組

- 支援多張照片
- 可刪除照片

---

# Admin 後台確認

可查看：

- Memories
- MemoryPhotos

---

## 範例資料

```
user: text1
place: 一中街
visit_date: 2026-03-19
shared_with_couple: True
```

---

# 本模組成果

本模組完成：

- 新增共享欄位
- 查看共享回憶
- 建立共享回憶
- 權限控管
- 編輯共享狀態
- 情侶解除後停止共享
- 與多模組整合

---

# 未來擴充

- 回憶時間軸
- 情侶回憶牆
- 留言功能
- 搜尋功能
- 標籤分類

---

# 總結

Shared Memory System 提供情侶之間的回憶共享功能，使 WhereNow 從單人記錄系統進化為雙人互動平台，提升系統情感價值與使用黏著度。

# Couple Home System（情侶首頁系統）

## 開發時間
2026/03/18

---

# 系統目標

建立情侶首頁功能，讓已建立情侶關係的兩位使用者可以在同一頁面查看彼此的關係資訊與共享資料摘要。

本模組整合：

- Couple 情侶關係系統
- Place 地點系統
- Memory 回憶系統

情侶首頁提供以下功能：

- 顯示目前情侶對象
- 設定與查看在一起紀念日
- 計算已在一起天數
- 顯示共同地點數量
- 顯示共同回憶數量
- 顯示最近共享回憶

---

# 資料模型

本模組主要延伸既有資料表：

- CoupleRelationship（情侶關係）

新增欄位：

- anniversary_date（在一起紀念日）

---

# CoupleRelationship

用途：紀錄情侶關係與紀念日資訊。

```python
class CoupleRelationship(models.Model):
    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relationship_user1'
    )
    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relationship_user2'
    )
    is_active = models.BooleanField(default=True)
    anniversary_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_1} ❤️ {self.user_2}"
```

## 欄位說明

| 欄位 | 用途 |
|------|------|
| user_1 | 情侶使用者 1 |
| user_2 | 情侶使用者 2 |
| is_active | 是否為目前有效關係 |
| anniversary_date | 在一起紀念日 |
| created_at | 建立時間 |

---

# 功能一：情侶首頁

已建立情侶關係的使用者可以進入情侶首頁，查看目前關係與共享資料摘要。

## URL

```
/couples/home/
```

## 顯示內容

- 目前情侶對象
- 在一起紀念日
- 已在一起幾天
- 共同地點數
- 共同回憶數
- 最近共享回憶

## View 邏輯

```python
from datetime import date
from django.db.models import Q
from places.models import Place
from memories.models import Memory


@login_required
def couple_home(request):
    relationship, partner = get_relationship_and_partner(request.user)

    days_together = None
    shared_place_count = 0
    shared_memory_count = 0
    recent_memories = []

    if relationship and partner:
        if relationship.anniversary_date:
            days_together = (date.today() - relationship.anniversary_date).days

        shared_place_count = Place.objects.filter(
            Q(user=request.user, shared_with_couple=True) |
            Q(user=partner, shared_with_couple=True)
        ).count()

        shared_memory_count = Memory.objects.filter(
            Q(user=request.user, shared_with_couple=True) |
            Q(user=partner, shared_with_couple=True)
        ).count()

        recent_memories = Memory.objects.filter(
            Q(user=request.user, shared_with_couple=True) |
            Q(user=partner, shared_with_couple=True)
        ).order_by('-created_at')[:5]

    return render(request, 'couples/couple_home.html', {
        'relationship': relationship,
        'partner': partner,
        'days_together': days_together,
        'shared_place_count': shared_place_count,
        'shared_memory_count': shared_memory_count,
        'recent_memories': recent_memories,
    })
```

---

# 功能二：設定紀念日

已建立情侶關係的使用者可以設定或修改在一起紀念日。

## URL

```
/couples/anniversary/edit/
```

## 功能流程

1. 使用者進入紀念日設定頁面  
2. 系統讀取目前情侶關係資料  
3. 使用者輸入日期  
4. 系統更新 `CoupleRelationship` 的 `anniversary_date`  
5. 返回情侶首頁顯示結果  

## View 邏輯

```python
@login_required
def edit_anniversary(request):
    relationship, partner = get_relationship_and_partner(request.user)

    if not relationship:
        return redirect('couple_status')

    if request.method == 'POST':
        anniversary_date = request.POST.get('anniversary_date')
        relationship.anniversary_date = anniversary_date or None
        relationship.save()
        return redirect('couple_home')

    return render(request, 'couples/edit_anniversary.html', {
        'relationship': relationship,
        'partner': partner
    })
```

---

# 功能三：計算在一起天數

系統會依照使用者設定的紀念日，自動計算目前已在一起幾天。

## 計算方式

```python
from datetime import date

days_together = None
if relationship and relationship.anniversary_date:
    days_together = (date.today() - relationship.anniversary_date).days
```

## 顯示範例

```
我的情侶：text2
在一起紀念日：2026-03-18
已經在一起：12 天
```

---

# 功能四：統計共享地點與共享回憶

情侶首頁會統計雙方共享的 Place 與 Memory 資料數量。

## 共同地點數

```python
shared_place_count = Place.objects.filter(
    Q(user=request.user, shared_with_couple=True) |
    Q(user=partner, shared_with_couple=True)
).count()
```

## 共同回憶數

```python
shared_memory_count = Memory.objects.filter(
    Q(user=request.user, shared_with_couple=True) |
    Q(user=partner, shared_with_couple=True)
).count()
```

## 顯示範例

```
共同地點數：5
共同回憶數：3
```

---

# 功能五：顯示最近共享回憶

情侶首頁會列出最近新增的共享回憶資料，作為快速查看入口。

## 查詢邏輯

```python
recent_memories = Memory.objects.filter(
    Q(user=request.user, shared_with_couple=True) |
    Q(user=partner, shared_with_couple=True)
).order_by('-created_at')[:5]
```

## 顯示內容

- 地點名稱
- 造訪日期
- 建立者

## 顯示範例

```
最近共享回憶
一中街 - 2026-03-19（text1）
林昕玫 - 2026-03-17（text2）
```

---

# 頁面設計

本模組新增兩個主要頁面：

- `couple_home.html`
- `edit_anniversary.html`

## couple_home.html 顯示內容

- 情侶名稱
- 紀念日
- 在一起天數
- 共同地點數
- 共同回憶數
- 最近共享回憶
- 快速連結按鈕

## edit_anniversary.html 顯示內容

- 目前情侶名稱
- 日期輸入欄位
- 儲存按鈕

---

# 系統流程

```
User
 │
 │ 進入情侶首頁
 ▼
讀取 CoupleRelationship
 │
 ├─ 顯示 partner
 ├─ 顯示 anniversary_date
 ├─ 計算 days_together
 ├─ 統計 shared_place_count
 ├─ 統計 shared_memory_count
 └─ 顯示 recent_memories
```

---

# 功能限制

為確保資料正確性，本模組加入以下限制：

- 只有建立情侶關係的使用者可以進入情侶首頁
- 若尚未建立情侶關係，系統導向情侶狀態頁
- 只有有效關係（`is_active=True`）才可顯示首頁內容
- 共同地點與共同回憶只統計 `shared_with_couple=True` 的資料
- 解除情侶關係後，首頁資料不再顯示共享內容

---

# 與其他模組整合

本模組與以下系統模組整合：

## Couple 模組

- 讀取目前情侶關係
- 顯示 partner
- 設定 anniversary_date

## Place 模組

- 統計共同地點數
- 提供共享地點資料來源

## Memory 模組

- 統計共同回憶數
- 顯示最近共享回憶

---

# Admin 後台確認

在 Django Admin 中可以查看：

- Couple Invitations
- Couple Relationships

## 範例資料

```
user_1: text1
user_2: text2
is_active: True
anniversary_date: 2026-03-18
created_at: 2026-03-18 07:33
```

---

# 本模組成果

本模組完成以下功能：

- 情侶首頁頁面
- 設定與修改紀念日
- 自動計算在一起天數
- 顯示共同地點數
- 顯示共同回憶數
- 顯示最近共享回憶
- 整合 Couple / Place / Memory 三個模組

情侶首頁完成後，系統不再只是單純的資料管理系統，而是提升為具有情感紀錄與雙人互動特色的情侶平台。

---

# 未來擴充

- 顯示情侶頭像與暱稱
- 顯示更多共同統計資料
- 回憶時間軸
- 情侶共同抽選地點
- 情侶首頁儀表板（Dashboard）

---

# 總結

Couple Home System 提供情侶關係的整合首頁，將紀念日、共享地點、共享回憶等功能集中呈現，提升系統完整性、互動性與情感價值，也使 WhereNow 更接近實際應用型 Web 系統。

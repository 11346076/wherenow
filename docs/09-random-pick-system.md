# Random Pick System（隨機抽選系統）

## 開發時間
2026/03/18

---

# 系統目標

建立隨機抽選功能，讓使用者可以從自己建立的地點清單中隨機抽出一個地點，幫助解決「今天要去哪裡」的問題。

本模組與 **Place 地點系統** 整合，抽選來源為使用者自己建立的地點資料。

系統提供以下功能：

- 從自己的地點清單中隨機抽出一個地點
- 顯示抽選結果
- 記錄每次抽選歷史
- 查看過去的抽選紀錄

---

# 資料模型

本模組主要新增一個資料表：

- RandomPickHistory（隨機抽選紀錄）

---

# RandomPickHistory

用途：紀錄使用者每次隨機抽選的結果。

```python
class RandomPickHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='random_pick_histories')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='random_pick_histories')
    picked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 抽到了 {self.place.name}"
```

## 欄位說明

| 欄位 | 用途 |
|------|------|
| user | 進行抽選的使用者 |
| place | 被抽中的地點 |
| picked_at | 抽選時間 |

---

# 功能一：隨機抽選地點

登入使用者可以從自己的地點清單中隨機抽出一個地點。

## URL

```
/places/random-pick/
```

---

## 功能流程

1. 使用者進入隨機抽選頁面  
2. 點擊「抽一個地點」按鈕  
3. 系統讀取目前使用者建立的地點資料  
4. 從地點清單中隨機選出一筆資料  
5. 顯示抽選結果  
6. 將本次結果記錄到 RandomPickHistory  

---

## View 邏輯

```python
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RandomPickHistory
from places.models import Place


@login_required
def random_pick(request):
    picked_place = None
    error = None

    if request.method == 'POST':
        places = Place.objects.filter(user=request.user)

        if not places.exists():
            error = '目前沒有可供抽選的地點，請先新增地點。'
        else:
            picked_place = random.choice(list(places))

            RandomPickHistory.objects.create(
                user=request.user,
                place=picked_place
            )

    return render(request, 'places/random_pick.html', {
        'picked_place': picked_place,
        'error': error
    })
```

---

# 功能二：查看抽選結果

系統會在抽選完成後顯示抽到的地點資訊。

## 顯示內容

- 地點名稱
- 地區
- 預算
- 備註

---

## 頁面範例

```
你抽到的是：

地點名稱：台中一中街
地區：台中
預算：200
備註：晚上可以去逛街吃東西
```

---

# 功能三：查看抽選歷史

使用者可以查看自己過去所有的抽選紀錄。

## URL

```
/places/random-pick-history/
```

---

## 功能流程

1. 使用者進入抽選歷史頁面  
2. 系統讀取目前使用者的抽選紀錄  
3. 依照抽選時間由新到舊排序顯示  

---

## View 邏輯

```python
@login_required
def random_pick_history(request):
    histories = RandomPickHistory.objects.filter(
        user=request.user
    ).select_related('place').order_by('-picked_at')

    return render(
        request,
        'places/random_pick_history.html',
        {'histories': histories}
    )
```

---

## 頁面顯示

```
2026-03-18 06:35：台中一中街
2026-03-18 06:35：景觀餐廳
2026-03-18 06:35：甜點店
```

---

# 功能限制

為確保系統邏輯正確，本模組加入以下限制：

- 只能從登入使用者自己的地點中抽選
- 若使用者尚未建立任何地點，系統顯示提示訊息
- 每次抽選都會新增一筆歷史紀錄

---

# 系統流程

```
User
 │
 │ 進入隨機抽選頁面
 ▼
Random Pick
 │
 │ 點擊抽選按鈕
 ▼
讀取 Place 資料
 │
 │ 隨機選出一筆
 ▼
顯示抽選結果
 │
 └── 寫入 RandomPickHistory
```

---

# 與 Place 模組整合

本模組直接使用 Place 系統中的地點資料作為抽選來源，因此與 Place 模組高度整合。

## 整合內容

- 讀取使用者自己的 Place 資料
- 顯示 Place 的基本資訊
- 建立與 Place 的歷史關聯紀錄

---

# Admin 後台確認

在 Django Admin 中可以查看：

- RandomPickHistories

## 範例資料

```
user: 林昕玫
place: 台中一中街
picked_at: 2026/03/18 06:35
```

---

# 本模組成果

本模組完成以下功能：

- 隨機抽選地點
- 顯示抽選結果
- 記錄抽選歷史
- 查看歷史紀錄
- 與 Place 系統整合

Random Pick 系統完成後，系統已具備 **地點隨機推薦能力**，可支援使用者快速決定想去的地點，也提升整體系統的互動性與趣味性。

---

# 未來擴充

- 依分類進行抽選
- 依地區進行抽選
- 避免重複抽到近期地點
- 情侶共同抽選功能

---

# 總結

Random Pick 模組提供使用者快速決策的功能，提升系統互動性與趣味性，並與 Place 系統深度整合，為未來推薦系統奠定基礎。

# Favorite Place System（收藏地點系統）

## 開發時間
2026/03/18

---

# 本週目標

建立 Favorite Place（收藏地點）模組，讓使用者可以收藏其他使用者的公開地點，並管理自己的收藏清單。

---

# 系統名稱

**Favorite Place（收藏地點系統）**

---

# 系統目標

提供使用者收藏與管理地點的功能，讓使用者可以：

- 收藏其他使用者的公開地點
- 建立個人收藏清單
- 快速查看感興趣的地點
- 取消收藏

本模組強化系統的「探索與記錄」體驗，並與 Place 模組進行整合。

---

# 本週完成內容

- 建立 FavoritePlace 資料模型
- 完成收藏功能（新增收藏）
- 完成取消收藏功能
- 建立收藏清單頁面
- 完成與 Place 模組整合
- 限制僅能收藏公開地點
- 限制不可收藏自己的地點

---

# 一、資料模型設計

## FavoritePlace（收藏地點）

用途：紀錄使用者收藏的地點

```python
class FavoritePlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.place.name}"
```

## 設計說明

- 一個使用者可以收藏多個地點
- 一個地點可以被多個使用者收藏
- 屬於 Many-to-Many 關係（透過 FavoritePlace 實現）
- 使用 `unique_together` 避免重複收藏

---

# 二、功能設計

## 1️⃣ 收藏地點功能

使用者可在地點詳細頁點擊「收藏」按鈕：

- 僅限登入使用者
- 僅能收藏公開地點
- 不可收藏自己的地點
- 若已收藏則不重複新增

---

## 2️⃣ 取消收藏功能

使用者可從收藏清單中取消收藏：

- 刪除 FavoritePlace 紀錄
- 即時更新收藏列表

---

## 3️⃣ 收藏清單頁

顯示目前使用者收藏的所有地點：

### 顯示內容

- 地點名稱
- 地區
- 分類
- 查看地點連結
- 取消收藏按鈕

---

# 三、View 設計

## 新增收藏

```python
@login_required
def add_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id, is_public=True)

    if place.user != request.user:
        FavoritePlace.objects.get_or_create(user=request.user, place=place)

    return redirect('place_detail', pk=place.id)
```

---

## 取消收藏

```python
@login_required
def remove_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    FavoritePlace.objects.filter(user=request.user, place=place).delete()

    return redirect('favorite_list')
```

---

## 收藏清單

```python
@login_required
def favorite_list(request):
    favorites = FavoritePlace.objects.filter(user=request.user).select_related('place')
    return render(request, 'places/favorite_list.html', {'favorites': favorites})
```

---

# 四、URL 設計

```python
path('favorites/', views.favorite_list, name='favorite_list'),
path('favorite/add/<int:place_id>/', views.add_favorite, name='add_favorite'),
path('favorite/remove/<int:place_id>/', views.remove_favorite, name='remove_favorite'),
```

---

# 五、Template 設計

## 收藏清單頁（favorite_list.html）

```html
<h2>我的收藏地點</h2>

{% if favorites %}
    <ul>
        {% for favorite in favorites %}
            <li>
                <strong>{{ favorite.place.name }}</strong><br>
                地區：{{ favorite.place.region }}<br>
                分類：{{ favorite.place.category.name }}<br>
                <a href="{% url 'place_detail' favorite.place.id %}">查看地點</a>
                |
                <a href="{% url 'remove_favorite' favorite.place.id %}">取消收藏</a>
            </li>
            <hr>
        {% endfor %}
    </ul>
{% else %}
    <p>目前沒有收藏任何地點。</p>
{% endif %}
```

---

# 六、系統流程

## 收藏流程

1. 使用者進入地點詳細頁  
2. 點擊「收藏地點」  
3. 系統建立 FavoritePlace 資料  
4. 重新導向回地點頁面  

---

## 查看收藏流程

1. 使用者進入收藏頁  
2. 系統讀取 FavoritePlace 資料  
3. 顯示收藏地點列表  

---

## 取消收藏流程

1. 使用者點擊「取消收藏」  
2. 系統刪除 FavoritePlace 資料  
3. 更新收藏清單  

---

# 七、功能限制

- 必須登入才可使用
- 僅能收藏公開地點
- 不可收藏自己的地點
- 不可重複收藏

---

# 八、與其他模組關聯

- 與 Place 模組關聯（ForeignKey）
- 與 User 模組關聯
- 可作為未來推薦系統與統計功能基礎

---

# 九、未來擴充

- 收藏分類（我的最愛、約會清單）
- 收藏排序功能
- 收藏數量統計
- 推薦熱門地點（依收藏數）

---

# 總結

Favorite Place 模組讓系統具備「收藏與探索」能力，提升使用者互動與留存率，並為後續推薦系統與社交功能提供基礎資料。

# Memory System（回憶管理系統）

## 開發時間
2026/03/18

---

# 本週目標

建立 Memory（回憶管理）模組，完成回憶資料的新增、顯示、編輯與刪除功能，並整合照片上傳與地點關聯。

---

# 本週完成內容

- 建立 Memory 資料模型
- 建立 MemoryPhoto（照片）資料模型
- 建立回憶新增功能（含照片上傳）
- 建立回憶列表頁
- 建立回憶詳細頁（顯示照片）
- 建立回憶編輯功能
- 建立回憶刪除功能
- 建立照片刪除功能
- 完成與 Place 模組關聯

---

# 一、資料模型設計

## Memory（回憶）

用途：記錄使用者的回憶內容

```python
class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='memories')

    visit_date = models.DateField()
    comment = models.TextField(blank=True)

    rating = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
```

---

## MemoryPhoto（回憶照片）

用途：儲存回憶圖片

```python
class MemoryPhoto(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to="memory_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

---

# 二、功能實作

## 1️⃣ 回憶新增（Create）

使用者可建立回憶並上傳多張照片

```python
def memory_create(request):
    if request.method == 'POST':
        memory = Memory.objects.create(...)
        
        for image in request.FILES.getlist('images'):
            MemoryPhoto.objects.create(memory=memory, image=image)
```

### 功能說明

- 建立 Memory 資料
- 同時建立多筆 MemoryPhoto

---

## 2️⃣ 回憶列表（List）

顯示所有回憶資料

```python
def memory_list(request):
    memories = Memory.objects.all().order_by('-created_at')
```

---

## 3️⃣ 回憶詳細頁（Detail）

顯示回憶內容與所有照片

```python
def memory_detail(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    photos = memory.photos.all()
```

---

## 4️⃣ 回憶編輯（Update）

可修改回憶內容，並新增照片

```python
def memory_edit(request, pk):
    memory = get_object_or_404(Memory, pk=pk)

    if request.method == 'POST':
        memory.save()

        for image in request.FILES.getlist('images'):
            MemoryPhoto.objects.create(memory=memory, image=image)
```

---

## 5️⃣ 回憶刪除（Delete）

刪除回憶資料

```python
def memory_delete(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    memory.delete()
```

👉 使用 CASCADE，會連同照片一起刪除

---

## 6️⃣ 單張照片刪除

```python
def memory_photo_delete(request, photo_id):
    photo = get_object_or_404(MemoryPhoto, pk=photo_id)
    photo.delete()
```

---

# 三、URL 設計

```
/memories/                     回憶列表
/memories/create/              新增回憶
/memories/<id>/                回憶詳細頁
/memories/<id>/edit/           編輯回憶
/memories/<id>/delete/         刪除回憶
/memories/photo/<id>/delete/   刪除照片
```

---

# 四、照片上傳設定

## settings.py

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## urls.py

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 表單設定（重要）

```html
<form method="post" enctype="multipart/form-data">
```

---

# 五、系統流程

## 新增回憶流程

1. 使用者填寫資料  
2. 上傳照片  
3. 建立 Memory  
4. 建立多筆 MemoryPhoto  
5. 導向詳細頁  

---

## 編輯回憶流程

1. 修改內容  
2. 可新增照片  
3. 儲存更新  

---

## 刪除回憶流程

1. 點擊刪除  
2. 確認刪除  
3. 刪除 Memory  
4. 相關照片自動刪除  

---

## 刪除照片流程

1. 進入編輯頁  
2. 點擊刪除照片  
3. 確認刪除  
4. 回到編輯頁  

---

# 六、本模組成果

本模組已完成：

- 回憶資料 CRUD 功能
- 與 Place 模組整合
- 多張照片上傳
- 圖片顯示功能
- 照片刪除功能

系統已具備完整回憶管理能力。

---

# 七、下階段規劃

- UI 美化（Bootstrap）
- 回憶卡片設計
- 情侶共享回憶
- 回憶時間軸（Timeline）
- 收藏與推薦系統

---

# 總結

Memory 模組為 WhereNow 系統核心之一，負責回憶資料與照片管理，已完成完整功能實作，並可支援後續社交與共享功能擴展。

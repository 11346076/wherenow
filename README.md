# WhereNow

WhereNow 是一個幫助使用者記錄地點、管理清單與整理回憶的系統。

使用者可以建立自己的地點清單、與伴侶共享地點、並在每個地點留下回憶與照片。

---

## 系統功能

### 使用者系統
- 使用者註冊
- 使用者登入 / 登出
- 個人資料管理
- 頭像上傳

### 情侶關係系統
- 發送情侶邀請
- 接受 / 拒絕邀請
- 建立共享空間

### 地點管理
- 建立地點
- 編輯地點資訊
- 地點分類與標籤

### 回憶紀錄
- 在地點新增回憶
- 上傳照片
- 記錄心情與文字

### API 系統
- 提供 RESTful API
- 支援前端或 App 串接

---

## 技術架構

- Python
- Django
- Django REST Framework
- MySQL
- HTML / CSS / JavaScript

---

## 專案結構

```
WhereNow
│
├─ users        # 使用者系統
├─ couples      # 情侶關係系統
├─ places       # 地點管理
├─ memories     # 回憶紀錄
├─ api          # API 相關
│
├─ templates
├─ static
├─ media
│
└─ manage.py
```

---

## 環境安裝

### 1 建立虛擬環境

```bash
python -m venv venv
```

啟動虛擬環境

```bash
.\venv\Scripts\activate
```

---

### 2 安裝套件

```bash
pip install django
pip install djangorestframework
pip install pymysql
pip install pillow
```

---

### 3 Migration

```bash
python manage.py migrate
```

---

### 4 啟動伺服器

```bash
python manage.py runserver
```

打開瀏覽器：

```
http://127.0.0.1:8000
```
## 開發團隊

- 林昕玫
- 劉明宗


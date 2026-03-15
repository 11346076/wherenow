#開發紀錄
建立時間：2026/03/04
## 本週目標
建立 WhereNow 系統的 Django 專案骨架，完成基本開發環境設定與專案結構建立，為後續功能開發做準備。

---

# 專案名稱

**WhereNow－地點清單與情侶回憶管理系統**

系統概念：

WhereNow 是一個用來記錄與管理地點與回憶的系統，使用者可以：

- 建立自己的地點清單
- 記錄去過的地方
- 撰寫回憶
- 上傳照片
- 與情侶共享回憶

---

# 本週完成內容

- 確定專案名稱
- 規劃核心 Use Case
- 設計系統 ERD
- 建立 Django 專案
- 建立系統 App
- 建立專案資料夾結構
- 建立 Python 虛擬環境
- 安裝必要套件
- 完成 Django Migration
- 成功啟動 Django Server

---

# 一、建立 Django 專案

建立 Django 專案：

```
django-admin startproject wherenow
```

建立完成後的基本結構：

```
wherenow/
│
├─ manage.py
└─ wherenow/
   ├─ __init__.py
   ├─ settings.py
   ├─ urls.py
   ├─ asgi.py
   └─ wsgi.py
```

---

# 二、建立系統 App

建立系統功能模組：

```
python manage.py startapp users
python manage.py startapp couples
python manage.py startapp places
python manage.py startapp memories
python manage.py startapp api
```

建立完成後的專案結構：

```
wherenow/
│
├─ users
├─ couples
├─ places
├─ memories
├─ api
│
└─ wherenow
```

各 App 的功能：

| App | 功能 |
|----|----|
| users | 使用者帳號與個人資料 |
| couples | 情侶關係與邀請 |
| places | 地點資料 |
| memories | 回憶紀錄 |
| api | REST API |

---

# 三、建立專案資料夾

為了管理前端模板、靜態檔案與媒體資料，建立以下資料夾：

```
templates
static
media
logs
locale
docs
```

資料夾用途：

| 資料夾 | 用途 |
|------|------|
| templates | HTML 模板 |
| static | CSS / JS / 圖片 |
| media | 使用者上傳檔案 |
| logs | 系統日誌 |
| locale | 多語系設定 |
| docs | 專案文件 |

---

# 四、建立虛擬環境

建立 Python 虛擬環境：

```
python -m venv venv
```

啟動虛擬環境：

```
.\venv\Scripts\activate
```

啟動後 Terminal 會顯示：

```
(venv)
```

---

# 五、安裝必要套件

安裝 Django 與相關套件：

```
pip install django
pip install djangorestframework
pip install pymysql
pip install pillow
```

套件用途：

| 套件 | 用途 |
|----|----|
| Django | Web Framework |
| djangorestframework | REST API |
| pymysql | MySQL 連線 |
| Pillow | 圖片處理 |

---

# 六、設定 INSTALLED_APPS

在 `settings.py` 中加入建立的 App：

```
INSTALLED_APPS = [
    'users',
    'couples',
    'places',
    'memories',
    'api',
]
```

這樣 Django 才會識別這些應用程式。

---

# 七、資料庫 Migration

初始化資料庫：

```
python manage.py migrate
```

這會建立 Django 預設資料表，例如：

- User
- Session
- Admin
- Auth

---

# 八、啟動 Django Server

啟動開發伺服器：

```
python manage.py runserver
```

開啟瀏覽器：

```
http://127.0.0.1:8000
```

如果看到 Django 預設畫面，代表專案建立成功。

---

# 本週成果

本週成功完成 WhereNow 專案的基本架構，包括：

- Django 專案建立
- App 模組設計
- 開發環境設定
- 虛擬環境建立
- 必要套件安裝
- 專案資料夾結構建立
- Django Server 成功啟動

目前專案已具備基本開發環境，可以開始進行系統資料模型與功能開發。

---

# 下週規劃

下一週將開始建立系統核心資料模型，包括：

- 使用者 Profile
- 情侶邀請與關係
- 地點分類與標籤
- 地點資料
- 回憶紀錄與照片

並完成 Django Admin 管理後台設定。

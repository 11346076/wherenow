# 專案安裝與啟動方式

## 1. 下載專案

```bash
git clone <你的 repository 網址>
```

---

## 2. 進入專案資料夾

```bash
cd wherenow
```

---

## 3. 建立虛擬環境

```bash
python -m venv venv
```

---

## 4. 啟動虛擬環境

```bash
.\venv\Scripts\activate
```

---

## 5. 安裝套件

```bash
pip install django djangorestframework pymysql pillow
```

---

## 6. 執行 migration

```bash
python manage.py migrate
```

---

## 7. 啟動伺服器

```bash
python manage.py runserver
```

---

## 8. 開啟瀏覽器

```text
http://127.0.0.1:8000
```

如果看到 Django 預設畫面，代表啟動成功。

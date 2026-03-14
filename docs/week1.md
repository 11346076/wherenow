# Week 1 開發紀錄

## 本週目標
完成 Django 專案骨架與基本環境設定。

---

## 已完成事項

- [x] 確定專案名稱  
WhereNow－地點清單與情侶回憶管理系統

- [x] 確定 5 個 Use Case

- [x] 完成 ERD 設計

---

## 建立 Django 專案

```bash
django-admin startproject wherenow
```

---

## 建立 App

```bash
python manage.py startapp users
python manage.py startapp couples
python manage.py startapp places
python manage.py startapp memories
python manage.py startapp api
```

---

## 建立專案資料夾

建立以下資料夾：

```
templates
static
media
logs
locale
```

---

## 建立虛擬環境

```bash
python -m venv venv
```

啟動虛擬環境

```bash
.\venv\Scripts\activate
```

---

## 安裝套件

```bash
pip install django
pip install djangorestframework
pip install pymysql
pip install pillow
```

---

## Migration

```bash
python manage.py migrate
```

---

## 啟動 Django Server

```bash
python manage.py runserver
```

打開：

```
http://127.0.0.1:8000
```

如果看到 Django 頁面代表成功。

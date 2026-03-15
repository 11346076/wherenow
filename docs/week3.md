# 第 3 週

## 目標
完成使用者帳號系統的基本功能，包括註冊、登入、登出與首頁流程。

---

## 本週完成內容

- 建立 `users/forms.py`
- 建立註冊表單 `RegisterForm`
- 建立註冊功能 `register_view`
- 建立 `users/urls.py`
- 將 `users` 路由接到主系統
- 建立註冊頁面 `register.html`
- 建立登入頁面 `login.html`
- 使用 Django 內建 `LoginView` 完成登入功能
- 使用 Django 內建 `LogoutView` 完成登出功能
- 建立首頁 `home`
- 確認 `settings.py` 的模板與登入 / 登出跳轉設定
- 測試註冊、登入、登出與首頁流程
- 修正登出 `HTTP 405` 問題（改為使用 `POST` 登出）

---

# 一、建立 `users/forms.py`

在 `users` 資料夾中建立表單檔案：

```
users/forms.py
```

程式碼如下：

```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

### 功能說明

此表單繼承 Django 內建的 `UserCreationForm`，可以自動完成：

- 使用者名稱輸入
- 密碼驗證
- 密碼一致性檢查
- 建立 `User` 帳號

---

# 二、建立註冊功能 `register_view`

檔案位置：

```
users/views.py
```

程式碼如下：

```python
from django.shortcuts import render, redirect
from .forms import RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})
```

### 功能說明

`register_view` 的流程：

1. 使用者進入註冊頁面時顯示空白表單  
2. 使用者送出資料時接收 `POST` 請求  
3. 若資料驗證成功則建立帳號  
4. 註冊完成後跳轉到登入頁  

---

# 三、建立首頁 `home`

檔案位置：

```
wherenow/views.py
```

程式碼如下：

```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

### 功能說明

首頁主要用來：

- 顯示登入中的使用者名稱
- 提供登入 / 註冊 / 登出入口
- 作為登入成功後的跳轉頁面

---

# 四、建立 `users/urls.py`

檔案位置：

```
users/urls.py
```

程式碼如下：

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view

urlpatterns = [
    path('register/', register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),
]
```

### 功能說明

設定以下網址路由：

- `/users/register/` → 註冊頁  
- `/users/login/` → 登入頁  
- `/users/logout/` → 登出  

登入與登出使用 Django 內建：

- `LoginView`
- `LogoutView`

---

# 五、將 users 路由接到主系統

檔案位置：

```
wherenow/urls.py
```

程式碼如下：

```python
from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('users/', include('users.urls')),
]
```

### 功能說明

此設定讓系統可以識別：

- `/` → 首頁  
- `/users/register/`  
- `/users/login/`  
- `/users/logout/`  

---

# 六、建立註冊頁面

檔案位置：

```
templates/users/register.html
```

程式碼：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>
<body>

<h1>註冊帳號</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}

    <button type="submit">註冊</button>
</form>

<p>
已有帳號？
<a href="{% url 'login' %}">前往登入</a>
</p>

</body>
</html>
```

---

# 七、建立登入頁面

檔案位置：

```
templates/users/login.html
```

程式碼：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>

<h1>登入</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}

    <button type="submit">登入</button>
</form>

<p>
沒有帳號？
<a href="{% url 'register' %}">註冊</a>
</p>

</body>
</html>
```

---

# 八、建立首頁模板

檔案位置：

```
templates/home.html
```

程式碼：

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>WhereNow 首頁</title>
</head>
<body>

<h1>歡迎來到 WhereNow</h1>

{% if user.is_authenticated %}
    <p>你好，{{ user.username }}！你已經登入。</p>

    <form method="post" action="{% url 'logout' %}">
        {% csrf_token %}
        <button type="submit">登出</button>
    </form>

{% else %}
    <p>你目前還沒登入。</p>

    <a href="{% url 'login' %}">登入</a>
    <a href="{% url 'register' %}">註冊</a>

{% endif %}

</body>
</html>
```

---

# 九、確認 `settings.py`

檔案位置：

```
wherenow/settings.py
```

### 模板設定

```python
'DIRS': [BASE_DIR / 'templates']
```

### 登入 / 登出跳轉設定

```python
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

---

# 十、測試功能

啟動 Django 伺服器：

```
python manage.py runserver
```

測試網址：

```
http://127.0.0.1:8000/
```

測試流程：

1. 進入註冊頁面  
2. 建立新帳號  
3. 跳轉至登入頁  
4. 使用新帳號登入  
5. 登入成功後進入首頁  
6. 首頁顯示登入使用者名稱  
7. 點擊登出  
8. 回到未登入狀態首頁  

---

# 本週成果

本週已完成 WhereNow 系統的帳號基礎功能：

- 使用者註冊
- 使用者登入
- 使用者登出
- 首頁登入狀態顯示
- 路由整合
- 模板整合
- 功能流程測試

目前系統已具備完整的帳號流程，後續可以繼續開發：

- 個人資料功能
- 頭貼上傳
- 地點清單管理
- 回憶功能
- 情侶共享功能

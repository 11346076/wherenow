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
- 使用 Django 內建 `LoginView` 完成登入功能
- 使用 Django 內建 `LogoutView` 完成登出功能
- 建立簡單首頁 `home`
- 確認 `settings.py` 的模板與登入跳轉設定
- 測試註冊、登入、登出與首頁流程

---

# 一、建立 `users/forms.py`

在 `users` 資料夾裡新增檔案：

```text
users/forms.py
```

貼上以下程式：

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

## 這段程式的作用

這個是註冊表單，會自動處理：

- username
- email
- password1
- password2
- 密碼一致檢查
- 建立 User

所以不用自己另外寫密碼驗證邏輯。

---

# 二、修改 `users/views.py`

打開：

```text
users/views.py
```

貼上以下程式：

```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
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


def home(request):
    return HttpResponse("Welcome to WhereNow")
```

## 這段程式的作用

### `register_view`
負責註冊功能：

- 進入註冊頁時，顯示空白表單
- 按送出後，接收使用者輸入
- 如果資料正確，就建立帳號
- 建立成功後，跳轉到登入頁面

### `home`
建立一個最簡單的首頁，登入成功後可以跳轉到這裡。

---

# 三、建立 `users/urls.py`

在 `users` 資料夾裡新增檔案：

```text
users/urls.py
```

貼上以下程式：

```python
from django.urls import path
from .views import register_view, home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),

    path('register/', register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
]
```

## 這段程式的作用

它告訴 Django：

- `/` → 首頁
- `/register/` → 註冊頁
- `/login/` → 登入頁
- `/logout/` → 登出功能

其中登入與登出使用 Django 內建的：

- `LoginView`
- `LogoutView`

所以不用自己寫登入邏輯。

---

# 四、把 users 的網址接到主系統

打開主專案的 `urls.py`：

```text
wherenow/urls.py
```

改成：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]
```

## 為什麼要這樣做

因為 Django 預設只知道：

```text
/admin/
```

現在把 `users/urls.py` 接進主系統後，以下網址才會生效：

- `/`
- `/register/`
- `/login/`
- `/logout/`

---

# 五、建立註冊頁面

在 `templates` 裡建立資料夾：

```text
templates/users
```

然後建立檔案：

```text
templates/users/register.html
```

貼上以下程式：

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

</body>
</html>
```

---

# 六、建立登入頁面

在同一個資料夾：

```text
templates/users/
```

新增檔案：

```text
templates/users/login.html
```

貼上以下程式：

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
<a href="/register/">註冊</a>
</p>

</body>
</html>
```

---

# 七、確認 `settings.py`

打開：

```text
wherenow/settings.py
```

## 1. 確認模板設定

找到：

```python
TEMPLATES
```

確認裡面有：

```python
'DIRS': [BASE_DIR / 'templates'],
```

完整範例如下：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
    },
]
```

## 2. 加入登入與登出跳轉設定

```python
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
```

### 作用說明

| 行為 | 跳轉位置 |
|---|---|
| 登入成功 | `/` |
| 登出成功 | `/login/` |

---

# 八、測試功能

在 terminal 輸入：

```bash
python manage.py runserver
```

測試以下網址：

## 註冊頁

```text
http://127.0.0.1:8000/register/
```

## 登入頁

```text
http://127.0.0.1:8000/login/
```

## 首頁

```text
http://127.0.0.1:8000/
```

---

# 九、成功流程

如果功能正常，流程會是：

1. 使用者進入註冊頁
2. 建立新帳號
3. 跳轉到登入頁
4. 使用者登入
5. 登入成功後跳到首頁
6. 使用者可點擊登出並回到登入頁

---

# 本週成果

本週已完成使用者帳號系統的基礎功能，包括：

- 使用者註冊
- 使用者登入
- 使用者登出
- 基本首頁
- 路由設定
- 模板設定
- 註冊與登入流程測試

目前系統已具備帳號系統雛形，後續可繼續開發地點管理與回憶功能。

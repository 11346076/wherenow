# 第 3 週

## 目標
完成使用者註冊功能與基本頁面流程。

---

## 本週目前進度

- 建立 `users/forms.py`
- 建立註冊表單 `RegisterForm`
- 建立註冊 view
- 建立 `users/urls.py`
- 將 users 路由接到主系統
- 建立註冊頁面 `register.html`
- 確認 `settings.py` 的 templates 設定
- 測試 `/register/` 頁面

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

這個是 **註冊表單**，它會自動處理：

- username
- email
- password1
- password2
- 密碼一致檢查
- 建立 User

因此不需要自己另外寫密碼驗證邏輯。

---

# 二、修改 `users/views.py`

打開：

```text
users/views.py
```

貼上以下程式：

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

## 這段程式的作用

這個 view 會做以下事情：

- 進入註冊頁時，顯示空白表單
- 按送出後，接收使用者輸入
- 如果資料正確，就建立帳號
- 建立成功後，跳轉到登入頁面

---

# 三、建立 `users/urls.py`

在 `users` 資料夾裡新增檔案：

```text
users/urls.py
```

貼上以下程式：

```python
from django.urls import path
from .views import register_view

urlpatterns = [
    path('register/', register_view, name='register'),
]
```

## 這段程式的作用

這是在告訴 Django：

當使用者開啟：

```text
/register/
```

就執行：

```text
register_view
```

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

你現在把 `users/urls.py` 接進主系統後，`/register/` 才會生效。

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

# 六、確認 `settings.py`

打開：

```text
wherenow/settings.py
```

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

如果沒有，請補上。

---

# 七、測試註冊功能

在終端機輸入：

```bash
python manage.py runserver
```

然後打開：

```text
http://127.0.0.1:8000/register/
```

如果看到註冊表單頁面，表示設定成功。

---

# 本週目前成果

目前已完成使用者註冊功能的基礎結構，包括：

- 註冊表單
- 註冊 view
- 註冊路由
- 註冊頁面
- 模板設定
- 註冊頁面測試

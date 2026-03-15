# 第 4 週

## 目標
完成使用者個人資料系統，包括 Profile 自動建立、個人資料頁面、編輯個人資料與頭像上傳功能。

---

# 本週完成內容

- 建立 Profile 自動建立機制 (signals)
- 建立 `/users/profile/` 個人資料頁面
- 建立 `/users/profile/edit/` 編輯個人資料頁面
- 建立 ProfileForm
- 支援修改 nickname 與 bio
- 支援上傳 avatar 頭像
- 設定 Django Media 檔案顯示
- 完成完整 Profile 管理流程

---

# 一、Profile 自動建立 (Signals)

建立檔案：

```
users/signals.py
```

```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            nickname=instance.username
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()
```

修改：

```
users/apps.py
```

```python
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
```

並在 `settings.py` 註冊：

```python
'users.apps.UsersConfig',
```

---

# 二、建立 ProfileForm

修改：

```
users/forms.py
```

新增：

```python
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'bio']
```

---

# 三、建立個人資料頁面

新增 view：

```
users/views.py
```

```python
@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'nickname': request.user.username}
    )

    return render(request, 'users/profile.html', {
        'profile': profile
    })
```

新增路由：

```
users/urls.py
```

```python
path('profile/', profile_view, name='profile'),
```

---

# 四、建立編輯個人資料頁面

新增 view：

```
users/views.py
```

```python
@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'nickname': request.user.username}
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, "users/edit_profile.html", {
        "form": form
    })
```

新增路由：

```python
path('profile/edit/', edit_profile, name='edit_profile'),
```

---

# 五、建立模板

## profile.html

```
templates/users/profile.html
```

顯示：

- username
- nickname
- bio
- avatar

並提供：

```
編輯個人資料
```

連結。

---

## edit_profile.html

```
templates/users/edit_profile.html
```

提供表單修改：

- nickname
- avatar
- bio

---

# 六、設定 Django Media

修改：

```
settings.py
```

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

修改：

```
wherenow/urls.py
```

```python
from django.conf import settings
from django.conf.urls.static import static
```

加入：

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

# 七、測試流程

測試以下流程：

1. 註冊新帳號
2. signals 自動建立 Profile
3. 登入系統
4. 進入 `/users/profile/`
5. 編輯 `/users/profile/edit/`
6. 修改 nickname
7. 上傳 avatar
8. 返回 profile 確認資料與圖片顯示正常

---

# 本週成果

本週已完成完整的使用者個人資料管理系統，包括：

- Profile 自動建立
- 個人資料頁面
- 編輯個人資料
- Avatar 上傳
- Django Media 設定

系統現在已具備完整的使用者帳號與個人資料管理功能，為後續情侶關係與地點管理功能提供基礎。

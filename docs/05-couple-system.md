# Couple System（情侶關係系統）

## 開發時間
2026/03/15

---

# 系統目標

建立情侶邀請與情侶關係管理功能，讓兩個使用者可以透過邀請建立情侶關係。

主要功能包括：

- 發送情侶邀請
- 查看收到的邀請
- 接受邀請
- 拒絕邀請
- 建立情侶關係

---

# 資料模型

## CoupleInvitation

用途：紀錄情侶邀請

```python
class CoupleInvitation(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invitations"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_invitations"
    )

    status = models.CharField(max_length=20, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
```

### 欄位說明

| 欄位 | 用途 |
|-----|-----|
| sender | 邀請發送者 |
| receiver | 邀請接收者 |
| status | 邀請狀態 (pending / accepted / rejected) |
| created_at | 建立時間 |

---

## CoupleRelationship

用途：紀錄情侶關係

```python
class CoupleRelationship(models.Model):

    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="relationship_user1"
    )

    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="relationship_user2"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
```

### 欄位說明

| 欄位 | 用途 |
|-----|-----|
| user_1 | 情侶使用者一 |
| user_2 | 情侶使用者二 |
| is_active | 是否為有效關係 |
| created_at | 建立時間 |

---

# 功能一：發送情侶邀請

登入使用者可以輸入另一個使用者的 username 發送邀請。

### URL

```
/couples/send/
```

### 功能流程

1. 使用者輸入對方帳號
2. 系統檢查是否存在該使用者
3. 檢查是否已有 pending 邀請
4. 建立 CoupleInvitation

### 表單

```python
class CoupleInvitationForm(forms.Form):
    receiver_username = forms.CharField(max_length=150)
```

---

# 功能二：查看收到的邀請

使用者可以查看收到的情侶邀請。

### URL

```
/couples/invitations/
```

頁面顯示：

```
xxx 邀請你成為情侶
[接受] [拒絕]
```

---

# 功能三：接受邀請

當使用者點擊接受時：

1. 將邀請 status 改為 `accepted`
2. 建立 CoupleRelationship

### URL

```
/couples/accept/<invitation_id>/
```

### View 邏輯

```python
@login_required
def accept_invitation(request, invitation_id):

    invitation = get_object_or_404(
        CoupleInvitation,
        id=invitation_id,
        receiver=request.user,
        status='pending'
    )

    invitation.status = 'accepted'
    invitation.save()

    relationship_exists = CoupleRelationship.objects.filter(
        user_1=invitation.sender,
        user_2=request.user
    ).exists() or CoupleRelationship.objects.filter(
        user_1=request.user,
        user_2=invitation.sender
    ).exists()

    if not relationship_exists:
        CoupleRelationship.objects.create(
            user_1=invitation.sender,
            user_2=request.user,
            is_active=True
        )

    return redirect('received_invitations')
```

---

# 功能四：拒絕邀請

當使用者拒絕邀請：

1. 將 status 改為 `rejected`
2. 不建立情侶關係

### URL

```
/couples/reject/<invitation_id>/
```

### View 邏輯

```python
@login_required
def reject_invitation(request, invitation_id):

    invitation = get_object_or_404(
        CoupleInvitation,
        id=invitation_id,
        receiver=request.user,
        status='pending'
    )

    invitation.status = 'rejected'
    invitation.save()

    return redirect('received_invitations')
```

---

# 系統流程

```
User A
   │
   │ send invitation
   ▼
CoupleInvitation (pending)
   │
   ├── 接受 → CoupleRelationship 建立
   │
   └── 拒絕 → status = rejected
```

---

# Admin 後台確認

在 Django Admin 中可以查看：

```
Couple Invitations
Couple Relationships
```

範例資料：

```
linmei -> linxin (accepted)
text1 -> text2 (rejected)

linmei ❤️ linxin
```

---

# 本模組成果

本模組完成以下功能：

- 情侶邀請系統
- 邀請接受與拒絕
- 情侶關係建立
- Django Admin 管理

情侶系統完成後，系統開始支援 **兩個使用者之間的共享關係**，為後續回憶共享功能奠定基礎。

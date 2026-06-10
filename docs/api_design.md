# WhereNow URL 與 REST API 規劃

本文件說明 WhereNow 的 Web UI URL、Django views 對照，以及 RESTful API resources 規劃。系統同時提供一般網頁操作與 DRF API，外部系統可透過 JWT token 存取 API。

## 1. Web UI urlpatterns 與 views 對照表

| URL | View | 功能 |
|---|---|---|
| `/` | `root_redirect` | 依登入狀態導向首頁或登入頁。 |
| `/home/` | `home` | 顯示登入後首頁與地點分類。 |
| `/explore/` | `explore_page` | 搜尋公開、個人與情侶共享的地點/回憶。 |
| `/dashboard/` | `dashboard` | 顯示統計儀表板。 |
| `/admin/` | Django Admin | 後台資料管理。 |
| `/accounts/login/` | `custom_login_view` | 自訂登入頁，包含 CAPTCHA。 |
| `/accounts/` | allauth urls | 第三方登入與帳號流程。 |
| `/i18n/` | Django i18n urls | 語言切換。 |
| `/swagger/` | drf-yasg Swagger UI | API 文件介面。 |
| `/redoc/` | drf-yasg ReDoc | API 文件介面。 |

### Users

| URL | View | 功能 |
|---|---|---|
| `/users/register/` | `register` | 使用者註冊。 |
| `/users/profile/` | `profile` | 個人資料頁。 |
| `/users/profile/edit/` | `edit_profile` | 編輯個人資料。 |

### Places

| URL | View | 功能 |
|---|---|---|
| `/places/` | `place_list` | 我的地點列表。 |
| `/places/shared/` | `shared_place_list` | 情侶共享地點列表。 |
| `/places/create/` | `place_create` | 新增地點。 |
| `/places/<pk>/` | `place_detail` | 地點詳情。 |
| `/places/<pk>/edit/` | `place_update` | 編輯地點。 |
| `/places/<pk>/delete/` | `place_delete` | 刪除地點。 |
| `/places/favorites/` | `favorite_list` | 收藏地點列表。 |
| `/places/favorite/add/<place_id>/` | `add_favorite` | 加入收藏。 |
| `/places/favorite/remove/<place_id>/` | `remove_favorite` | 移除收藏。 |
| `/places/random-pick/` | `random_pick` | 隨機推薦地點。 |
| `/places/random-pick-history/` | `random_pick_history` | 隨機推薦紀錄。 |

### Memories

| URL | View | 功能 |
|---|---|---|
| `/memories/` | `memory_list` | 我的回憶列表。 |
| `/memories/shared/` | `shared_memory_list` | 情侶共享回憶列表。 |
| `/memories/create/` | `memory_create` | 新增回憶。 |
| `/memories/<pk>/` | `memory_detail` | 回憶詳情。 |
| `/memories/<pk>/edit/` | `memory_edit` | 編輯回憶。 |
| `/memories/<pk>/delete/` | `memory_delete` | 刪除回憶。 |
| `/memories/photo/<pk>/delete/` | `memory_photo_delete` | 刪除回憶照片。 |
| `/memories/public-search/` | `public_memory_search` | 公開回憶搜尋。 |

### Couples

| URL | View | 功能 |
|---|---|---|
| `/couples/send/` | `send_invitation` | 送出情侶邀請。 |
| `/couples/invitations/` | `received_invitations` | 查看收到的邀請。 |
| `/couples/accept/<invitation_id>/` | `accept_invitation` | 接受邀請。 |
| `/couples/reject/<invitation_id>/` | `reject_invitation` | 拒絕邀請。 |
| `/couples/status/` | `couple_status` | 查看情侶關係狀態。 |
| `/couples/break/` | `break_up` | 解除情侶關係。 |
| `/couples/home/` | `couple_home` | 情侶首頁。 |
| `/couples/anniversary/edit/` | `edit_anniversary` | 編輯紀念日。 |

## 2. RESTful API Resources 規劃

API 路徑集中於 `/api/`，採用資源導向設計。列表端點支援 `GET` 查詢與 `POST` 建立；詳情端點支援 `GET`、`PUT`、`PATCH`、`DELETE`。

| Resource | List/Create Endpoint | Detail Endpoint | 說明 |
|---|---|---|---|
| Categories | `/api/categories/` | `/api/categories/<id>/` | 地點分類。 |
| Tags | `/api/tags/` | `/api/tags/<id>/` | 地點標籤。 |
| Places | `/api/places/` | `/api/places/<id>/` | 地點資料。 |
| Favorites | `/api/favorites/` | `/api/favorites/<id>/` | 收藏地點。 |
| Random Picks | `/api/random-picks/` | `/api/random-picks/<id>/` | 隨機推薦紀錄。 |
| Memories | `/api/memories/` | `/api/memories/<id>/` | 回憶資料。 |
| Memory Photos | `/api/memory-photos/` | `/api/memory-photos/<id>/` | 回憶照片。 |
| Couple Invitations | `/api/couple-invitations/` | `/api/couple-invitations/<id>/` | 情侶邀請。 |
| Couple Relationships | `/api/couple-relationships/` | `/api/couple-relationships/<id>/` | 情侶關係。 |
| Profiles | `/api/profiles/` | `/api/profiles/<id>/` | 使用者 Profile 與角色資料。 |

## 3. JWT 認證端點

| URL | Method | 功能 |
|---|---|---|
| `/api/token/` | `POST` | 使用帳號密碼取得 access token 與 refresh token。 |
| `/api/token/refresh/` | `POST` | 使用 refresh token 換發新的 access token。 |

JWT 使用方式：

```http
Authorization: Bearer <access_token>
```

## 4. REST 設計原則

1. URL 使用名詞代表資源，例如 `/api/places/`。
2. HTTP Method 代表動作，例如 `GET` 查詢、`POST` 新增、`PATCH` 部分更新、`DELETE` 刪除。
3. Web UI 與 API 分離：一般使用者操作走 `/places/`、`/memories/` 等頁面；外部整合走 `/api/`。
4. API 文件提供 Swagger 與 ReDoc，方便外部呼叫者查看欄位與測試請求。

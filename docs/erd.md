# ER Diagram

本系統共設計 **12 個主要資料表**，用來支援使用者帳號管理、情侶關係、地點清單管理、回憶紀錄與抽選功能。

---

# 資料表列表

系統資料表如下：

1. USER（使用者帳號）
2. PROFILE（使用者個人資料）
3. COUPLE_INVITATION（情侶邀請）
4. COUPLE_RELATIONSHIP（情侶關係）
5. CATEGORY（地點分類）
6. TAG（標籤）
7. PLACE（地點）
8. PLACE_TAG（地點標籤關聯）
9. MEMORY（回憶紀錄）
10. MEMORY_PHOTO（回憶照片）
11. FAVORITE_PLACE（收藏地點）
12. RANDOM_PICK_HISTORY（抽選紀錄）

---

# ERD 圖

![WhereNow ERD](./images/erd.png)

---

# 資料表說明

## 1. USER（使用者帳號）

此資料表儲存系統使用者的基本帳號資訊。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 使用者編號 |
| username | string | 使用者帳號名稱 |
| email | string | 電子郵件 |
| password | string | 登入密碼 |
| date_joined | datetime | 註冊時間 |

---

## 2. PROFILE（使用者個人資料）

此資料表用來儲存使用者的個人資料。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 資料編號 |
| user_id | int (FK) | 對應 USER |
| nickname | string | 暱稱 |
| avatar | string | 頭像圖片 |
| bio | string | 個人介紹 |

---

## 3. COUPLE_INVITATION（情侶邀請）

此資料表記錄使用者之間的情侶邀請。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 邀請編號 |
| sender_id | int (FK) | 邀請發送者 |
| receiver_id | int (FK) | 邀請接收者 |
| status | string | 邀請狀態 |
| created_at | datetime | 建立時間 |

---

## 4. COUPLE_RELATIONSHIP（情侶關係）

當邀請被接受後，會建立正式情侶關係。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 關係編號 |
| user1_id | int (FK) | 使用者1 |
| user2_id | int (FK) | 使用者2 |
| is_active | boolean | 是否有效 |
| created_at | datetime | 建立時間 |

---

## 5. CATEGORY（地點分類）

儲存地點的分類資訊。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 分類編號 |
| name | string | 分類名稱 |

---

## 6. TAG（標籤）

儲存地點標籤。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 標籤編號 |
| name | string | 標籤名稱 |

---

## 7. PLACE（地點）

系統的核心資料表，用來儲存使用者的「想去地點」。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 地點編號 |
| user_id | int (FK) | 建立者 |
| category_id | int (FK) | 分類 |
| name | string | 地點名稱 |
| region | string | 地區 |
| google_map_link | string | Google Map 連結 |
| note | string | 備註 |
| budget | string | 預算 |
| is_public | boolean | 是否公開 |
| visited | boolean | 是否去過 |
| created_at | datetime | 建立時間 |

---

## 8. PLACE_TAG（地點標籤）

此表為 **PLACE 與 TAG 的多對多關係表**。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 資料編號 |
| place_id | int (FK) | 地點 |
| tag_id | int (FK) | 標籤 |

---

## 9. MEMORY（回憶紀錄）

儲存使用者去過某個地點後的回憶紀錄。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 回憶編號 |
| user_id | int (FK) | 使用者 |
| place_id | int (FK) | 地點 |
| visit_date | date | 造訪日期 |
| comment | text | 心得 |
| rating | int | 評分 |
| cost | int | 花費 |
| recommended | boolean | 是否推薦 |
| created_at | datetime | 建立時間 |

---

## 10. MEMORY_PHOTO（回憶照片）

儲存回憶紀錄中的照片。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 照片編號 |
| memory_id | int (FK) | 回憶紀錄 |
| image | string | 照片檔案 |
| uploaded_at | datetime | 上傳時間 |

---

## 11. FAVORITE_PLACE（收藏地點）

使用者可以收藏其他人的公開地點。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 收藏編號 |
| user_id | int (FK) | 使用者 |
| place_id | int (FK) | 地點 |
| created_at | datetime | 收藏時間 |

---

## 12. RANDOM_PICK_HISTORY（抽選紀錄）

紀錄每次抽選地點的結果。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 紀錄編號 |
| user_id | int (FK) | 使用者 |
| place_id | int (FK) | 抽到的地點 |
| mode | string | 抽選模式 |
| created_at | datetime | 抽選時間 |

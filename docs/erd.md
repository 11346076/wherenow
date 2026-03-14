# ER Diagram（實體關係圖）

本系統設計一組資料庫結構，用來支援 **WhereNow－地點清單與情侶回憶管理系統** 的核心功能。

系統主要包含以下模組：

- 使用者帳號系統
- 情侶關係系統
- 地點清單管理系統
- 回憶紀錄系統
- 擴充功能（收藏與抽選紀錄）

---

# ERD 圖

![WhereNow ERD](./ERD.png)

---

# 系統資料表分類

本系統共設計 **12 個主要資料表**。

## 一、使用者帳號系統

### USER（使用者帳號）

儲存使用者的基本帳號資訊。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 使用者編號 |
| username | string | 使用者帳號 |
| email | string | 電子郵件 |
| password | string | 登入密碼 |
| date_joined | datetime | 註冊時間 |

---

### PROFILE（使用者個人資料）

儲存使用者的個人資料。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 資料編號 |
| user_id | int (FK) | 對應 USER |
| nickname | string | 暱稱 |
| avatar | string | 頭像 |
| bio | string | 個人介紹 |

---

## 二、情侶關係系統

### COUPLE_INVITATION（情侶邀請）

記錄使用者之間的情侶邀請。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 邀請編號 |
| sender_id | int (FK) | 邀請發送者 |
| receiver_id | int (FK) | 邀請接收者 |
| status | string | 邀請狀態 |
| created_at | datetime | 建立時間 |

---

### COUPLE_RELATIONSHIP（情侶關係）

當邀請被接受後，建立正式情侶關係。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 關係編號 |
| user1_id | int (FK) | 使用者1 |
| user2_id | int (FK) | 使用者2 |
| is_active | boolean | 是否有效 |
| created_at | datetime | 建立時間 |

---

## 三、地點清單管理系統

### CATEGORY（地點分類）

儲存地點分類資訊。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 分類編號 |
| name | string | 分類名稱 |

---

### TAG（標籤）

儲存地點標籤。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 標籤編號 |
| name | string | 標籤名稱 |

---

### PLACE（地點）

系統核心資料表，用來儲存使用者建立的地點清單。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 地點編號 |
| user_id | int (FK) | 建立者 |
| category_id | int (FK) | 地點分類 |
| name | string | 地點名稱 |
| region | string | 地區 |
| google_map_link | string | Google Map 連結 |
| note | string | 備註 |
| budget | string | 預算 |
| is_public | boolean | 是否公開 |
| visited | boolean | 是否已去過 |
| created_at | datetime | 建立時間 |

---

### PLACE_TAG（地點標籤關聯）

此表為 **PLACE 與 TAG 的多對多關聯表**。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 資料編號 |
| place_id | int (FK) | 地點 |
| tag_id | int (FK) | 標籤 |

---

## 四、回憶紀錄系統

### MEMORY（回憶紀錄）

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

### MEMORY_PHOTO（回憶照片）

儲存回憶紀錄中的照片。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 照片編號 |
| memory_id | int (FK) | 回憶紀錄 |
| image | string | 照片檔案 |
| uploaded_at | datetime | 上傳時間 |

---

## 五、系統擴充功能

### FAVORITE_PLACE（收藏地點）

使用者可以收藏其他人的公開地點。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 收藏編號 |
| user_id | int (FK) | 使用者 |
| place_id | int (FK) | 地點 |
| created_at | datetime | 收藏時間 |

---

### RANDOM_PICK_HISTORY（抽選紀錄）

記錄每次隨機抽選地點的結果。

| 欄位名稱 | 型態 | 說明 |
|---|---|---|
| id | int (PK) | 紀錄編號 |
| user_id | int (FK) | 使用者 |
| place_id | int (FK) | 抽到的地點 |
| mode | string | 抽選模式 |
| created_at | datetime | 抽選時間 |

---

# 資料表關聯關係

系統主要關係如下：

- USER 與 PROFILE 為 **一對一關係**
- USER 與 PLACE 為 **一對多關係**
- PLACE 與 CATEGORY 為 **多對一關係**
- PLACE 與 TAG 為 **多對多關係（透過 PLACE_TAG）**
- PLACE 與 MEMORY 為 **一對多關係**
- MEMORY 與 MEMORY_PHOTO 為 **一對多關係**
- USER 與 COUPLE_INVITATION 為 **一對多關係**
- USER 與 COUPLE_RELATIONSHIP 為 **一對多關係**

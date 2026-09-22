
## 5 Endpoint

### 1. Lấy danh sách repo của một user
- **Endpoint:** `GET /users/{username}/repos`
- **Headers:**
  - Request: `Accept: application/vnd.github+json`
  - Response: `ETag`, `Link` (phân trang prev/next), `X-RateLimit-Remaining`
- **Status code:** `200 OK` (thành công), `404 Not Found` (sai username)
- **RESTful:** Chuẩn. Dùng danh từ số nhiều, phân cấp quan hệ `users` -> `repos`, dùng đúng method `GET` thuần túy để đọc dữ liệu.

### 2. Tạo mới một issue
- **Endpoint:** `POST /repos/{owner}/{repo}/issues`
- **Headers:**
  - Request: `Authorization: Bearer <token>`, `Content-Type: application/json`
  - Response: `Location: https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}`
- **Status code:** `201 Created` (tạo thành công), `400 Bad Request` (thiếu title), `401 Unauthorized` (chưa có token)
- **RESTful:** Rất chuẩn. Dùng đúng `POST` để tạo mới, trả về `201` kèm header `Location` trỏ thẳng tới issue vừa được tạo.

### 3. Sửa thông tin profile của user hiện tại
- **Endpoint:** `PATCH /user`
- **Headers:**
  - Request: `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Status code:** `200 OK` (cập nhật thành công), `422 Unprocessable Entity` (dữ liệu gửi lên sai định dạng)
- **RESTful:** Chuẩn. Phân biệt rõ ràng với `PUT`, dùng đúng `PATCH` để partial update (chỉ sửa các field gửi lên, không bắt gửi lại toàn bộ profile).

### 4. Gắn sao (Star) một repository
- **Endpoint:** `PUT /user/starred/{owner}/{repo}`
- **Headers:**
  - Request: `Authorization: Bearer <token>`, `Content-Length: 0`
- **Status code:** `204 No Content` (thành công, không có body trả về), `401 Unauthorized`
- **RESTful:** Rất chuẩn Idempotent. Coi hành động star như việc set trạng thái cho một liên kết, gọi 1 lần hay nhiều lần kết quả vẫn y như nhau. Trả về đúng `204` vì không cần gửi payload về cho client.

### 5. Hủy theo dõi (Unfollow) một user
- **Endpoint:** `DELETE /user/following/{username}`
- **Headers:**
  - Request: `Authorization: Bearer <token>`
- **Status code:** `204 No Content` (xóa liên kết thành công), `404 Not Found` (không tồn tại user này)
- **RESTful:** Chuẩn. Dùng đúng method `DELETE` để gỡ bỏ quan hệ following và trả mã `204` khi hoàn tất tác vụ.
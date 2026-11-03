# Security Audit — Social Network API

**Phạm vi:** `POST /auth/login`, `POST /auth/refresh`, `GET /posts/{id}`  
**Tài liệu tham chiếu:** `openapi.yaml`  
**Trạng thái:** *Danh sách rủi ro cần rà soát; chưa phải kết quả pentest hoặc khẳng định mã nguồn đang có lỗ hổng.*

## 1. Scope và chính sách truy cập

| Endpoint | Xác thực cần có | Scope cần có | Kiểm tra thêm |
|---|---|---|---|
| `POST /auth/login` | Không yêu cầu đăng nhập | Không có | Chống brute-force, kiểm tra thông tin đăng nhập |
| `POST /auth/refresh` | Cookie `refresh_token` hợp lệ | Không yêu cầu access-token scope | Chống CSRF, kiểm tra phiên, refresh-token rotation |
| `GET /posts/{id}` | JWT access token | `posts:read` | Xác minh bài viết public, thuộc về người gọi, hoặc được chia sẻ |

> **Lưu ý:** Authentication (AuthN) xác minh người dùng là ai, còn Authorization (AuthZ) xác định họ có được phép thực hiện hành động trên đối tượng hay không. Chỉ kiểm tra có JWT hoặc có scope vẫn chưa đủ để cho phép xem bài private.

## 2. Các điểm có thể bị lộ / tấn công

| # | Điểm rủi ro | Tác động nếu triển khai sai | Biện pháp cần làm |
|---|---|---|---|
| 1 | **Brute-force tại `/auth/login`** | Kẻ tấn công thử nhiều mật khẩu để chiếm tài khoản. | Rate limit theo IP và tài khoản; cảnh báo, khóa tạm có giới hạn, theo dõi đăng nhập thất bại. |
| 2 | **User enumeration từ thông báo đăng nhập** | Phân biệt được email nào đã đăng ký. | Trả `401 INVALID_CREDENTIALS` chung cho email sai và mật khẩu sai; tránh khác biệt lớn về thời gian phản hồi. |
| 3 | **Lưu mật khẩu thô, mã hóa đảo ngược hoặc hash yếu** | Lộ DB dẫn đến lộ mật khẩu hàng loạt. | Dùng Argon2id (hoặc phương án được duy trì phù hợp), salt riêng ngẫu nhiên và cost thích hợp; kiểm tra việc nâng tham số / rehash. |
| 4 | **JWT bị giả mạo / xác minh thiếu chặt chẽ** | Chấp nhận token giả, token của hệ thống khác hoặc thuật toán `none`. | Chỉ cho phép thuật toán ký đã chỉ định (ví dụ RS256); xác minh signature, `iss`, `aud`, `exp`, `nbf` và key tin cậy; không tin `alg` do client tự chọn. |
| 5 | **Access token sống quá lâu hoặc bị lộ** | Token bị đánh cắp có thể bị sử dụng trong thời gian dài. | `exp` ngắn (ví dụ 15 phút), HTTPS; không ghi token vào URL/log; hạn chế lưu token trong `localStorage` nếu có nguy cơ XSS. |
| 6 | **Refresh token không rotation hoặc bị dùng lại (replay)** | Refresh token cũ bị đánh cắp có thể xin access token liên tục. | Refresh token ngẫu nhiên, lưu hash phía server, rotation mỗi lần dùng; phát hiện reuse và thu hồi cả phiên liên quan. |
| 7 | **Cookie refresh token bị đánh cắp / CSRF** | Kẻ tấn công lợi dụng cookie tự gửi đến `/auth/refresh` hoặc đọc token qua JavaScript nếu cấu hình sai. | Cookie `HttpOnly; Secure; SameSite=Strict; Path=/auth/refresh`; kiểm tra `Origin` và cấu hình CORS giới hạn origin tin cậy; triển khai CSRF token khi mô hình client yêu cầu. |
| 8 | **BOLA/IDOR trên `GET /posts/{id}`** | Người dùng có `posts:read` thay ID để xem bài private của người khác. | Kiểm tra quyền trên **từng bài viết** (owner, public, share list), không chỉ kiểm tra scope; trả 404 với bài bị ẩn. |
| 9 | **Thiếu kiểm tra scope/role** | JWT hợp lệ nhưng không có `posts:read` vẫn đọc được bài. | Middleware xác minh JWT, sau đó chặn bằng `403 INSUFFICIENT_SCOPE` khi thiếu scope; kiểm thử riêng AuthN và AuthZ. |
| 10 | **Rò rỉ thông tin qua lỗi và log** | Stack trace, email, password, JWT, refresh cookie hoặc chi tiết DB bị lộ. | Lỗi trả về dạng chung; log có request ID, che/mask credential; không log `Authorization`, `Cookie` và body đăng nhập. |
| 11 | **XSS khi hiển thị nội dung bài viết** | Nội dung bài chứa script có thể chạy trên trình duyệt, lấy dữ liệu phiên/đánh cắp access token. | Escape output, sanitize nội dung HTML nếu cho phép rich text, dùng CSP phù hợp. |
| 12 | **SQL injection / truy vấn không ràng buộc dữ liệu** | Kẻ tấn công thao túng DB hoặc lấy thông tin ngoài quyền. | Validate UUID, truy vấn parameterized/ORM, không nối chuỗi SQL, giới hạn quyền DB. |

## 3. HTTP status code dự kiến

| Endpoint | Thành công | Lỗi có thể xảy ra |
|---|---|---|
| `POST /auth/login` | `200 OK` | `400` JSON hoặc email không hợp lệ; `401` sai thông tin đăng nhập; `429` quá nhiều lần thử; `500` lỗi máy chủ |
| `POST /auth/refresh` | `200 OK` | `401` thiếu / hết hạn / thu hồi / tái sử dụng refresh token; `403` Origin bị từ chối; `429` quá nhiều yêu cầu; `500` lỗi máy chủ |
| `GET /posts/{id}` | `200 OK` | `400` ID sai định dạng; `401` JWT thiếu / hỏng / hết hạn; `403` thiếu `posts:read`; `404` bài không tồn tại hoặc người gọi không được xem; `429` quá nhiều yêu cầu; `500` lỗi máy chủ |

**Quy ước phân biệt:** `401` = chưa xác thực hợp lệ; `403` = đã xác thực nhưng thiếu quyền hoặc yêu cầu bị chặn bởi chính sách; `404` = không tìm thấy hoặc cố ý che sự tồn tại của bài viết private.

## 4. Kết luận

Ba endpoint có ba lớp trách nhiệm khác nhau: `/auth/login` xác minh danh tính; `/auth/refresh` bảo vệ vòng đời phiên đăng nhập; `/posts/{id}` kiểm tra **cả scope hành động lẫn quyền trên đối tượng**. Đặc tả OpenAPI mô tả hợp đồng API; mã nguồn backend vẫn phải thực thi các chính sách này và cần được kiểm thử trước khi kết luận an toàn.

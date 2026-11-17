# Lab 4 — Phân tích kết quả

Nguồn: báo cáo [A](../reports/A.html), [B](../reports/B.html), [C](../reports/C.html) ngày 17/11/2026.

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30s | 18 | 0,00% (0/143) | 4,84 |
| B | 50 | 5 | 60s | 18 | 0,21% (3/1397) | 23,48 |
| C | 200 | 50 | 30s | 67 | 0,17% (5/2913) | 98,15 |

p95 và RPS lấy từ dòng `Aggregated`; failure rate = failures / requests × 100%.
Duration là thời gian cấu hình; báo cáo thực tế ghi nhận 29/59/29 giây.

1. **Kịch bản có p95 cao nhất:** C đạt 67 ms, gấp 3,72 lần A/B (18 ms).
   Khi tăng lên 200 users, RPS đạt 98,15 và độ trễ tăng; chưa đủ dữ liệu xác định nút thắt.

2. **Endpoint gây failure:** Chỉ `GET /books?year`, với 3 lỗi ở B và 5 lỗi ở C.
   Đây là `response.failure()` giả lập xác suất 1% sau HTTP 200, không phải HTTP 500 từ server.
   `GET /books/{id}` chấp nhận 404 nên không tính vào failure.

3. **SLO p95 < 300 ms:** Cả A, B, C đều đạt trong lần đo này.
   Thời gian chạy ngắn, chưa tách warm-up; Flask development server và SQLite trên máy cá nhân
   không đại diện cho hiệu năng production.

4. **Kiểm chứng pool giới hạn 5:** So sánh `pool_size=5, max_overflow=0` với pool lớn hơn,
   giữ nguyên dữ liệu và mức tải, chạy lặp lại. Đo p95, RPS, thời gian chờ connection
   và timeout thực, tách lỗi giả lập. Nếu pool lớn hơn giảm thời gian chờ và p95,
   kết quả hỗ trợ giả thuyết pool là nút thắt; hiện chưa có phép đo đối chứng này.

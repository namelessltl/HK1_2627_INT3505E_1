1. chạy lệnh `curl.exe "http://localhost:5000/api/v1/books?sort=price"` để sắp xếp sách theo giá tăng dần.<br>
kết quả: sách "Mat Biec" có giá 110000 đứng trước sách "Clean Code - Ma Sach" có giá 350000.
![](<gia tang.png>)

1. chạy lệnh `curl.exe "http://localhost:5000/api/v1/books?sort=-price"` để sắp xếp sách theo giá giảm dần.<br>
kết quả: sách "Clean Code - Ma Sach" có giá 350000 đứng trước sách "Mat Biec" có giá 110000.
![](<gia giam.png>)

1. chạy lệnh `curl.exe "http://localhost:5000/api/v1/books?sort=-id"` để sắp xếp sách theo ID giảm dần.<br>
kết quả: sách có ID bằng 2 đứng trước sách có ID bằng 1.
![](<id giam.png>)

1. chạy lệnh `curl.exe "http://localhost:5000/api/v1/books?category_id=1"` để lọc sách theo danh mục có ID bằng 1.<br>
kết quả: trả về sách "Mat Biec" thuộc danh mục "van-hoc", với `has_more: false` và `next_cursor: null`.
![](<loc theo cat.png>)

1. kết hợp lọc danh mục và sắp xếp, ví dụ chạy lệnh `curl.exe "http://localhost:5000/api/v1/books?category_id=1&sort=-price"`.<br>
kết quả: trả về sách "Mat Biec" thuộc danh mục có ID bằng 1. Ảnh chỉ hiển thị phần kết quả, không hiển thị đầy đủ lệnh đã chạy; danh mục này chỉ có một sách nên chưa thể hiện rõ thứ tự sắp xếp.
![](<filter va sort.png>)

1. chạy lệnh `curl.exe "http://localhost:5000/api/v1/books?sort=-price&limit=2"` để lấy tối đa 2 sách mỗi trang, sắp xếp theo giá giảm dần.<br>
kết quả: trả về 2 sách theo thứ tự giá 350000 rồi 110000. Với dữ liệu hiện tại chỉ có 2 sách, `next_cursor` bằng `null`, không có trang tiếp theo.
![](<cursor pagination.png>)



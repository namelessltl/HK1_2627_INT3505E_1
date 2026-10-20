1. chạy lệnh `curl -i -X GET http://127.0.0.1:5000/api/v1/books` để lấy danh sách sách.<br>
kết quả: trả về danh sách sách với mã trạng thái `200 OK`.
![](<get_books.png>)

1. chạy lệnh `curl -i -X GET http://127.0.0.1:5000/api/v1/books/1` để lấy thông tin sách có ID bằng 1.<br>
kết quả: trả về thông tin sách "Mat Biec".
![](<get_book.png>)

1. chạy lệnh `curl -i -X GET http://127.0.0.1:5000/api/v1/books/9999` để lấy thông tin sách không tồn tại.<br>
kết quả: trả về mã trạng thái `404 NOT FOUND`.
![](<get_book_404.png>)

1. chạy lệnh sau trong Git Bash để thêm sách mới:<br>

```bash
curl -i -X POST http://127.0.0.1:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Lap Trinh Python Co Ban",
    "isbn": "978-604-2-99999-1",
    "price_vnd": 150000,
    "stock": 45,
    "category_id": 2
  }'
```

kết quả: tạo sách thành công, trả về thông tin sách có ID bằng 3 với mã trạng thái `201 CREATED`.
![](<Post_201.png>)

1. chạy lại lệnh POST ở trên với cùng ISBN `978-604-2-99999-1`.<br>
kết quả: trả về mã trạng thái `409 CONFLICT` và thông báo "ISBN đã tồn tại hoặc khóa ngoại không hợp lệ".
![](<Post_409.png>)

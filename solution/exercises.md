# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**
>0.0 : "Một sự thật thú vị về Việt Nam là quốc gia này sở hữu Hang Sơn Đoòng, hang động tự nhiên lớn nhất thế giới. Nằm tại Vườn quốc gia Phong Nha - Kẻ Bàng, tỉnh Quảng Bình, hang động này lớn đến mức có dòng sông ngầm, hệ sinh thái rừng và kiểu khí hậu riêng biệt ở bên trong."
>0.5 : "Bạn có biết Việt Nam không chỉ nổi tiếng về cà phê mà còn là quốc gia xuất khẩu hạt điều và hạt tiêu đen lớn nhất thế giới không? Dù hạt điều có nguồn gốc từ Nam Mỹ, nhưng nhờ khí hậu nhiệt đới và kỹ thuật canh tác, Việt Nam hiện đang chiếm lĩnh hoàn toàn thị trường toàn cầu về loại hạt gia vị này."
>1.0 : "Hãy nói về 'đặc sản' giao thông đi! Ở Việt Nam, chiếc xe máy không chỉ là phương tiện di chuyển, nó là một 'chiếc xe tải đa năng thu nhỏ'. Bạn có thể bắt gặp một người lái xe máy chở theo một cái tủ lạnh khổng lồ, một gia đình 4 người, hay thậm chí là chở hàng trăm quả bóng bay sặc sỡ lướt đi trên phố. Nghệ thuật giữ thăng bằng của người Việt trên xe máy thực sự là một siêu năng lực!"
>1.5 : "Ồ, tuyệt cú mèo luôn! Hình chữ S uốn lượn đó là nơi mà cà phê trứng không chỉ để uống mà nó bay bổng như một đám mây béo ngậy trên bầu trời Hà Nội rực rỡ! Ngôn ngữ của họ ư? Sáu thanh điệu nhảy múa như một bản giao hưởng hip-hop, nơi con ma và bà má chơi trốn tìm trong cùng một nốt nhạc! Có người bảo dưới đáy Vịnh Hạ Long có rồng giấu châu báu cơ đấy, ai mà biết được, thật điên rồ và kỳ diệu!"
**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature tăng dần từ 0.0 đến 1.5, phản hồi chuyển từ tính xác định, rập khuôn sang tính sáng tạo và ngẫu nhiên. Ở mức 0.0, câu trả lời luôn nhất quán và tập trung vào các sự thật phổ biến nhất (như lượng xe máy hoặc xuất khẩu cà phê). Từ mức 1.0 trở lên, mô hình bắt đầu sử dụng từ ngữ lạ lẫm hơn, sinh ra các thông tin ngẫu nhiên, và tại mức 1.5, văn phong có thể bị lộn xộn hoặc xuất hiện hiện tượng ảo tưởng thông tin (hallucination).

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ đặt temperature ở mức thấp, từ 0.0 đến 0.2. Đối với chatbot hỗ trợ khách hàng, sự chính xác, nhất quán và đáng tin cậy của thông tin là yếu tố quan trọng nhất; việc đặt giá trị thấp giúp kiểm soát chặt chẽ câu trả lời của mô hình dựa trên tài liệu hỗ trợ, tránh việc AI tự "sáng tạo" ra các chính sách hoặc thông tin sai lệch gây ảnh hưởng đến uy tín doanh nghiệp.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Dựa trên bảng giá thông thường (GPT-4o giá $0.010/1K output tokens và GPT-4o-mini giá $0.0006/1K output tokens), GPT-4o đắt hơn GPT-4o-mini khoảng 16.67 lần. Cụ thể với tổng khối lượng 10.500.000 tokens mỗi ngày, chi phí ước tính cho GPT-4o là $105.00, trong khi GPT-4o-mini chỉ tiêu tốn khoảng $6.30.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> Trường hợp GPT-4o xứng đáng: Các tác vụ yêu cầu khả năng lập luận logic phức tạp, phân tích cấu trúc mã nguồn sâu, giải quyết bài toán toán học chuyên sâu, hoặc xử lý các văn bản pháp lý, tài chính đa tầng ngữ nghĩa mà mô hình nhỏ không đảm bảo được độ chính xác.

>Trường hợp GPT-4o-mini tốt hơn: Các tác vụ lặp đi lặp lại với khối lượng dữ liệu lớn (high-volume, low-complexity) như phân loại sắc thái bình luận (sentiment analysis), trích xuất thực thể (NER), tóm tắt nhanh văn bản ngắn, hoặc các cuộc hội thoại chào hỏi, điều hướng cơ bản.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming đóng vai trò quan trọng nhất trong các ứng dụng tương tác trực tiếp với người dùng cuối theo thời gian thực (như Chatbot, Trợ lý ảo), nơi "độ trễ cảm nhận" (perceived latency) quyết định trải nghiệm người dùng; việc hiển thị văn bản ngay khi vừa được tạo ra giúp giảm bớt cảm giác sốt ruột khi phải chờ đợi phản hồi dài. Ngược lại, chế độ non-streaming lại phù hợp hơn cho các tác vụ xử lý ngầm (batch processing), trích xuất dữ liệu có cấu trúc định dạng sẵn (như JSON) cần được parse hoàn chỉnh bởi hệ thống backend trước khi thực hiện các logic tiếp theo, hoặc khi cần kiểm duyệt toàn bộ nội dung đầu ra trước khi hiển thị công khai.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 

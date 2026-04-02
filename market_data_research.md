# Market Data Research

## Mục tiêu
- So sánh nguồn dữ liệu giả lập (GBM) với dữ liệu thực tế (Polygon.io, AlphaVantage, Yahoo). 
- Đăng tải các tần suất/chiến lược, ưu nhược.

## Nội dung
1. Dữ liệu GBM (hiện tại)
   - Ưu: nhanh, không cần API key, dễ điều chỉnh
   - Nhược: không có thông tin lịch sử, thiếu khối lượng và spread
2. Dữ liệu thực tế
   - Polygon.io, API kết nối `MASSIVE_API_KEY`
   - Có giá bid/ask, volume, news

## Kế hoạch
- Tạo `scripts/fetch_market_data.py` lấy symbol AAPL/TSLA và plot
- So sánh hiệu suất chiến lược momentum/mean-reversion với dữ liệu thật

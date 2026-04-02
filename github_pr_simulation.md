# GitHub PR Simulation for AI Agent

## Mục tiêu
- Cho AI viết tài liệu/PR tự động từ codebase hiện tại.
- Bổ sung script kiểm tra (AI-review) repo.

## Kịch bản
1. AI scan diff, nhận diện thay đổi trade/chat.
2. Sinh PR body + checklist:
   - [x] `api/chat` parse command
   - [x] `api/trades` buy/sell
   - [x] `frontend/ChatInterface` cập nhật
3. Tạo nhãn `automation`.

## Demo
- Với GitHub Action `anthropics/claude-code-action` đã cấu hình, mỗi PR sẽ có review comment tự động.

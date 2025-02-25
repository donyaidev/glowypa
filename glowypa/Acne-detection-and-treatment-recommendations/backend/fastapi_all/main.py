from fastapi import FastAPI
from routes.userRoute import user
from routes.recommendRoute import recommend
from routes.feedbackRoute import feedback
from routes.architectureRoute import architecture
from routes.acneDetectionRoute import acneDetection
from routes.storageRoutineRoute import storage_routine

from routes.chatboxRoute import chatbox
from fastapi.middleware.cors import CORSMiddleware

# Khởi tạo ứng dụng FastAPI
app = FastAPI()


# Cấu hình CORS chi tiết
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origins - trong production nên chỉ định cụ thể
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả methods (GET, POST, etc.)
    allow_headers=["*"],  # Cho phép tất cả headers
)


# Thêm middleware để xử lý cookie
@app.middleware("http")
async def add_cookie_header(request, call_next):
    response = await call_next(request)
    # Thêm các header liên quan đến cookie
    response.headers["Access-Control-Allow-Credentials"] = "true"
    # Nếu bạn cần set cookie
    # response.set_cookie(
    #     key="session",
    #     value="value",
    #     httponly=True,
    #     secure=True,
    #     samesite="none",
    #     max_age=1800  # 30 phút
    # )
    return response

# Bao gồm các router
app.include_router(user)
app.include_router(feedback)
app.include_router(architecture)
app.include_router(acneDetection)
app.include_router(chatbox)
app.include_router(recommend)
app.include_router(storage_routine)
# Tùy chọn: Thêm route test để kiểm tra CORS
@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS is working"}

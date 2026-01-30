from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from repositories.request_repo import InMemoryRequestRepository
from services.request_service import RequestService

from routers import guide_router, request_router, stt_router, companion_router
from routers import booking_router
from routers import memo_router
from routers import memo_list_router
from routers import map_router
from routers import guardian_note_router
from routers import guardian_note_list_router
from routers import booking_checklist_router

app = FastAPI(
    title="Backend API Server",
    description="API server for handling backend requests",
    version="1.0.0"
)

# 라우터 여기에 추가
# app.include_router(xxx_router.router)
app.include_router(request_router.router)
app.include_router(booking_router.router)
app.include_router(memo_router.router)
app.include_router(memo_list_router.router)
app.include_router(stt_router.router)
app.include_router(guide_router.router)
app.include_router(guardian_note_router.router)
app.include_router(guardian_note_list_router.router)
app.include_router(companion_router.router)
app.include_router(map_router.router)
app.include_router(booking_checklist_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 요청 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/")
def main():
    return "Hello World!"

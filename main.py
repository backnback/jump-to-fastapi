from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

def create_app() -> FastAPI:

    app = FastAPI(
        title="My FastAPI App",
        description="FastAPI 학습용 앱",
        version="1.0.0"
    )

    # CORS 미들웨어 설정 (개발환경용)
    origins = [
        "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {"message": "Hello FastAPI!"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    app.include_router(question_router.router)
    app.include_router(answer_router.router)
    app.include_router(user_router.router)


    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
from fastapi import FastAPI, Request
from jose import JWTError, jwt
from starlette.middleware.cors import CORSMiddleware
from log import logger
from .controllers.user import SECRET_KEY, ALGORITHM
from .database import SessionLocal
from .models.user import Log
from .views import user as user_view
from .views import entity as entity_view
from .views import achievement as achievement_view
from .views import count as count_view

app = FastAPI(
    title="SOMS-fastapi",
    description="",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 中间件定义
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    token = request.headers.get("Authorization")
    db = SessionLocal()
    user_id = None

    if token:
        try:
            payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("id")
        except:
            pass

    # 提取请求信息
    request_type = request.method
    request_path = request.url.path
    source_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    try:
        # 记录到数据库
        log_entry = Log(
            user_id=user_id,
            request_type=request_type,
            request_path=request_path,
            source_ip=source_ip,
            user_agent=user_agent
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.error(f"请求日志记录失败: {e}")
        db.rollback()
        return response
    finally:
        db.close()
    return response


app.include_router(user_view.router)
app.include_router(entity_view.router)
app.include_router(achievement_view.router)
app.include_router(count_view.router)

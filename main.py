from fastapi import FastAPI, Depends
from pydantic import BaseSettings
from dotenv import load_dotenv

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk import set_user

load_dotenv()


# environment 환경 변수 추가
class Settings(BaseSettings):
    environment: str
    sentry_dsn: str


app = FastAPI()
settings = Settings()


# 센트리 environment 설정
sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.environment, traces_sample_rate=1)
app.add_middleware(SentryAsgiMiddleware)


@app.get("/health")
def health_check():
    return {
        "environment": settings.environment,
        "sentry_dsn": settings.sentry_dsn
    }


# 센트리 user 설정
def set_sentry_user(sid: str):
    set_user({"id": sid})


# 1. Exception 발생 자동 보고
@app.get("/crash/{sid}", dependencies=[Depends(set_sentry_user)])
def make_error(sid: str):
    raise Exception(f"some error to sentry, {sid}")


# 2. 직접 에러 리포팅
@app.get("/report/{sid}", dependencies=[Depends(set_sentry_user)])
def make_error2(sid: str):
    try:
        division_by_zero = 1 / 0
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)

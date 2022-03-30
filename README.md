Sentry 연동 테스트
---

#### 센트리 개념

* 센트리는 크래시 리포팅 툴이다. Exception 이 발생하면 센트리로 리포팅된다

#### 센트리 연동 절차

* 프로젝트 생성 후 DSN 키 확인
* 코드에서 SDK 초기화 `sentry_sdk.init(dsn="")`
* 알림 설정 (slack notification)

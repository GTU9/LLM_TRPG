# Python 3.11 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 의존성 먼저 복사 및 설치 (캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 로그 저장 디렉토리 생성
RUN mkdir -p /app/data

# Streamlit 설정
RUN mkdir -p /root/.streamlit
COPY .streamlit/config.toml /root/.streamlit/config.toml

# 포트 노출
EXPOSE 8501

# 헬스체크
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 실행
CMD ["streamlit", "run", "trpg_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# 사용될 베이스 이미지
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일을 작업 디렉토리로 복사
COPY requirements.txt requirements.txt

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["python", "app.py"]

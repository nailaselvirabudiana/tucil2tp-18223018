FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 17787
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "17787"]

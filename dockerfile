FROM python:3.12.3

# Install netcat-openbsd for checking DB connection
RUN apt-get update && apt-get install -y netcat-openbsd

# Your other Dockerfile instructions...

# Установим зависимости
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Скопируем код проекта
COPY . .

# Установка Daphne (ASGI server)
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]

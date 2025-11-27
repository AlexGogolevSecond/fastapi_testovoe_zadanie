FROM python:3.12-slim

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Копируем приложение
COPY . /app

# SQLite файл будет в рабочей директории
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости и устанавливаем (requirements.txt находится в корне репозитория)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь репозиторий в рабочую директорию (в результате будет /app/app/...)
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

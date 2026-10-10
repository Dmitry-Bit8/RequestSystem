
echo "=== Деплой RequestSystem ==="

# 1. Собираем образ
echo "Сборка Docker-образа..."
docker build -t request-system .

# 2. Запускаем контейнер
echo "Запуск контейнера..."
docker-compose down
docker-compose up -d

# 3. Проверяем здоровье
echo "Проверка доступности..."
sleep 5
curl -f http://localhost:8000/health || echo "Ошибка: сервис не отвечает"

echo "=== Деплой завершён ==="

#!/bin/sh
# Скрипт для проверки доступности портов

# Функция для проверки доступности порта
wait_for_port() {
  local host="$1"
  local port="$2"
  local timeout=60

  echo "Проверка доступности порта $port..."

  # Цикл ожидания доступности порта
  while ! nc -z "$host" "$port" >/dev/null 2>&1; do
    timeout=$((timeout - 1))
    if [ "$timeout" -eq 0 ]; then
      echo "Тайм-аут. Порт $port не доступен."
      exit 1
    fi
    sleep 1
  done

  echo "Порт $port доступен."
}

# Ожидание доступности портов
wait_for_port my-elast 9200
wait_for_port postgres 5432

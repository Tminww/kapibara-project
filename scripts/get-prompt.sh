#!/bin/bash

# Путь к корню проекта (текущая директория по умолчанию)
PROJECT_ROOT=$(pwd)/frontend

# Выходной файл
OUTPUT_FILE="frontend_archive.txt"

# Очистка выходного файла перед началом
> "$OUTPUT_FILE"

# Проверяем, является ли текущая директория Git-репозиторием
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Ошибка: Текущая директория не является Git-репозиторием."
    exit 1
fi

echo "Начинаем сборку проекта..."

# Нахождение всех файлов, исключая те, которые указаны в .gitignore
find "$PROJECT_ROOT" -type f | while read -r file; do
    # Проверяем, игнорируется ли файл по правилам .gitignore
    if git check-ignore -q "$file"; then
        echo "Игнорируется: $file"
        continue
    fi

    # Проверяем расширение файла
    ext="${file##*.}"
    if [[ "$ext" != "js" && "$ext" != "ts" && "$ext" != "vue" && "$ext" != "py" && "$ext" != "json" ]]; then
        echo "Пропускается (не подходит по расширению): $file"
        continue
    fi

    # Выводим информацию о том, что файл обрабатывается
    relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$file")
    echo "Обработка файла: $relative_path"

    # Добавляем разделитель с именем файла
    echo "########### $relative_path ###########" >> "$OUTPUT_FILE"
    
    # Добавляем содержимое файла
    if [[ -f "$file" && -r "$file" ]]; then
        cat "$file" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"  # Пустая строка между файлами
    else
        echo "Ошибка чтения файла: $file" >&2
    fi

    # Добавляем пустую строку для разделения файлов
    echo "" >> "$OUTPUT_FILE"
done

echo "Проект собран в файл: $OUTPUT_FILE"
# Block Auditor

**Block Auditor** — инструмент для аудита содержимого блока в сети Bitcoin.

## Что делает

- Анализирует все транзакции в блоке
- Выявляет OP_RETURN
- Показывает транзакции с подозрительно высокими комиссиями
- Считает общее количество транзакций и общую комиссию

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python block_auditor.py <block_height>
```

Пример:

```bash
python block_auditor.py 808000
```

## Применение

- Blockchain forensic
- Анализ аномалий в блоках
- Обнаружение спама и нестандартных скриптов

## Лицензия

MIT License

# AILearn3009
AILearn3009

222

## Задание «ИГРА 9»: загрузка INBOX

Скрипт `fetch_inbox.py` использует стандартную библиотеку Python 3.10+.
Он подключается к IMAP, открывает INBOX в режиме чтения и сохраняет полные
письма (включая вложения) как `.eml`, а заголовки и текст — в `messages.json`.
Флаги прочтения не изменяются. Для каждого сообщения используется IMAP UID.

Запуск в PowerShell:

```powershell
$env:IMAP_HOST = '51.250.109.172'
$env:IMAP_PORT = '3143'
$env:IMAP_USER = 'api@example.com'
$env:IMAP_PASSWORD = '<пароль из задания>'
$env:IMAP_TLS = '0'
python fetch_inbox.py
```

Учебный сервер использует соединение без TLS на порту 3143.
По умолчанию скрипт использует IMAP over TLS и порт 993.
Путь сохранения можно изменить: `python fetch_inbox.py --output inbox/run2`.
Каталог `inbox/`, файлы `.env` и кеш Python исключены из Git.

Результаты фактической загрузки и сводка по письмам: [RESULTS.md](RESULTS.md).

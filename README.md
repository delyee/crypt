## Crypt *(old)*

### Pic:

![](./static/README.png)

---

## Info:

Пароль и открытый текст никогда не хранится в БД, encrypt/decrypt полностью на client-side за счет CryptoJS (AES-256). Иными словами, даже администратор сервиса не может получить доступ к Вашему открытому тексту. 
В случае, если Вы или кто-то другой, введет неправильный пароль с включенной функцией “Delete after reading”, то заметка так же будет удалена.

Пожалуйста, соблюдайте следующие требования к паролю, если не используете автоматическую генерацию - `[a-Z0-9]{32}`. Надеюсь, что Вам поможет данный [snippet](https://medium.com/@delyee/easy-password-gen-in-console-61455ef0abd5).

### Функции: 

- Удаление заметки после прочтения
- Генерация пароля за пользователя (опционально), устойчивого к прямому перебору
- Генерация “quick link” - позволяет получить ссылку, включающую в себя UUID+%password% для удобства пользователя: Вы можете передать её по незащищенным каналам связи, если получатель по умолчанию сразу прочитает записку после публикации (обязательно с включенной опцией "удалить после прочтения" и генерацией пароля)





---



## todo:


0. ~~beta-версия~~
1. ~~Рефакторинг~~
2. ~~Оптимизация~~
3. ~~Найти другую либу~~ для шифрования на стороне клиента, так как текущая очень слабая в плане криптостойкости
4. ~~Закончить реализацию~~ исходной идеи - шифрование/расшифровка полностью на стороне клиента (даже открытый текст на сервер не отправляется), без надобности хранения пароля в БД *(see example: `db.json`)*. Ваши заметки не сможет прочитать даже владелец сервиса.
5. Продолжить идею логгирования (logging warnings - bad UUIDs, malcode in client query)
5. Добавить хранение файлов (картинки, архивы, документы)
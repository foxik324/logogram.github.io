# K.E.R.N.E.L — карта проекта Logogram

> Обновлено: 2026-09-17 22:45
> Стек: Electron + Node.js, JSON-файлы без БД, vanilla JS + CSS без сборки

## 1. Где что лежит

КЛИЕНТ (Electron): ...\workspace\Logogram project\Logogram-client\
- main.js       — Electron main (окно, IPC check-server/notify)
- preload.js    — contextBridge, отдаёт window.kernelDesktop
- renderer.js   — вся логика клиента (~2600 строк)
- index.html    — вся разметка + ВСЕ стили в одном inline <style>
- style.css     — старый файл, в HTML НЕ подключён

СЕРВЕР: ...\workspace\Logogram project\Logogram\
- server.js     — Express, все роуты, rate-limit
- users.json    — пользователи
- messages.json — сообщения
- groups.json   — группы/каналы

ЗАПУСК:
- Сервер:  cd Logogram && npm start  (порт 3000)
- Клиент:  cd Logogram-client && node_modules\.bin\electron.cmd .

## 2. Реализовано

Аутентификация: token в localStorage[logogramToken], currentUser, profile PATCH.

Список чатов и папки:
- Вкладки-папки над списком (#folderTabs), кнопка + открывает менеджер
- Папки в localStorage[logogramFolders] = [{name, members[]}]
- applyFolder(name) фильтрует, Drag&drop чата на вкладку, ПКМ по вкладке = delete
- FAB ✎ внизу = создать чат/группу/канал
- Онлайн-индикатор: lastSeen < 60 сек → зелёная точка
- Время последнего сообщения, pin/mute, бейдж непрочитанных
- Поиск #search → searchChats()

Чат:
- Оптимистичный рендер (tmp_id)
- Галочки: ⏱ отправка, ✓ sent, ✓✓ серые = delivered, ✓✓ голубые = read
- Reply: replyTo на сервере, span.bubble-quote с кликом-прокруткой
- Forward: forwardedFrom на сервере, модалка #forwardModal, метка Forwarded from @user
- Реакции: localStorage[logogramReactions] = {msgId:{emoji:[users]}}; двойной клик = thumbs-up; ПКМ → React = пикер
- Шапка: online/lastSeen (ЛС) или members (группа); клик → инфо

Панель ввода: Enter отправляет, Shift+Enter новая строка, reply-bar над полем.

Профиль (модалка через drawer → My profile):
- Мульти-аватарки: Emoji / Photo·Video / Initials, фон из AVATAR_BACKGROUNDS
- История аватарок: карусель + localStorage[logogramAvatarHistory]
- Эмодзи-статус: localStorage[logogramStatusEmoji], рендер в drawer + чужом профиле
- Accent/Theme/Stars/Premium/Gifts/NFT
- Danger zone → Log out

Чужой профиль (ПКМ по чату → Profile): аватар, имя+emoji, @user, bio.

Статусы подключения: setConnStatus, pingServer 10 сек, «Ожидание сети / Соединение / Обновление».

Уведомления: window.kernelDesktop.notify → ipcMain logogram:notify → Notification.

Горячие клавиши: Ctrl+K поиск, Esc (по приоритету), ↑ reply на последнее.

Контекстные меню:
- Сообщение: Reply, Forward, React, Copy, Delete for me, Delete for all, Report, Ban
- Чат: Open, Profile/Info, Add contact, Pin, Mute, Mark read, Clear history, Delete, Ban

## 3. API сервера

GET /api/status, POST /api/register, POST /api/login, POST /api/logout, GET /api/me
GET /api/users?me=, PATCH /api/profile, GET /api/profile/:username
GET/POST /api/groups, PATCH /api/groups/:id, POST /api/groups/:id/members|leave
GET/POST /api/messages, POST /api/messages/read, POST /api/messages/delivered
GET /api/shop/catalog, GET /api/shop/inventory, POST /api/shop/buy|premium|gift

Middleware: authRequired (Bearer token, обновляет lastSeen раз в 30 сек), rateLimit (10/мин/IP).

publicUser: id, username, email, displayName, bio, avatar, avatarBg, accent, theme, lastSeen, stars, premium, premiumSince, gifts.

## 4. localStorage ключи

logogramToken, logogramUser, logogramFolders, logogramPin, logogramMute,
logogramContacts, logogramBanned, logogramDeletedMsgs, logogramReports,
logogramReactions, logogramStatusEmoji, logogramPeerStatuses,
logogramAvatarHistory, logogramTheme, logogramAccent, logogramLang

## 5. Ключевые функции renderer.js

apiFetch, retryConnect, openMessenger, loadUsers, loadGroups, refreshAll,
renderChats, renderFolderTabs, applyFolder, openChat, buildRow,
renderMessages, appendNewMessages, sendMessage, messageContextMenu,
chatContextMenu, openForwardModal, doForward, setReplyTo, cancelReply,
toggleReaction, setConnStatus, pingServer, poll, maybeShowNotification,
openProfileModal, saveProfile, openUserProfile, openFoldersModal,
createFolderFromInput, openDrawer, closeDrawer, showCtxMenu, showToast

## 6. Сделано за сессию 2026-09-17

1. Восстановили layout (убрали style.css link)
2. Вкладки-папки над списком + FAB
3. Убрали карандаш из верхней панели
4. Убрали нижнюю панель профиля (вход через drawer)
5. Логаут в модалку Profile (Danger zone)
6. Эмодзи-статусы (пикер + drawer + чужой профиль)
7. Статусы подключения в шапке + ping
8. Онлайн-индикатор собеседников
9. Мульти-аватарки (галерея + конструктор + видео + фон)
10. Галочки сообщений (sent→delivered→read)
11. Drag&drop чатов в папки
12. Реакции
13. Системные уведомления
14. Reply с цитатами
15. Горячие клавиши
16. Forward (ЛС + группы + каналы)
17. Убрали scope-tabs из drawer

## 7. Бэклог (планируем)

- Экспорт чата в .txt/.json
- Автопереключение темы по времени суток
- Галерея медиа в чужом профиле
- Голосовые сообщения (MediaRecorder)
- Редактирование своих сообщений (edit)
- Реальное удаление у обоих (DELETE /api/messages/:id)
- Lightbox для медиа
- Закреплённые сообщения в шапке
- Опросы
- Групповые звонки
- Оффлайн-режим (кэш)
- Глобальный поиск по сообщениям

## 8. Особенности работы

Кодировка:
- В cmd русский текст отображается кракозябрами (CP866/1251) — не ошибка.
- Python: io.open(path, encoding="utf-8"). print() русских букв падает — только ASCII.

Правки:
- Многострочные вставки через %WRITE ... %ENDWRITE.
- После JS: node --check renderer.js. После сервера: node --check server.js.
- \uXXXX в Python-строках попадает в HTML как ЛИТЕРАЛ — писать реальные символы.

Якоря для CSS-правок: .folder-tabs {  .reactions-bar {  .bubble-quote {

## 9. Полезные команды

node --check renderer.js
node --check server.js

Мягкий рестарт сервера:
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter ""Name='node.exe'"" | Where-Object { $_.CommandLine -like '*server.js*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"

Мягкий рестарт клиента:
powershell -NoProfile -Command "Get-Process electron -ErrorAction SilentlyContinue | Stop-Process -Force"

Все роуты сервера:
findstr /n "app.get app.post app.patch app.delete" server.js

Статус API:
powershell -NoProfile -Command "(Invoke-WebRequest -Uri 'http://localhost:3000/api/status' -UseBasicParsing).Content"

---

Разработчик клиента: CloudCat. Версия: 1.0.0.
Verified users: cloudcat, systemx, vp2.

Спокойной ночи! Завтра скажи «продолжаем» или «прочитай карту проекта».

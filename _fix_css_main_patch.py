# -*- coding: utf-8 -*-
import io, re

def fix(path, repl):
    s = io.open(path, encoding='utf-8').read()
    for a, b in repl:
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8').write(s)
    left = re.findall(r'[а-яА-ЯёЁ]+', s)
    print(path, '-> remaining russian chunks:', len(left), left[:10])

# style.css
fix('style.css', [
    ('/* ===== ключи по схеме tdesktop, значения — наши (из ТЗ) ===== */',
     '/* ===== tdesktop-style tokens; values are ours (from spec) ===== */'),
    ('/* bg-active (акцент) */', '/* bg-active (accent) */'),
    ('/* accent-blue (ссылки) */', '/* accent-blue (links) */'),
    ('/* исходящие пузыри */', '/* outgoing bubbles */'),
    ('/* алиасы для совместимости с существующим CSS */',
     '/* aliases for compatibility with the existing CSS */'),
    ('/* кривые анимаций как у tdesktop */', '/* easing curves like tdesktop */'),
    ('/* ====== ripple-эффект (как windowBgRipple в tdesktop) ====== */',
     '/* ====== ripple effect (like windowBgRipple in tdesktop) ====== */'),
    ('/* ====== skeleton-загрузка (как skeleton_animation) ====== */',
     '/* ====== skeleton loading (like skeleton_animation) ====== */'),
    ('/* ====== shake при ошибке (как shake_animation) ====== */',
     '/* ====== shake on error (like shake_animation) ====== */'),
    ('/* ====== отправка сообщения (как send_action_animations) ====== */',
     '/* ====== message sending (like send_action_animations) ====== */'),
    ('/* ====== typing-индикатор (три точки) ====== */',
     '/* ====== typing indicator (three dots) ====== */'),
    ('/* ====== контекстное меню (как menuBg/menuBgOver в tdesktop) ====== */',
     '/* ====== context menu (like menuBg/menuBgOver in tdesktop) ====== */'),
    ('/* ====== toast-уведомление (как toast.tgs) ====== */',
     '/* ====== toast notification (like toast.tgs) ====== */'),
])

# main.js
fix('main.js', [
    ('Клиент запускается ОТДЕЛЬНО от сервера.', 'The client runs SEPARATELY from the server.'),
    ('Сервер поднимается вручную:  cd ..\\Logogram && npm start',
     'Start the server manually:  cd ..\\Logogram && npm start'),
    ('/* ---------- проверка сервера ---------- */', '/* ---------- server check ---------- */'),
    ('/* ---------- окно ---------- */', '/* ---------- window ---------- */'),
])

# patch2.js
fix('patch2.js', [
    ('// 2. apiFetch: вставить Authorization после объявления opts',
     '// 2. apiFetch: insert Authorization after opts declaration'),
    ('// 3. login: после currentUser = r.data.user; вставить setToken(r.data.token)',
     '// 3. login: after currentUser = r.data.user; insert setToken(r.data.token)'),
    ('// 5. logout: убрать user -> добавить setToken("")',
     '// 5. logout: remove user -> add setToken("")'),
    ('console.log("заменено: " + n);', 'console.log("patched: " + n);'),
])
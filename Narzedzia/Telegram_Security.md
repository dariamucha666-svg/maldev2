---
tags: [xmask, security, telegram, opsec]
date: 2026-08-15
status: active
---

# Telegram — bot i kanał, twarde ustawienia

Powiązane: [[Telegram_Obsidian_Bot]] · [[Warsztat/README]]

## Bot (@Xmaskapp_bot)

- Tylko allowlista (`ALLOWED_USER_IDS` + `.owner_id`). Pusta lista = bot nie wstaje.
- Obcy `/start` — cisza, bez „bot prywatny”.
- Komendy i przycisk Dashboard tylko u właściciela. Domyślnie pusta lista komend.
- Wrzucony do grupy — wychodzi sam.
- `/start` nie pokazuje ścieżek na serwerze.
- Nowe posty na kanał: `protect_content` (trudniej zapisać / puścić dalej).
- `.env` i `.owner_id` mode 600. Unit: NoNewPrivileges, PrivateTmp, ProtectSystem.

BotFather (kliknij sam): *Allow Groups? → Turn groups off*.

## Kanał XMaskPoland

- Admini: Ty (creator) + bot (post/edit/delete, bez dodawania adminów).
- Extra invite link unieważniony. Wejście przez publiczny `t.me/XMaskPoland`.
- Brak grupy komentarzy (linked chat).
- Nie dodawaj trzeciego admina „bo kolega pomoże”.

W Telegramie na kanale:
1. Komentarze / grupa dyskusyjna — wyłączone.
2. *Restrict saving content* — włącz, jak jest w ustawieniach.
3. Twoje konto TG: 2FA.

## Świadomie otwarte

Publiczny dashboard labu (osobny serwis). To nie jest bot. Jak chcesz — zamykamy osobno.

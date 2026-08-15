---
tags: [xmask, channel, electron, stage1]
channel: true
updated: 2026-08-14
---

⚠️ XMask | Alert — fałszywy instalator „Runtime Components”

Co to za wirus?
To NIE jest aktualizacja Windowsa, EA ani Exodusa. To instalator Electron, który udaje pasek postępu („Runtime Components 3.2.1”, rzekomo ~187 MB, 1247 plików).

Po „zainstalowaniu” próbuje ściągnąć drugi plik (payload.exe) — backdoora Go opisanego w osobnym poście.

W kodzie jest miejsce na wysyłkę zrzutów ekranu i IP na Telegram, ale w tej konkretnej kopii token był pusty. Kolejna wersja może już mieć żywego bota.

Jak się bronić?
• Oficjalne programy nie aktualizują się przez losowy setup z przeglądarki o nazwie „Runtime Components”.
• Jeśli to odpaliłeś: odinstaluj tę aplikację z „Dodaj/usuń programy”, sprawdź folder %LOCALAPPDATA% i autostart (Menedżer zadań → Uruchamianie).
• Zmień hasła z CZYSTEGO komputera / telefonu.
• Nie wklejaj seedów portfela ani haseł, dopóki nie masz pewności że stage-2 nie wstał.

Połączony alert: Backdoor Go (easports.gg) — ten sam łańcuch.

#XMask #phishing #Electron #socialengineering

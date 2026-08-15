---
tags: [xmask, laik, recap]
channel: false
updated: 2026-08-15
---

Przypominajka: Zirex / Digikala_Job

To była ta „folia bąbelkowa” na Androidzie. Apka udaje ogłoszenie o pracę w Digikali.

Co zrobiliśmy: otworzyliśmy kod startowy i bibliotekę native. Okazało się, że najpierw ładuje się cienka skorupa, a właściwy program siedzi w pliku analytics.db (udaje bazę SQLite). Skorupa go odszyfrowuje w pamięci.

nativeComposeUrl — funkcja, która ma złożyć adres serwera — jest tylko w bibliotece .so, nie w Javie. W stringach nie ma http. Jest za to lista uprawnień (SMS, telefon, zdjęcia) i token zt9Te.

Czego nie zrobiliśmy: nie odszyfrowaliśmy drugiego etapu na VPS.

Notatka z detalami: Zirex_nativeComposeUrl.

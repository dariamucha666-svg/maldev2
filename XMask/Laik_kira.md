---
tags: [xmask, laik, recap]
channel: false
updated: 2026-08-15
---

Przypominajka: Kira

Wzięliśmy apkę `com.kira.malware`, bo wyglądała na RAT (zdalne sterowanie telefonem).

Co wyszło: to nie wirus z kampanii. To zestaw szkoleniowy z GitHuba (Ivan Sincek, „malware-apk”). Na ekranie wprost pisze „Malware APK”.

Po co to było: zobaczyłeś na żywym przykładzie, jak wyglądają sztuczki RAT-a — nakładka na inne okna, czytanie tekstu z ekranu, podgląd powiadomień. Tyle że tu jest do tego menu. W prawdziwym wirusie nie ma menu.

Czego nie ma: ukrytego adresu serwera. To, co pipeline nazwał „WebSocket”, to zwykła biblioteka sieciowa.

Notatka z detalami: 410a5cba Android RAT kira.

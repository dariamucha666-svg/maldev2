---
tags: [xmask, laik, recap, telegram]
channel: false
updated: 2026-08-15
---

Przypominajka (prosto)

To jest notatka dla Ciebie, nie post na kanał. Żeby za tydzień nie myśleć „co my tam właściwie robiliśmy”.

## Od czego się zaczęło

Masz lab: VPS, pipeline (skrypt, który rozkłada podejrzane pliki) i sejf Obsidian. Poprosiłeś, żeby iść dalej z analizą — RAT-y, stealery, backdoory, miners.

Zasada od początku: **tylko oglądamy pliki, nie odpalamy ich z internetem.**

## Co zrobiliśmy po kolei

1. **Posegregowaliśmy cały stos próbek.**  
   Nie „wszystko to wirus”, tylko etykiety: RAT, stealer, backdoor, dropper, packer. Minera (cryptojackera) w tym zestawie nie było.

2. **Wpięliśmy etykiety w pipeline.**  
   Nowy plik po analizie sam dostaje tag (rat / stealer / …). Bot i dashboard też to widzą.

3. **Kira (apka na telefon).**  
   Wyglądała jak klasyczny RAT. Po otwarciu kodu okazało się: to publiczna apka szkoleniowa (malware-apk). Pokazuje sztuczki, ale nie ma ukrytego serwera. Nie instalować na swoim telefonie.

4. **Rozszerzenie Chrome „Receita Federal”.**  
   To już nie szkoła. Udaje urząd skarbowy i kradnie dane z banków (Brazylia). Adresy serwerów są wpisane w plikach. Tego nie ruszaliśmy w sieci.

5. **Sześć plików Windows (.NET).**  
   Nie jeden stealer. Trzy to NanoCore (stary RAT). Reszta: duży „Loader”, stub udający aktualizację i mały `system32.exe` z kamerą. Adresów w czystym tekście nie było.

6. **Spakowane APK-i.**  
   Nie jeden packer. Zirex (Digikala_Job — fałszywa oferta pracy), dwa z paczką `nvcgehin`, perska strona w apce, plus zaszyfrowany plik w assets.

7. **Zirex głębiej — nativeComposeUrl.**  
   Adres, z którym apka ma gadać, składa się w bibliotece native, nie w Javie. Widać przynętę Digikala i listę uprawnień (SMS, telefon, zdjęcia). Samego adresu nie wyciągnęliśmy — trzeba by emulować kod offline. Tego nie zrobiliśmy.

8. **Bot Telegram.**  
   Umie dopisywać notatki do Obsidiana, czytać dashboard i dawać gotowce na kanał. Ten przycisk czyta właśnie tę notatkę.

## Czego świadomie nie ruszaliśmy

- Odpalania próbek.
- Łączenia się z ich serwerami.
- Odszyfrowywania drugiego etapu Zirex / nvcgehin na VPS.
- Sliver / C2 z tej sesji.

## Gdzie to leży, jak zapomnisz nazw

- Cała segregacja → notatka Klasyfikacja korpusu
- Dziennik dnia → Daily 2026-08-15
- Kira, Chrome, .NET, Zirex → karty w Analizy/Malware
- Przyciski pod spodem → krótsze kawałki tej samej historii

Jak będziesz robił kolejne RE, dopisz akapit tutaj — bot pokaże nową wersję.

---
tags: [xmask, channel, pe, golang, easports]
channel: true
sha256: 178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4
updated: 2026-08-14
---

🚨 XMask | Alert — Backdoor Go (fałszywy EA Sports)

Co to za wirus?
Windowsowy backdoor napisany w Go (wersja 1.25.4). Udaje podpisane oprogramowanie EA Sports — w certyfikacie jest domena easports.gg, to podróbka, nie oficjalny EA.

To DRUGI etap. Najpierw ofiara odpala instalator „Runtime Components” (Electron), a ten ściąga ten właśnie plik jako payload.exe.

W środku są funkcje Windowsa do:
• dodawania kont
• udziałów sieciowych
• logowania się w imieniu użytkownika

Adresów serwera C2 nie ma gołym okiem w pliku — program składa je dopiero po starcie. Nie uruchamiamy tego w labie z siecią.

Jak się bronić?
• Nie klikaj instalatorów „Runtime Components / aktualizacja kodeków / EA launcher” z maila, Discorda, fałszywej strony.
• Zablokuj hash w AV/EDR (poniżej).
• Jeśli plik już był odpalony: odłącz sieć, nie wchodź na bank/mail/krypto z tego komputera, zmień hasła z innego sprzętu, pełny skan Defender Offline.
• Certyfikat easports.gg ≠ zaufany wydawca. Windows czasem i tak pokaże „nieznany wydawca”.

IoC (możesz wrzucić do VirusTotal):
SHA256
178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4
MD5
15e0ce7b0403c42fa224bb40ef10dcfe
Nazwa z sieci
141935c46a5c4ff1b84b433e84f36e61.exe  /  payload.exe

YARA (lab): Backdoor_EASports_Go

Pewność: średnia — analiza statyczna, bez detonacji.

#XMask #malware #Windows #Go #backdoor

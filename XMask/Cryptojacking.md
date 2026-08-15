---
tags: [xmask, channel, cryptojacking]
channel: true
updated: 2026-08-14
---

⛏️ XMask | Cryptojacking — stan korpusu

Co to jest?
Cryptojacker używa TWOJEGO CPU/GPU do kopania krypto (często Monero / XMRig). Telefon się grzeje, laptop wyje, prąd skacze.

Co mamy w labie teraz?
W aktualnym pipeline (14 APK + backdoor Go + kwarantanna Windows/JS/Chrome) **nie ma potwierdzonego cryptojackera**.
Szukaliśmy: XMRig, stratum, Monero, NiceHash, Coinhive, RandomX — brak.

Wysoka entropia ≠ miner. To zwykle packer.

Jak się bronić (gdy trafi)?
• Nagły wiatrak / 100% CPU bez powodu → Menedżer zadań / Android battery.
• Rozszerzenia Chrome „kopiące w tle” — usuń.
• Serwery: nie zostawiaj Redis/Docker otwartego na świat (klasyczny wektor XMRig).

Jak znajdziemy próbkę — będzie osobny alert z hashem.

#XMask #cryptojacking

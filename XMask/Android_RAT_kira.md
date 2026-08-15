---
tags: [xmask, channel, android, rat, lab]
channel: true
updated: 2026-08-15
sha256: 410a5cbaabc1cdee003ac2fd1d6c1ca8b58c9eb75cd7c671dfa163653b5ae712
---

🐀 XMask | Analiza — „kira.malware” (lab APK, nie kampania)

Co to jest?
Hash z naszego pipeline (410a5cba…) to publiczny zestaw szkoleniowy Ivana Sinceka: malware-apk. Pakiet nazywa się wprost com.kira.malware, na ekranie jest „Malware APK”.

To nie jest cichy wirus z maila. To apka-laboratorium, która POKAZUJE prawdziwe sztuczki RAT-a:
• Accessibility — czyta tekst z okien innych aplikacji
• nakładka (overlay) — okno nad innymi apkami
• podgląd powiadomień — stąd biorą się kody 2FA
• schowek, enumeracja pakietów, HTTP z formularza

Nie ma zaszytego adresu C2. WebSocket w skanerze to biblioteka OkHttp, nie tunel do operatora.

Dlaczego to i tak ważne?
Bo dokładnie tak samo wygląda „prawdziwy” Android RAT — tylko bez przycisków i z ukrytą ikoną. Jak ktoś prosi o Accessibility + nakładki, to jest ten sam wzorzec.

Jak się bronić (prawdziwe RAT-y, nie ten lab):
• Nie instaluj APK spoza sklepu.
• Accessibility tylko dla apki, której ufasz (np. menedżer haseł, nie „wygaszacz”).
• Zabierz zgodę na „wyświetlanie nad innymi aplikacjami”.
• Podejrzenie: odinstaluj, zmień hasła banku z innego telefonu.

Ten konkretny hash: nie traktuj jako IoC kampanii. To znany projekt MIT na GitHubie.

#XMask #Android #RAT #lab

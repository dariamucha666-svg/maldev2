---
tags: [xmask, channel, android, dropper]
channel: true
updated: 2026-08-14
---

📱 XMask | Alert — Android: fałszywa aktualizacja (dropper)

Co to za wirus?
Aplikacja na telefon, która w środku ma gotowy szablon strony „upgrade-template”. Wygląda jak aktualizacja albo oficjalny sklep, a tak naprawdę to dropper: pokazuje WebView i może dociągnąć kolejny złośliwy APK albo wyłudzić uprawnienia.

W pipeline widać znacznik:
appassets.shelltemplate.internal
oraz
upgrade-template/index.html

Dwie próbki z tym samym motywem są już w dashboardzie.

Jak się bronić?
• Aplikacje tylko z Google Play (albo sklepu producenta telefonu).
• Play Protect — włączony.
• Jak prosi o „dostęp do całej zawartości”, SMS, Accessibility albo „rysowanie na innych aplikacjach” — to zwykle kradzież albo overlay na bank.
• Już zainstalowane? Ustawienia → Aplikacje → odinstaluj, potem skan Play Protect. Zmień hasło Google z innego urządzenia.

Nie wysyłaj nam APK na grupę — hash wystarczy.

#XMask #Android #dropper #overlay

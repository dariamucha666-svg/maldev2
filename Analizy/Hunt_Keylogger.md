---
title: "Hunt + OSINT — Keylogger"
date: 2026-08-15
updated: 2026-08-15
tags: [hunt, keylogger, t1056, capa, pipeline, osint]
status: active
---

# Keylogger — hunt w korpusie (detekcja)

**Keylogger** = przechwytywanie naciśnięć klawiszy albo tekstu z pól (ATT&CK [T1056.001](https://attack.mitre.org/techniques/T1056/001/)).  
Na Androidzie ten sam efekt często idzie przez **Accessibility** (`getText` / `TYPE_VIEW_TEXT_CHANGED`), nie przez klasyczny hook.

To **nie** przepis na logger. Tylko co już jest w labie i jak to oznaczać.

Powiązane: [[Hunt_Clipper]] · [[Hunt_Phishing_Stealer]] · [[DotNet_cluster]] · [[410a5cba Android RAT kira]]

---

## Werdykt labu (15.08, static)

### Potwierdzone (capa / karta)

| Hash | Rodzina | Dowód | Uwaga |
|------|---------|-------|--------|
| `7ae00fe8…6f33` | Win32.RAT.DotNetCam (`system32.exe`) | capa: **log keystrokes via polling** (2), ATT&CK T1056.001, MBC F0002.002, plus screenshot T1113 | Keylog jest **modułem RATa**, nie osobnym clipperem. Karta katalogu: kamera + polling. |
| `45b98ab0` `98df0a98` `85915561` | NanoCore RAT | rodzina standardowo ma keylog; w tych raportach **capa puste** (timeout / packed rsrc) | Traktować jako **oczekiwany plugin** NanoCore, nie jako osobny binarek. [[DotNet_cluster]] |
| `410a5cba` | kira / malware-apk | Accessibility + `getText` / focus — **kradzież tekstu z UI** | Lab toolkit, nie cichy implant. To *odpowiednik* keyloga na Androidzie. |

### Szum / nie potwierdzone

| Hash | Co widać | Werdykt |
|------|----------|---------|
| `7d8b4974…d024` | Delphi + WebView2, importy `SetWindowsHookExW`, `GetAsyncKeyState`, `GetKeyboardState`, `CallNextHookEx` | Typowe dla dużego GUI VCL (skróty, hotkeys). **Brak** stringów `keylog`/`keystroke`. Nie oznaczać jako keylogger bez dalszego RE. |

Brak samodzielnego „gołego” keyloggera (mały PE tylko z hookiem i plikiem `log.txt`).

---

## Jak łapać w pipeline

1. **capa** na PE — szukaj `collection/keylog` / T1056.001 (tak wyszedł `7ae00fe8`).
2. YARA hunt: `tools/yara-rules/custom/hunt_keylogger.yar`
   - Win: hook/poll API **oraz** string `keylog`/`keystroke` (żeby nie zabić każdego Delphi).
   - Android: AccessibilityService + BIND_ + TEXT_CHANGED/getText.
3. Rola w `classify_roles` zostaje **rat** / **stealer**, nie nowa rola `keylogger` — to zwykle *zdolność*, nie rodzina.

---

## OSINT — klasa (czytać, nie odtwarzać)

| Klasa | Typowy sygnał | Publiczne przykłady |
|-------|---------------|---------------------|
| Polling | `GetAsyncKeyState` w pętli | wiele .NET stubów, starych RATów |
| Hook | `SetWindowsHookEx(WH_KEYBOARD_LL)` | klasyczny Win32 logger |
| RAT plugin | ten sam binarek + screen + C2 | NanoCore, AsyncRAT, Remcos |
| Android a11y | serwis dostępności czyta drzewo UI | bankerzy, kira (lab) |
| Form grabber | tekst z przeglądarki, nie surowe VK | stealery bankowe |

Detekcja na hoście (Sigma/Sysmon): nowy proces ładuje `user32!SetWindowsHookEx` i pisze do `%TEMP%`/`AppData` bez okna. To hunting, nie exploit.

---

## Czego nie robię

- Nie piszę keyloggera ani PoC hooka.
- Nie odpalam `7ae00fe8` żeby „zobaczyć log”.
- Nie włączam keylog_start na żadnym agencie.

## Next

Głębszy static na `7ae00fe8` (gdzie capa znalazła polling) albo NanoCore rsrc — w karcie [[DotNet_cluster]], bez detonation.

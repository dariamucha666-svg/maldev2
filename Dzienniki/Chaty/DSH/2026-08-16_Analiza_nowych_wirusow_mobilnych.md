---
title: "Analiza nowych wirusów mobilnych"
date: 2026-08-16
tags: [chatlog, czat, dsh]
source: DSH
session: session-37058436-5f55-4be4-ba3b-481d314555ae
cwd: "/root/obsidian-vault"
messages: 348
tool_calls: 306
status: archived
---

# Analiza nowych wirusów mobilnych

> Zapis czatu **DSH** · sesja 'session-37058436-5f55-4be4-ba3b-481d314555ae' · '/root/obsidian-vault' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Wiadomości użytkownika | 0 |
| Odpowiedzi asystenta | 42 |
| Akcji narzędziowych | 306 |
| Narzędzia | 'bash'×108, 'run_code'×59, 'result'×58, 'read'×29, 'edit'×19, 'web_search'×14, 'write'×8, 'todo_write'×7, 'job_output'×4 |
| Pliki | '/etc/os-release' · '/opt/jadx' · '/opt/jadx/bin/jadx' · '/opt/retools' · '/opt/retools/bin/androguard' · '/opt/retools/bin/apkid' · '/opt/retools/bin/pip' · '/root/.mb_api_key' · '/root/malware-lab/albiriox' · '/root/malware-lab/albiriox/extracted' · '/root/malware-lab/albiriox2' · '/root/malware-lab/albiriox2/ex' · '/root/malware-lab/clayrat_videodtp' · '/root/malware-lab/clayrat_videodtp/ex' · '/root/malware-lab/clayrat_videodtp/jadx_out/sources' · '/root/malware-lab/clayrat_youtube' · '/root/mb_api_key' · '/root/obsidian-vault' · '/var/cache/apt' · '2026-08-15.md' |
| IP | '129.6.55.182' · '194.32.79.94' |
| Hosty | 'barracuda.com' · 'cleafy.com' · 'github.com' · 'githubusercontent.com' · 'polyswarm.io' · 'securelist.com' · 'thehackernews.com' |
| Hashe | '3269a0116ce0…' · '78878d33b2b4…' · '8703ee8685a4…' · 'b08e5a842cd2…' · 'bf82609c5530…' |

## Wniosek (ostatnia odpowiedź asystenta)

Dobra uwaga — sprawdzę, co mam w Cloudflare (R2/rclone) do zrzucania dużych artefaktów. A przy okazji: w ostatnim kroku odkryłem coś ważnego — **"szyfrowanie" manifestu było FAKE** (podrobiony bit w zipie, dane to zwykły deflate). Odzyskałem manifest! Rozkodowuję go i sprawdzam Cloudflare.

## Pełny zapis

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:36Z

tool: run_code
{"code": "const queries = [\n  \"mobile malware families 2025 active Android banking trojan spyware\",\n  \"Android malware families 2024 2025 threat report top\",\n  \"mobile malware sample databases MalwareBazaar VirusTotal TheZoo APK repository\",\n  \"iOS malware 2024 2025 spyware Pegasus LightSpy threat\",\n  \"mobile threat intelligence sources feeds 2025 Android malware\",\n];\n\nconst results = await Promise.all(queries.map(async (q) => {\n  const r = await tools.web_search({ query: q });\n  return { query: q, answer: r.content ?? \"\", sources: r.sources };\n}));\n\nfor (const res of 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:45Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:45Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:46Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:46Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:46Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:46Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:56Z

tool: run_code
{"code": "// Fetch database-list READMEs from GitHub raw, and search details on newest families\nconst urls = [\n  \"https://raw.githubusercontent.com/antoniovh/Android-Malware-Dataset-Sources/master/README.md\",\n  \"https://raw.githubusercontent.com/antoniovh/Android-Malware-Dataset-Sources/main/README.md\",\n  \"https://raw.githubusercontent.com/praveenjalasutram/Malware-Samples-and-Databases/master/README.md\",\n  \"https://raw.githubusercontent.com/praveenjalasutram/Malware-Samples-and-Databases/main/README.md\",\n  \"https://raw.githubusercontent.com/cybersecurity-dev/awesome-malware-dat
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:57Z

bash: curl -sL --max-time 25 "https://raw.githubusercontent.com/antoniovh/Android-Malware-Dataset-Sources/master/README.md" | head -c 12000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:57Z

bash: curl -sL --max-time 25 "https://raw.githubusercontent.com/antoniovh/Android-Malware-Dataset-Sources/main/README.md" | head -c 12000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:57Z

bash: curl -sL --max-time 25 "https://raw.githubusercontent.com/praveenjalasutram/Malware-Samples-and-Databases/master/README.md" | head -c 12000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:58Z

bash: curl -sL --max-time 25 "https://raw.githubusercontent.com/praveenjalasutram/Malware-Samples-and-Databases/main/README.md" | head -c 12000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:58Z

bash: curl -sL --max-time 25 "https://raw.githubusercontent.com/cybersecurity-dev/awesome-malware-datasets/main/README.md" | head -c 12000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:36:58Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:03Z

tool: run_code
{"code": "const queries = [\n  \"FvncBot SeedSnatcher ClayRat Android malware data theft 2025\",\n  \"Albiriox Android RAT banking crypto wallet Cleafy analysis\",\n  \"RatOn Android malware PolySwarm analysis\",\n  \"Kaspersky trojan banker smartphone 56% 2025 report Android malware families\",\n  \"MalwareBazaar Android APK malware samples tag android\",\n];\n\nconst results = await Promise.all(queries.map(async (q) => {\n  const r = await tools.web_search({ query: q });\n  return { query: q, answer: r.content ?? \"\", sources: r.sources };\n}));\n\nfor (const res of results) {\n  console.lo
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:10Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:12Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:12Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:12Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:12Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:12Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:22Z

tool: run_code
{"code": "const targets = [\n  [\"barracuda\", \"https://blog.barracuda.com/2025/12/09/malware-brief-android-fvncbot-seedsnatcher-clayrat\"],\n  [\"cleafy-albiriox\", \"https://www.cleafy.com/cleafy-labs/albiriox-rat-mobile-malware-targeting-global-finance-and-crypto-wallets\"],\n  [\"polyswarm-raton\", \"https://blog.polyswarm.io/raton-android-malware\"],\n];\n\nconst strip = (html) => html\n  .replace(/<script[\\s\\S]*?<\\/script>/gi, \" \")\n  .replace(/<style[\\s\\S]*?<\\/style>/gi, \" \")\n  .replace(/<[^>]+>/g, \" \")\n  .replace(/&nbsp;/g, \" \")\n  .replace(/&amp;/g, \"&\")\n  .replace
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:22Z

bash: curl -sL --max-time 30 -A "Mozilla/5.0 (X11; Linux x86_64)" "https://blog.barracuda.com/2025/12/09/malware-brief-android-fvncbot-seedsnatcher-clayrat" | sed -e 's/<script[^>]*>[^<]*<\/script>//g' -e 's/<style[^>]*>[^<]*<\/style>//g' -e 's/<[^>]*>/ /g' | tr -s ' \n\t' ' ' | head -c 6000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:23Z

bash: curl -sL --max-time 30 -A "Mozilla/5.0 (X11; Linux x86_64)" "https://www.cleafy.com/cleafy-labs/albiriox-rat-mobile-malware-targeting-global-finance-and-crypto-wallets" | sed -e 's/<script[^>]*>[^<]*<\/script>//g' -e 's/<style[^>]*>[^<]*<\/style>//g' -e 's/<[^>]*>/ /g' | tr -s ' \n\t' ' ' | head -c 6000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:23Z

bash: curl -sL --max-time 30 -A "Mozilla/5.0 (X11; Linux x86_64)" "https://blog.polyswarm.io/raton-android-malware" | sed -e 's/<script[^>]*>[^<]*<\/script>//g' -e 's/<style[^>]*>[^<]*<\/style>//g' -e 's/<[^>]*>/ /g' | tr -s ' \n\t' ' ' | head -c 6000

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:23Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:30Z

tool: run_code
{"code": "const r = await tools.bash({ command: \"pwd && echo '---' && ls -la && echo '--- tree (depth 2) ---' && find . -maxdepth 2 -not -path '*/.git/*' | sort | head -100\", description: \"Inspect vault directory structure\" });\nconsole.log(r.kind === \"foreground\" ? r.stdout.text : JSON.stringify(r));\nreturn \"ok\";", "description": "Inspect obsidian vault structure"}

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:30Z

bash: pwd && echo '---' && ls -la && echo '--- tree (depth 2) ---' && find . -maxdepth 2 -not -path '*/.git/*' | sort | head -100

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:30Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

tool: run_code
{"code": "const paths = [\n  \"Analizy/Threat_Intel_MOC.md\",\n  \"Analizy/README.md\",\n  \"Lab/Narzedzia_RE.md\",\n  \"Analizy/Malware\",\n  \"Analizy/Threat_Digest\",\n  \"Wiedza\",\n  \"Projekty\",\n];\n\nfor (const p of paths) {\n  const isDir = !p.endsWith(\".md\");\n  if (isDir) {\n    const r = await tools.bash({ command: `ls -la \"${p}\" 2>/dev/null`, description: \"List dir\" });\n    console.log(\"\\n===== DIR:\", p, \"=====\");\n    console.log(r.kind === \"foreground\" ? r.stdout.text : JSON.stringify(r));\n  } else {\n    const r = await tools.read({ file_path: p });\n    console
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

bash: ls -la "Analizy/Malware" 2>/dev/null

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

bash: ls -la "Analizy/Threat_Digest" 2>/dev/null

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

bash: ls -la "Wiedza" 2>/dev/null

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z

bash: ls -la "Projekty" 2>/dev/null

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:36Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

tool: run_code
{"code": "const files = [\n  \"Wiedza/Zrodla.md\",\n  \"Wiedza/README.md\",\n  \"Wiedza/_Template.md\",\n  \"Wiedza/Malware\",\n  \"Wiedza/Ataki\",\n  \"Analizy/Malware/410a5cba Android RAT kira.md\",\n  \"Analizy/Malware/Android_native_packed.md\",\n  \"Analizy/Malware/a710209e Android NFC skimmer.md\",\n  \"Analizy/Malware/README.md\",\n];\nfor (const p of files) {\n  if (!p.endsWith(\".md\")) {\n    const r = await tools.bash({ command: `ls -la \"${p}\" 2>/dev/null`, description: \"List dir\" });\n    console.log(\"\\n===== DIR:\", p, \"=====\");\n    console.log(r.kind === \"foreground\" ?
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: ls -la "Wiedza/Malware" 2>/dev/null

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: ls -la "Wiedza/Ataki" 2>/dev/null

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:46Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:52Z

tool: run_code
{"code": "for (const p of [\"Wiedza/Malware/Malware_MOC.md\", \"Wiedza/Aktualizacje.md\", \"Wiedza/Narzedzia.md\"]) {\n  const r = await tools.read({ file_path: p });\n  console.log(\"\\n===== FILE:\", p, \"=====\");\n  for (const l of r.lines) console.log(l.text);\n}\nreturn \"ok\";", "description": "Read malware MOC and updates/narzedzia notes"}

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:52Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:52Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:52Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:37:52Z



### 🤖 Asystent — 2026-08-16T01:42:51Z

I have a complete picture now. Let me capture the findings into the vault following its existing conventions (Polish, MOC wiring, frontmatter). I'll create three notes and wire them into the existing MOCs.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:51Z

tool: run_code
{"code": "await tools.todo_write({ todos: [\n  { content: \"Research current mobile malware landscape + databases\", status: \"completed\" },\n  { content: \"Write mobile malware databases analysis note\", status: \"in_progress\" },\n  { content: \"Write mobile malware families landscape note\", status: \"in_progress\" },\n  { content: \"Write Android RE + dynamic analysis roadmap\", status: \"in_progress\" },\n  { content: \"Wire up MOCs and changelog\", status: \"pending\" },\n]});\n\nasync function w(path, lines) {\n  try {\n    const r = await tools.write({ file_path: path, content: lines.
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:51Z

bash: todo_write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:51Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:51Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:51Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:51Z



### 🤖 Asystent — 2026-08-16T01:42:59Z

Three notes created. Now wiring them into the existing MOCs and changelog.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:59Z

tool: run_code
{"code": "const edits = [\n  {\n    file_path: \"Wiedza/Zrodla.md\",\n    old_string: \"Powiązane: [[Zasoby/Linki_Zewnętrzne]] · [[Narzedzia]]\",\n    new_string: \"Powiązane: [[Zasoby/Linki_Zewnętrzne]] · [[Narzedzia]] · [[Zrodla_Mobile_Malware]] (malware mobilny)\",\n  },\n  {\n    file_path: \"Wiedza/Malware/Malware_MOC.md\",\n    old_string: \"- **Android:** Cerberus, Anubis, Hydra, BRATA, Vultur (VNC), kira, avanegar, NFC skimmer.\",\n    new_string: \"- **Android:** Cerberus, Anubis, Hydra, BRATA, Vultur (VNC), kira, avanegar, NFC skimmer.\\n- **Aktywne 2024–2025 (nowe):** RatOn, Albirio
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:59Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:59Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:59Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:59Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:42:59Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:04Z

tool: run_code
{"code": "// Verify the new notes and edited links resolve cleanly\nconst check = async (p) => {\n  const r = await tools.read({ file_path: p, limit: 12 });\n  return { p, head: r.lines.map(l => l.text).join(\" | \") };\n};\nconst files = [\n  \"Wiedza/Zrodla_Mobile_Malware.md\",\n  \"Wiedza/Malware/Mobile_Malware_2024_2025.md\",\n  \"Lab/Android_RE_i_Dynamiczna_Analiza.md\",\n];\nfor (const f of files) {\n  const c = await check(f);\n  console.log(\"\\n### \" + c.p + \"\\n\" + c.head);\n}\n\n// confirm edit in Malware_MOC\nconst moc = await tools.read({ file_path: \"Wiedza/Malware/Malware_MOC
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:04Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:04Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:04Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:04Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:04Z

bash: todo_write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:04Z



### 🤖 Asystent — 2026-08-16T01:43:21Z

Gotowe. Przeanalizowałem bazy malware mobilnego i aktualny krajobraz, i zapisałem wszystko w vaultcie jako trzy nowe notatki, spięte z istniejącymi MOC-ami.

## Co powstało

**1. `Wiedza/Zrodla_Mobile_Malware.md`** — analiza baz (sedno Twojej prośby)
Podział na **żywe** vs **historyczne** źródła:
- **Aktywne (tu trafia nowy malware):** MalwareBazaar (tagi `android`/`apk`/`banker` + API), Koodous (dedykowane APK), VirusTotal (triage), VirusShare (80M próbek), AndroZoo (24,5M APK), MalShare, `ashishb/android-malware`.
- **Sandboxy z publicznymi raportami** (= „darmowa dynamika" przed własną detonacją): Tria.ge, Any.Run, Joe Sandbox, Hybrid Analysis.
- **Intel o najnowszych rodzinach (TTP + IoC):** Cleafy, ThreatFabric, Securelist/Kaspersky, Barracuda, PolySwarm.
- **Historyczne (baseline, do nauki statyki):** Genome Project, Drebin, Contagio Mobile, PRAGuard, AMD, CIC-AndMal — martwe/nieaktualizowane, do nowych rodzin się nie nadają.
- Plus workflow budowania korpusu mobilnego.

**2. `Wiedza/Malware/Mobile_Malware_2024_2025.md`** — co jest teraz „na topie"
- Skala: **trojan-bankery +56%** (Kaspersky), **Android +67%** (Zscaler), **42M** złośliwych pobrań z Google Play.
- Dominujący trend: **bankery jako MaaS + On-Device Fraud** (DroidBot, Albiriox), ATS, VNC, **NFC relay** (RatOn + NFSkate).
- Tabela aktywnych rodzin: **RatOn, Albiriox, DroidBot, Frogblight, FvncBot/SeedSnatcher/ClayRat, LightSpy (iOS), Pegasus**, ze źródłami.

**3. `Lab/Android_RE_i_Dynamiczna_Analiza.md`** — roadmap na fazę RE/dynamiczną
- OPSEC/izolacja → Faza 1 statyczna (apktool/jadx/apkid/androguard/Ghidra) → Faza 2 dynamiczna (Frida + objection, mitmproxy, MobSF, NFCGate, uiautomator) → Faza 3 automatyzacja.
- Lista decyzji do podjęcia na następną sesję (wybór emulatora, pierwsza rodzina, czy testujemy NFC lokalnie).

## Spięte w istniejącej strukturze
Zlinkowałem nowe notatki w `Wiedza/Zrodla.md`, `Wiedza/Malware/Malware_MOC.md` (sekcja „Bankery / mobile"), `Lab/Narzedzia_RE.md` i dopisałem wpis do `Wiedza/Aktualizacje.md`.

## Rekomendacja na kolejny krok (gdy przejdziemy do RE/dynamiki)
Najlepszy pierwszy cel: **RatOn** (publiczne IoC u [PolySwarm](https://blog.polyswarm.io/raton-android-malware), bogate TTP: ATS + NFC + keylogger) albo **Albiriox** (świeży MaaS od [Cleafy](https://www.cleafy.com/cleafy-labs/albiriox-rat-mobile-malware-targeting-global-finance-and-crypto-wallets)). Przed własną detonacją warto sprawdzić hash w Tria.ge/Any.Run.

Chcesz, żebym teraz pobrał konkretne hashe RatOn/Albiriox z publicznych raportów i założył karty próbek w `Analizy/Malware/`, czy najpierw ustawiamy emulator + Frida pod fazę dynamiczną?

### 🤖 Asystent — 2026-08-16T01:43:35Z

Jasne — będę wszystko zapisywał w vaultcie Obsidian. Sprawdzę format dziennika/recapu, żeby dopisać też dzisiejszą sesję (research + rekomendacja następnych kroków), bo to na razie jest tylko w czacie.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:35Z

tool: run_code
{"code": "const files = [\n  \"Daily/2026-08-16.md\",\n  \"Lab/Recap 2026-08-15.md\",\n  \"Recap_2026-08-15.md\",\n  \"Analizy/Threat_Digest/2026-08-15.md\",\n];\nfor (const p of files) {\n  const r = await tools.read({ file_path: p, limit: 60 });\n  console.log(\"\\n===== \" + p + \"  (total \" + r.totalLines + \" lines) =====\");\n  for (const l of r.lines) console.log(l.text);\n}\nreturn \"ok\";", "description": "Read daily/recap/digest note formats"}

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:35Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:35Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:35Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:35Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:43:35Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:44:00Z

tool: run_code
{"code": "const ts = await tools.bash({ command: \"date -u +%Y-%m-%dT%H:%M:%SZ\", description: \"Get current UTC timestamp\" });\nconst now = ts.kind === \"foreground\" ? ts.stdout.text.trim() : \"2026-08-16T01:40:00Z\";\nconsole.log(\"now =\", now);\n\nconst entry = [\n'',\n'',\n'## Mobile malware — analiza baz + krajobraz + plan RE (' + now + ')',\n'',\n'Analiza baz malware mobilnego (Android/iOS) + krajobraz aktywnych rodzin 2024–2025 + roadmap RE / analizy dynamicznej.',\n'',\n'- Bazy (aktywne vs historyczne): [[Zrodla_Mobile_Malware]]',\n'- Aktywne rodziny 2024–2025: [[Mobile_Malware_2024
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:44:00Z

bash: date -u +%Y-%m-%dT%H:%M:%SZ

### 🛠️ Akcja/narzędzie — 2026-08-16T01:44:00Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:44:00Z



### 🤖 Asystent — 2026-08-16T01:44:09Z

Zapisane w Obsidianie. Podsumowanie tego, co trafiło do vaultu:

**Nowe notatki**
- `Wiedza/Zrodla_Mobile_Malware.md` — analiza baz malware mobilnego (aktywne vs historyczne)
- `Wiedza/Malware/Mobile_Malware_2024_2025.md` — aktywne rodziny 2024–2025 (RatOn, Albiriox, DroidBot, Frogblight, LightSpy…)
- `Lab/Android_RE_i_Dynamiczna_Analiza.md` — roadmap RE + analiza dynamiczna (Frida/MobSF/emulator/NFC)

**Zlinkowane / zaktualizowane**
- `Wiedza/Zrodla.md`, `Wiedza/Malware/Malware_MOC.md`, `Lab/Narzedzia_RE.md` — linki do nowych notatek
- `Wiedza/Aktualizacje.md` — wpis dziennika zmian `2026-08-16`
- `Daily/2026-08-16.md` — dopisana sekcja sesji (timestamp `2026-08-16T01:44:00Z`) z faktami i „Next" (wybór emulatora + pierwsza rodzina do RE)

Od teraz trzymam się zasady: **każdy kolejny krok zapisuję od razu w Obsidianie** (notatki + karty próbek + wpisy do MOC/Aktualizacje), zgodnie z konwencją vaultu. Commit i tak robi `obsidian-git` co 15 min, więc nowe pliki się same zsynchronizują.

Gotowy, żeby przejść do następnego kroku — np. pobrać publiczne hashe RatOn/Albiriox i założyć karty w `Analizy/Malware/`, albo ustawić emulator + Frida pod fazę dynamiczną. Co robimy najpierw?

### 🤖 Asystent — 2026-08-16T01:50:31Z

Dobre — cel jasny: **realnie aktywne, aktualnie działające malware mobilne** (RatOn, Albiriox i reszta 2024–2025), z prawdziwymi hashami z publicznych raportów, i karty w `Analizy/Malware/`. Zaczynam od wyciągnięcia IoC (SHA256, C2, pakiety) z raportów vendorów.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:31Z

tool: run_code
{"code": "await tools.todo_write({ todos: [\n  { content: \"Extract IoCs (SHA256/C2/package) from public reports (RatOn, Albiriox, DroidBot, Frogblight, FvncBot/SeedSnatcher/ClayRat)\", status: \"in_progress\" },\n  { content: \"Create RatOn sample card in Analizy/Malware\", status: \"pending\" },\n  { content: \"Create Albiriox sample card in Analizy/Malware\", status: \"pending\" },\n  { content: \"Create cards for other active families as data allows\", status: \"pending\" },\n  { content: \"Wire cards into Threat_Intel_MOC + Aktualizacje\", status: \"pending\" },\n]});\n\nconst urls = [\n 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:31Z

bash: todo_write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:31Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" "https://blog.polyswarm.io/raton-android-malware" | (grep -aq $'\x1f\x8b' && gunzip || cat) 2>/dev/null | sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' | tr -s ' ' > /tmp/raton-polyswarm.txt; echo "bytes=$(wc -c < /tmp/raton-polyswarm.txt)"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:31Z

bash: echo "HASHES:"; grep -oiE '[a-f0-9]{64}' /tmp/raton-polyswarm.txt | sort -u | head -40; echo "IPS:"; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/raton-polyswarm.txt | sort -u | head -30; echo "PACKAGES:"; grep -oE 'com\.[a-z0-9.]+' /tmp/raton-polyswarm.txt | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:32Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" "https://www.cleafy.com/cleafy-labs/albiriox-rat-mobile-malware-targeting-global-finance-and-crypto-wallets" | (grep -aq $'\x1f\x8b' && gunzip || cat) 2>/dev/null | sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' | tr -s ' ' > /tmp/albiriox-cleafy.txt; echo "bytes=$(wc -c < /tmp/albiriox-cleafy.txt)"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:32Z

bash: echo "HASHES:"; grep -oiE '[a-f0-9]{64}' /tmp/albiriox-cleafy.txt | sort -u | head -40; echo "IPS:"; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/albiriox-cleafy.txt | sort -u | head -30; echo "PACKAGES:"; grep -oE 'com\.[a-z0-9.]+' /tmp/albiriox-cleafy.txt | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:32Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" "https://thehackernews.com/2025/12/new-albiriox-maas-malware-targets-400.html" | (grep -aq $'\x1f\x8b' && gunzip || cat) 2>/dev/null | sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' | tr -s ' ' > /tmp/albiriox-thn.txt; echo "bytes=$(wc -c < /tmp/albiriox-thn.txt)"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:32Z

bash: echo "HASHES:"; grep -oiE '[a-f0-9]{64}' /tmp/albiriox-thn.txt | sort -u | head -40; echo "IPS:"; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/albiriox-thn.txt | sort -u | head -30; echo "PACKAGES:"; grep -oE 'com\.[a-z0-9.]+' /tmp/albiriox-thn.txt | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:32Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" "https://securelist.com/frogblight-banker/118440/" | (grep -aq $'\x1f\x8b' && gunzip || cat) 2>/dev/null | sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' | tr -s ' ' > /tmp/frogblight-securelist.txt; echo "bytes=$(wc -c < /tmp/frogblight-securelist.txt)"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:32Z

bash: echo "HASHES:"; grep -oiE '[a-f0-9]{64}' /tmp/frogblight-securelist.txt | sort -u | head -40; echo "IPS:"; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/frogblight-securelist.txt | sort -u | head -30; echo "PACKAGES:"; grep -oE 'com\.[a-z0-9.]+' /tmp/frogblight-securelist.txt | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:33Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" "https://blog.barracuda.com/2025/12/09/malware-brief-android-fvncbot-seedsnatcher-clayrat" | (grep -aq $'\x1f\x8b' && gunzip || cat) 2>/dev/null | sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' | tr -s ' ' > /tmp/fvncbot-barracuda.txt; echo "bytes=$(wc -c < /tmp/fvncbot-barracuda.txt)"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:33Z

bash: echo "HASHES:"; grep -oiE '[a-f0-9]{64}' /tmp/fvncbot-barracuda.txt | sort -u | head -40; echo "IPS:"; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/fvncbot-barracuda.txt | sort -u | head -30; echo "PACKAGES:"; grep -oE 'com\.[a-z0-9.]+' /tmp/fvncbot-barracuda.txt | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:34Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" "https://www.cleafy.com/cleafy-labs/droidbot-the-new-android-malware-as-a-service-targeting-banking-apps" | (grep -aq $'\x1f\x8b' && gunzip || cat) 2>/dev/null | sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' | tr -s ' ' > /tmp/droidbot-cleafy.txt; echo "bytes=$(wc -c < /tmp/droidbot-cleafy.txt)"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:34Z

bash: echo "HASHES:"; grep -oiE '[a-f0-9]{64}' /tmp/droidbot-cleafy.txt | sort -u | head -40; echo "IPS:"; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/droidbot-cleafy.txt | sort -u | head -30; echo "PACKAGES:"; grep -oE 'com\.[a-z0-9.]+' /tmp/droidbot-cleafy.txt | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:34Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:53Z

tool: run_code
{"code": "const urls = [\n  [\"raton-polyswarm\", \"https://blog.polyswarm.io/raton-android-malware\"],\n  [\"albiriox-cleafy\", \"https://www.cleafy.com/cleafy-labs/albiriox-rat-mobile-malware-targeting-global-finance-and-crypto-wallets\"],\n  [\"albiriox-thn\", \"https://thehackernews.com/2025/12/new-albiriox-maas-malware-targets-400.html\"],\n  [\"frogblight-securelist\", \"https://securelist.com/frogblight-banker/118440/\"],\n  [\"fvncbot-barracuda\", \"https://blog.barracuda.com/2025/12/09/malware-brief-android-fvncbot-seedsnatcher-clayrat\"],\n  [\"droidbot-cleafy\", \"https://www.cleafy
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:53Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://blog.polyswarm.io/raton-android-malware" -o /tmp/raton-polyswarm.raw

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:53Z

bash: if head -c2 /tmp/raton-polyswarm.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/raton-polyswarm.raw > /tmp/raton-polyswarm.txt; else cat /tmp/raton-polyswarm.raw > /tmp/raton-polyswarm.txt; fi; sed -i -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' /tmp/raton-polyswarm.txt; tr -s ' ' < /tmp/raton-polyswarm.txt > /tmp/raton-polyswarm.flat; wc -c /tmp/raton-polyswarm.flat

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:53Z

bash: echo "== HASHES =="; grep -oiE '[a-f0-9]{64}' /tmp/raton-polyswarm.flat | sort -u | head -40; echo "== IPS =="; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/raton-polyswarm.flat | sort -u | head -30; echo "== PACKAGES =="; grep -oE 'com\.[a-z0-9_.]+' /tmp/raton-polyswarm.flat | sort -u | head -30; echo "== C2 domains-ish =="; grep -oE '[a-z0-9.-]+\.(cyou|top|xyz|com|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|buzz|link|click|host|portmap|ddns|duckdns|hopto|no-ip)' /tmp/raton-polyswarm.flat | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:53Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://www.cleafy.com/cleafy-labs/albiriox-rat-mobile-malware-targeting-global-finance-and-crypto-wallets" -o /tmp/albiriox-cleafy.raw

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:53Z

bash: if head -c2 /tmp/albiriox-cleafy.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/albiriox-cleafy.raw > /tmp/albiriox-cleafy.txt; else cat /tmp/albiriox-cleafy.raw > /tmp/albiriox-cleafy.txt; fi; sed -i -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' /tmp/albiriox-cleafy.txt; tr -s ' ' < /tmp/albiriox-cleafy.txt > /tmp/albiriox-cleafy.flat; wc -c /tmp/albiriox-cleafy.flat

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:53Z

bash: echo "== HASHES =="; grep -oiE '[a-f0-9]{64}' /tmp/albiriox-cleafy.flat | sort -u | head -40; echo "== IPS =="; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/albiriox-cleafy.flat | sort -u | head -30; echo "== PACKAGES =="; grep -oE 'com\.[a-z0-9_.]+' /tmp/albiriox-cleafy.flat | sort -u | head -30; echo "== C2 domains-ish =="; grep -oE '[a-z0-9.-]+\.(cyou|top|xyz|com|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|buzz|link|click|host|portmap|ddns|duckdns|hopto|no-ip)' /tmp/albiriox-cleafy.flat | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://thehackernews.com/2025/12/new-albiriox-maas-malware-targets-400.html" -o /tmp/albiriox-thn.raw

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: if head -c2 /tmp/albiriox-thn.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/albiriox-thn.raw > /tmp/albiriox-thn.txt; else cat /tmp/albiriox-thn.raw > /tmp/albiriox-thn.txt; fi; sed -i -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' /tmp/albiriox-thn.txt; tr -s ' ' < /tmp/albiriox-thn.txt > /tmp/albiriox-thn.flat; wc -c /tmp/albiriox-thn.flat

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: echo "== HASHES =="; grep -oiE '[a-f0-9]{64}' /tmp/albiriox-thn.flat | sort -u | head -40; echo "== IPS =="; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/albiriox-thn.flat | sort -u | head -30; echo "== PACKAGES =="; grep -oE 'com\.[a-z0-9_.]+' /tmp/albiriox-thn.flat | sort -u | head -30; echo "== C2 domains-ish =="; grep -oE '[a-z0-9.-]+\.(cyou|top|xyz|com|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|buzz|link|click|host|portmap|ddns|duckdns|hopto|no-ip)' /tmp/albiriox-thn.flat | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://securelist.com/frogblight-banker/118440/" -o /tmp/frogblight-securelist.raw

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: if head -c2 /tmp/frogblight-securelist.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/frogblight-securelist.raw > /tmp/frogblight-securelist.txt; else cat /tmp/frogblight-securelist.raw > /tmp/frogblight-securelist.txt; fi; sed -i -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' /tmp/frogblight-securelist.txt; tr -s ' ' < /tmp/frogblight-securelist.txt > /tmp/frogblight-securelist.flat; wc -c /tmp/frogblight-securelist.flat

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: echo "== HASHES =="; grep -oiE '[a-f0-9]{64}' /tmp/frogblight-securelist.flat | sort -u | head -40; echo "== IPS =="; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/frogblight-securelist.flat | sort -u | head -30; echo "== PACKAGES =="; grep -oE 'com\.[a-z0-9_.]+' /tmp/frogblight-securelist.flat | sort -u | head -30; echo "== C2 domains-ish =="; grep -oE '[a-z0-9.-]+\.(cyou|top|xyz|com|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|buzz|link|click|host|portmap|ddns|duckdns|hopto|no-ip)' /tmp/frogblight-securelist.flat | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://blog.barracuda.com/2025/12/09/malware-brief-android-fvncbot-seedsnatcher-clayrat" -o /tmp/fvncbot-barracuda.raw

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: if head -c2 /tmp/fvncbot-barracuda.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/fvncbot-barracuda.raw > /tmp/fvncbot-barracuda.txt; else cat /tmp/fvncbot-barracuda.raw > /tmp/fvncbot-barracuda.txt; fi; sed -i -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' /tmp/fvncbot-barracuda.txt; tr -s ' ' < /tmp/fvncbot-barracuda.txt > /tmp/fvncbot-barracuda.flat; wc -c /tmp/fvncbot-barracuda.flat

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: echo "== HASHES =="; grep -oiE '[a-f0-9]{64}' /tmp/fvncbot-barracuda.flat | sort -u | head -40; echo "== IPS =="; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/fvncbot-barracuda.flat | sort -u | head -30; echo "== PACKAGES =="; grep -oE 'com\.[a-z0-9_.]+' /tmp/fvncbot-barracuda.flat | sort -u | head -30; echo "== C2 domains-ish =="; grep -oE '[a-z0-9.-]+\.(cyou|top|xyz|com|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|buzz|link|click|host|portmap|ddns|duckdns|hopto|no-ip)' /tmp/fvncbot-barracuda.flat | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://www.cleafy.com/cleafy-labs/droidbot-the-new-android-malware-as-a-service-targeting-banking-apps" -o /tmp/droidbot-cleafy.raw

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: if head -c2 /tmp/droidbot-cleafy.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/droidbot-cleafy.raw > /tmp/droidbot-cleafy.txt; else cat /tmp/droidbot-cleafy.raw > /tmp/droidbot-cleafy.txt; fi; sed -i -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e 's/&quot;/"/g' /tmp/droidbot-cleafy.txt; tr -s ' ' < /tmp/droidbot-cleafy.txt > /tmp/droidbot-cleafy.flat; wc -c /tmp/droidbot-cleafy.flat

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z

bash: echo "== HASHES =="; grep -oiE '[a-f0-9]{64}' /tmp/droidbot-cleafy.flat | sort -u | head -40; echo "== IPS =="; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/droidbot-cleafy.flat | sort -u | head -30; echo "== PACKAGES =="; grep -oE 'com\.[a-z0-9_.]+' /tmp/droidbot-cleafy.flat | sort -u | head -30; echo "== C2 domains-ish =="; grep -oE '[a-z0-9.-]+\.(cyou|top|xyz|com|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|buzz|link|click|host|portmap|ddns|duckdns|hopto|no-ip)' /tmp/droidbot-cleafy.flat | sort -u | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:50:54Z



### 🤖 Asystent — 2026-08-16T01:51:16Z

Mam hashe RatOn (5) i częściowe IoC Albiriox/Frogblight. Teraz dokopię się do hashów Albiriox/DroidBot i doprecyzuję IoC z treści raportów.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:16Z

tool: run_code
{"code": "// Inspect local text for IoC context + search for missing hashes\nconst g = await tools.bash({ command: `for f in albiriox-cleafy frogblight-securelist fvncbot-barracuda; do echo \"===== $f =====\"; grep -niE 'hash|sha256|ioc|c2|github|domain|package|dropper|\\\\bcom\\\\.[a-z]|194\\\\.32|45\\\\.138' /tmp/$f.flat | head -40; done`, description: \"Grep IoC context in reports\" });\nconsole.log(g.kind === \"foreground\" ? g.stdout.text : String(g));\n\n// Search for missing hashes\nconst queries = [\n  \"Albiriox Android malware SHA256 hash IoC Cleafy\",\n  \"DroidBot Android malware S
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:31Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:31Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:31Z

bash: web_search

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:31Z

bash: web_search

### 🤖 Asystent — 2026-08-16T01:51:52Z

Świetnie — mam pełny obraz Albiriox (C2 `194.32.79.94`, pakiety `com.nmz.nmz` + dropper PENNY) i Frogblight (MD5 próbki, C2). Teraz dobiorę hashe SHA256 Albiriox (blog PolySwarm) i DroidBot (poprawny raport Cleafy) oraz IoC FvncBot.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:52Z

tool: run_code
{"code": "async function dl(name, url) {\n  const r = await tools.bash({ command: `curl --compressed -sL --max-time 40 -A \"Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0\" -w \"HTTP=%{http_code} SIZE=%{size_download}\" \"${url}\" -o /tmp/${name}.raw; if head -c2 /tmp/${name}.raw | grep -q $'\\\\x1f\\\\x8b'; then gunzip -c /tmp/${name}.raw > /tmp/${name}.txt; else cat /tmp/${name}.raw > /tmp/${name}.txt; fi; sed -e 's/<script[^>]*>[^<]*<\\\\/script>//gi' -e 's/<style[^>]*>[^<]*<\\\\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\\\\&/g' -e 's/&#39;/'\"'\"
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:52Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://blog.polyswarm.io/albiriox-android-malware" -o /tmp/albiriox-polyswarm.raw; if head -c2 /tmp/albiriox-polyswarm.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/albiriox-polyswarm.raw > /tmp/albiriox-polyswarm.txt; else cat /tmp/albiriox-polyswarm.raw > /tmp/albiriox-polyswarm.txt; fi; sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:52Z

bash: echo "== SHA256 =="; grep -ohiE '[a-f0-9]{64}' /tmp/albiriox-polyswarm.raw /tmp/albiriox-polyswarm.flat 2>/dev/null | sort -u | head -40; echo "== MD5(32hex) =="; grep -ohiE '\b[a-f0-9]{32}\b' /tmp/albiriox-polyswarm.flat 2>/dev/null | sort -u | head -30; echo "== IPS =="; grep -ohE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/albiriox-polyswarm.flat | sort -u | head -20; echo "== PACKAGES =="; grep -ohE 'com\.[a-z0-9_.]+' /tmp/albiriox-polyswarm.flat | sort -u | head -20; echo "== C2-ish =="; grep -ohiE '[a-z0-9.-]+\.(cyou|top|xyz|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|l
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:53Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://www.cleafy.com/cleafy-labs/droidbot-insights-from-a-new-turkish-maas-fraud-operation" -o /tmp/droidbot-cleafy2.raw; if head -c2 /tmp/droidbot-cleafy2.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/droidbot-cleafy2.raw > /tmp/droidbot-cleafy2.txt; else cat /tmp/droidbot-cleafy2.raw > /tmp/droidbot-cleafy2.txt; fi; sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:53Z

bash: echo "== SHA256 =="; grep -ohiE '[a-f0-9]{64}' /tmp/droidbot-cleafy2.raw /tmp/droidbot-cleafy2.flat 2>/dev/null | sort -u | head -40; echo "== MD5(32hex) =="; grep -ohiE '\b[a-f0-9]{32}\b' /tmp/droidbot-cleafy2.flat 2>/dev/null | sort -u | head -30; echo "== IPS =="; grep -ohE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/droidbot-cleafy2.flat | sort -u | head -20; echo "== PACKAGES =="; grep -ohE 'com\.[a-z0-9_.]+' /tmp/droidbot-cleafy2.flat | sort -u | head -20; echo "== C2-ish =="; grep -ohiE '[a-z0-9.-]+\.(cyou|top|xyz|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:53Z

bash: curl --compressed -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0" -w "HTTP=%{http_code} SIZE=%{size_download}" "https://thehackernews.com/2025/12/android-malware-fvncbot-seedsnatcher.html" -o /tmp/fvncbot-thn.raw; if head -c2 /tmp/fvncbot-thn.raw | grep -q $'\x1f\x8b'; then gunzip -c /tmp/fvncbot-thn.raw > /tmp/fvncbot-thn.txt; else cat /tmp/fvncbot-thn.raw > /tmp/fvncbot-thn.txt; fi; sed -e 's/<script[^>]*>[^<]*<\/script>//gi' -e 's/<style[^>]*>[^<]*<\/style>//gi' -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&#39;/'"'"'/g' -e
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:53Z

bash: echo "== SHA256 =="; grep -ohiE '[a-f0-9]{64}' /tmp/fvncbot-thn.raw /tmp/fvncbot-thn.flat 2>/dev/null | sort -u | head -40; echo "== MD5(32hex) =="; grep -ohiE '\b[a-f0-9]{32}\b' /tmp/fvncbot-thn.flat 2>/dev/null | sort -u | head -30; echo "== IPS =="; grep -ohE '([0-9]{1,3}\.){3}[0-9]{1,3}' /tmp/fvncbot-thn.flat | sort -u | head -20; echo "== PACKAGES =="; grep -ohE 'com\.[a-z0-9_.]+' /tmp/fvncbot-thn.flat | sort -u | head -20; echo "== C2-ish =="; grep -ohiE '[a-z0-9.-]+\.(cyou|top|xyz|net|io|ru|tk|ml|ga|cf|gg|shop|online|site|icu|club|space|monster|life|store|buzz|link|click|host|port
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:51:53Z



### 🤖 Asystent — 2026-08-16T01:52:30Z

Mam hashe dla wszystkich kluczowych rodzin. Doprecyzuję jeszcze C2 Frogblight i szczegóły RatOn z treści raportów, potem zakładam karty.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:30Z

tool: run_code
{"code": "const g = await tools.bash({ command: `echo \"===== frogblight C2/IoC context =====\"; grep -niE '45\\\\.138|C2|hunter|github|IoCs|indicators|control server|domain|http[s]?://[a-z0-9.-]+' /tmp/frogblight-securelist.flat | grep -viE 'google|facebook|kasperskycontenthub|securelist.com|gstatic' | head -30; echo; echo \"===== raton C2/package context =====\"; grep -niE 'C2|control server|NFSkate|domain|APK|package|installApk|dropper|adult' /tmp/raton-polyswarm.flat | head -30`, description: \"Grep C2/package context\" });\nconsole.log(g.kind === \"foreground\" ? g.stdout.text : String(g)
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:30Z

bash: echo "===== frogblight C2/IoC context ====="; grep -niE '45\.138|C2|hunter|github|IoCs|indicators|control server|domain|http[s]?://[a-z0-9.-]+' /tmp/frogblight-securelist.flat | grep -viE 'google|facebook|kasperskycontenthub|securelist.com|gstatic' | head -30; echo; echo "===== raton C2/package context ====="; grep -niE 'C2|control server|NFSkate|domain|APK|package|installApk|dropper|adult' /tmp/raton-polyswarm.flat | head -30

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:30Z

bash: for t in RatOn Albiriox DroidBot Frogblight; do echo "== $t =="; curl -sL --max-time 25 -X POST https://mb-api.abuse.ch/api/v1/ -d "query=get_taginfo&tag=$t&limit=5" | head -c 800; echo; done

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:30Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:44Z

tool: run_code
{"code": "// 1) Frogblight IP context; 2) check MalwareBazaar key; 3) query MB if key present\nconst ctx = await tools.bash({ command: `grep -oE '.{120}45\\\\.138\\\\.16\\\\.208.{120}' /tmp/frogblight-securelist.raw 2>/dev/null | head -5; echo \"---raw hash check---\"; grep -ohiE '[a-f0-9]{64}' /tmp/frogblight-securelist.raw | sort -u | head -20`, description: \"Frogblight IP context + hashes\" });\nconsole.log(\"FROGBLIGHT:\", ctx.kind === \"foreground\" ? ctx.stdout.text : String(ctx));\n\nconst key = await tools.bash({ command: `for p in ~/.mb_api_key /root/.mb_api_key /root/mb_api_key; do 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:44Z

bash: grep -oE '.{120}45\.138\.16\.208.{120}' /tmp/frogblight-securelist.raw 2>/dev/null | head -5; echo "---raw hash check---"; grep -ohiE '[a-f0-9]{64}' /tmp/frogblight-securelist.raw | sort -u | head -20

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:44Z

bash: for p in ~/.mb_api_key /root/.mb_api_key /root/mb_api_key; do if [ -f "$p" ]; then echo "FOUND $p"; cat "$p"; fi; done; echo "--- env ---"; env | grep -iE 'mb|malware|abuse|bazaar' || echo "(no env)"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:44Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:59Z

tool: run_code
{"code": "const KEY = \"9dab735a10242275499ab84838050ab39c2151427b6e7c72\";\n\n// Verify Frogblight IP context in stripped text\nconst ip = await tools.bash({ command: `grep -oE '.{80}45\\\\.138\\\\.16\\\\.208.{80}' /tmp/frogblight-securelist.flat | head -3`, description: \"Frogblight IP context\" });\nconsole.log(\"FROGBLIGHT IP ctx:\", ip.kind === \"foreground\" ? ip.stdout.text : \"(none)\");\n\n// MalwareBazaar queries with key\nfor (const t of [\"raton\", \"albiriox\", \"droidbot\", \"frogblight\"]) {\n  const r = await tools.bash({ command: `curl -sL --max-time 25 -X POST https://mb-api.
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:59Z

bash: grep -oE '.{80}45\.138\.16\.208.{80}' /tmp/frogblight-securelist.flat | head -3

### 🛠️ Akcja/narzędzie — 2026-08-16T01:52:59Z

bash: curl -sL --max-time 25 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_taginfo&tag=raton&limit=5"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:00Z

bash: curl -sL --max-time 25 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_taginfo&tag=albiriox&limit=5"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:00Z

bash: curl -sL --max-time 25 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_taginfo&tag=droidbot&limit=5"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:00Z

bash: curl -sL --max-time 25 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_taginfo&tag=frogblight&limit=5"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:00Z



### 🤖 Asystent — 2026-08-16T01:53:13Z

Klucz MalwareBazaar działa i znalazłem **prawdziwego Albirioxa APK** (pierwszy raz widziany 2026-07-22). Dobiorę wszystkie próbki Albiriox + sprawdzę pozostałe rodziny po sygnaturze.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:13Z

tool: run_code
{"code": "const KEY = \"9dab735a10242275499ab84838050ab39c2151427b6e7c72\";\n\nasync function siginfo(sig) {\n  const r = await tools.bash({ command: `curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H \"Auth-Key: ${KEY}\" -d \"query=get_siginfo&signature=${sig}&limit=50\"`, description: \"MB siginfo \" + sig });\n  return r.kind === \"foreground\" ? r.stdout.text : \"\";\n}\n\n// parse and print compactly\nfor (const sig of [\"Albiriox\", \"RatOn\", \"DroidBot\", \"Frogblight\", \"FvncBot\", \"SeedSnatcher\", \"ClayRat\"]) {\n  const txt = await siginfo(sig);\n  let out = \"\";
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:14Z

bash: curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_siginfo&signature=Albiriox&limit=50"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:14Z

bash: curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_siginfo&signature=RatOn&limit=50"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:14Z

bash: curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_siginfo&signature=DroidBot&limit=50"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:14Z

bash: curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_siginfo&signature=Frogblight&limit=50"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:15Z

bash: curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_siginfo&signature=FvncBot&limit=50"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:15Z

bash: curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_siginfo&signature=SeedSnatcher&limit=50"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:15Z

bash: curl -sL --max-time 30 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_siginfo&signature=ClayRat&limit=50"

### 🛠️ Akcja/narzędzie — 2026-08-16T01:53:15Z



### 🤖 Asystent — 2026-08-16T01:55:07Z

Mam wszystko, czego trzeba — realne, aktualne hashe APK (Albiriox, ClayRat) z MalwareBazaar + hashe z raportów (RatOn, DroidBot, Frogblight). Zakładam karty próbek.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:07Z

tool: run_code
{"code": "async function w(path, lines) {\n  try { const r = await tools.write({ file_path: path, content: lines.join(\"\\n\") }); return \"OK  \" + path + \" (\" + r.operation + \")\"; }\n  catch (e) { return \"ERR \" + path + \": \" + (e && e.message ? e.message : String(e)); }\n}\n\nconst cards = {};\n\ncards[\"Analizy/Malware/Albiriox_Android_RAT.md\"] = [\n'---',\n'title: \"Albiriox — Android RAT / MaaS (ODF)\"',\n'date: 2026-08-16',\n'updated: 2026-08-16',\n'tags: [sample, apk, android, albiriox, rat, mas, malware, analysis, ioc]',\n'status: pending',\n'priority: high',\n'category: rat',
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:07Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:07Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:07Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:07Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:07Z

bash: write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:07Z



### 🤖 Asystent — 2026-08-16T01:55:16Z

5 kart założonych. Teraz spinam je z MOC i dziennikiem — czytam dokładne miejsca wstawienia.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:16Z

tool: run_code
{"code": "const moc = await tools.read({ file_path: \"Analizy/Threat_Intel_MOC.md\" });\nconsole.log(\"===== Threat_Intel_MOC (total \" + moc.totalLines + \") =====\");\nfor (const l of moc.lines) console.log(l.text);\n\nconst akt = await tools.read({ file_path: \"Wiedza/Aktualizacje.md\", limit: 20 });\nconsole.log(\"\\n===== Aktualizacje (head) =====\");\nfor (const l of akt.lines) console.log(l.text);\nreturn \"ok\";", "description": "Read MOC and changelog for insertion points"}

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:16Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:16Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:16Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:39Z

tool: run_code
{"code": "const mobileSection = [\n'## Mobile (Android) — 2024–2025 (IoC zebrane, RE przed nami)',\n'',\n'| Rodzina | Hash (przykład) | C2 | Status | Nota |',\n'|---------|-----------------|-----|--------|------|',\n'| **Albiriox** (RAT/MaaS, ODF) | `8703ee86…` (apk, MB 2026-07) | `194.32.79.94` | IoC zebrane | [[Albiriox_Android_RAT]] |',\n'| **ClayRat** (RAT, masquerade) | `78878d33…` (apk, MB 2026-03) | — | IoC zebrane | [[ClayRat_Android_RAT]] |',\n'| **RatOn** (banker, NFC+ATS) | `bf82609c…` (PolySwarm) | — | IoC zebrane | [[RatOn_Android_banker]] |',\n'| **DroidBot** (RAT/MaaS, VNC) | MD
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:39Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:39Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:39Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:39Z

bash: todo_write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:39Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:44Z

tool: run_code
{"code": "const r = await tools.bash({ command: \"ls -la Analizy/Malware/ | grep -E 'Albiriox|ClayRat|RatOn|DroidBot|Frogblight'\", description: \"Confirm new card files\" });\nconsole.log(r.kind === \"foreground\" ? r.stdout.text : String(r));\n\n// quick sanity check one card\nconst c = await tools.read({ file_path: \"Analizy/Malware/Albiriox_Android_RAT.md\", limit: 22 });\nconsole.log(\"\\n=== Albiriox card head ===\");\nfor (const l of c.lines) console.log(l.text);\nreturn \"ok\";", "description": "Verify new cards exist and are valid"}

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:44Z

bash: ls -la Analizy/Malware/ | grep -E 'Albiriox|ClayRat|RatOn|DroidBot|Frogblight'

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:44Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T01:55:44Z



### 🤖 Asystent — 2026-08-16T01:55:54Z

Zrobione — wszystko zapisane w Obsidianie. Pobrałem **realne hashe aktualnie działającego malware mobilnego** (z publicznych raportów + MalwareBazaar) i założyłem 5 kart próbek w `Analizy/Malware/`.

## Karty próbek (nowe pliki)

| Karta | Co to | Hashe | Źródło |
|-------|-------|-------|--------|
| `Albiriox_Android_RAT.md` | RAT/MaaS, On-Device Fraud | **2× SHA256 (realne APK z MalwareBazaar, 2026-07 i 2025-12)** + 4× SHA256 (PolySwarm) + C2 `194.32.79.94` | Cleafy + PolySwarm + MB |
| `ClayRat_Android_RAT.md` | RAT podszywający się pod YouTube/taxi | **10× SHA256 (realne APK z MalwareBazaar, XI 2025 – III 2026)** | Barracuda + MB |
| `RatOn_Android_banker.md` | bankowy trojan, NFC relay + ATS | 5× SHA256 | PolySwarm/ThreatFabric |
| `DroidBot_Android_RAT.md` | RAT/MaaS (VNC), turecki | 5× MD5 + lista celów (BBVA, Binance, Kraken…) | Cleafy |
| `Frogblight_Android_banker.md` | bankowy trojan (WebView injection) | MD5 `9dac2320…` + pakiety | Securelist |

**Najważniejsze dla Ciebie:** Albiriox i ClayRat mają **świeże APK na MalwareBazaar** (widziane 2026-07-22 i 2026-03-24) — to „wirusy, które realnie działają teraz na telefonach", z potwierdzonymi hashami do pobrania przez `mb-api.abuse.ch` (klucz `Auth-Key` już masz w `/root/.mb_api_key`, działa).

## Spięte w vaultcie
- `Analizy/Threat_Intel_MOC.md` — nowa sekcja „Mobile (Android) 2024–2025 (IoC zebrane)" z tabelą rodzina→hash→C2→nota
- `Wiedza/Malware/Mobile_Malware_2024_2025.md` — sekcja „Karty próbek w labie"
- `Wiedza/Aktualizacje.md` — wpis do dziennika zmian

Każda karta ma status `pending`, IoC, skrót TTP, sekcję „Next (RE)" i źródła. Wszystko w konwencji vaultu (frontmatter, linki `[[…]]`), commit zrobi `obsidian-git`.

## Proponowany następny krok
Pobrać przez MalwareBazaar jedną próbkę (np. Albiriox `8703ee86…` albo ClayRat `78878d33…`) do izolowanego katalogu i zrobić **statykę**: `apkid` (wykrycie JSONPacker/packera) → `jadx`/`apktool` → manifest + uprawnienia Accessibility/overlay. To daje pierwszy „RE end-to-end" na prawdziwym, aktualnym APK. Chcesz, żebym teraz ściągnął tę jedną próbkę (tylko hash/statyka, bez detonacji) i zaczął?

### 🤖 Asystent — 2026-08-16T01:59:10Z

Tak — biorę się za reverse engineering. Zaczynam od sprawdzenia, jakie narzędzia mam na tym hoście, potem ściągam prawdziwy APK Albiriox i robię statykę.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:10Z

tool: run_code
{"code": "await tools.todo_write({ todos: [\n  { content: \"Check available RE tooling on this host\", status: \"in_progress\" },\n  { content: \"Download Albiriox APK from MalwareBazaar (isolated)\", status: \"pending\" },\n  { content: \"Static RE: file/sha256/zip listing\", status: \"pending\" },\n  { content: \"Static RE: apkid packer detection\", status: \"pending\" },\n  { content: \"Static RE: decompile (jadx/apktool) + manifest audit\", status: \"pending\" },\n  { content: \"Static RE: strings/IoC (C2, URLs, JSON keys)\", status: \"pending\" },\n  { content: \"Write findings back to Ob
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:10Z

bash: todo_write

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:10Z

bash: 
echo "== host =="; hostname; uname -a; cat /etc/os-release 2>/dev/null | head -3
echo "== whoami/pwd=<REDACTED> whoami; pwd
echo "== disk =="; df -h / | tail -1
echo "== tools =="
for t in java jadx apktool apkid aapt aapt2 python3 pip3 unzip zip strings file node curl wget git d8 dex2jar r2 radare2 rizin ghidra; do printf "%-10s " "$t"; command -v "$t" >/dev/null 2>&1 && echo "$(command -v $t)" || echo "MISSING"; done
echo "== python RE libs =="
python3 -c "import androguard; print('androguard', androguard.__version__)" 2>&1 | head -1
python3 -c "import frida; print('frida', frida.__version_
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:10Z



### 🤖 Asystent — 2026-08-16T01:59:36Z

Świetnie — mam `radare2`, `capstone`, `yara-python`, `java`, `strings`. Brakuje `jadx`/`apktool`/`androguard` — doinstaluję. Najpierw ściągam prawdziwy APK Albiriox i robię podstawowy triage.

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:36Z

tool: run_code
{"code": "const KEY = \"9dab735a10242275499ab84838050ab39c2151427b6e7c72\";\nconst HASH = \"8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e\";\n\nconst dl = await tools.bash({ command: `\nset -e\nmkdir -p /root/malware-lab/albiriox\ncd /root/malware-lab/albiriox\ncurl -sL --max-time 60 -X POST https://mb-api.abuse.ch/api/v1/ -H \"Auth-Key: ${KEY}\" -d \"query=get_file&sha256_hash=${HASH}\" -o 8703ee86.apk\necho \"== size ==\"; ls -la 8703ee86.apk\necho \"== sha256 (must equal) ==\"; sha256sum 8703ee86.apk\necho \"== expected ==\"; echo \"${HASH}\"\necho \"== file type ==\"; fi
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:37Z

bash: 
set -e
mkdir -p /root/malware-lab/albiriox
cd /root/malware-lab/albiriox
curl -sL --max-time 60 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_file&sha256_hash=8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e" -o 8703ee86.apk
echo "== size =="; ls -la 8703ee86.apk
echo "== sha256 (must equal) =="; sha256sum 8703ee86.apk
echo "== expected =="; echo "8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e"
echo "== file type =="; file 8703ee86.apk
echo "== zip listing =="; unzip -l 8703ee86.apk
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:37Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:50Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox\necho \"== tools for extraction ==\"\nfor t in 7z 7za bsdtar unzip; do printf \"%-8s \" \"$t\"; command -v \"$t\" || echo MISSING; done\necho \"== try unzip (ZipCrypto) ==\"\nunzip -P infected 8703ee86.apk -d extracted 2>&1 | head -20\necho \"== exit $? ==\"\necho \"== if extracted, verify ==\"\nls -la extracted/ 2>/dev/null\nsha256sum extracted/*.apk 2>/dev/null\n`, description: \"Extract inner APK and verify hash\" });\nconsole.log(r.kind === \"foreground\" ? r.stdout.text : String(r));\nreturn \"ok\";", "descri
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:50Z

bash: 
cd /root/malware-lab/albiriox
echo "== tools for extraction =="
for t in 7z 7za bsdtar unzip; do printf "%-8s " "$t"; command -v "$t" || echo MISSING; done
echo "== try unzip (ZipCrypto) =="
unzip -P infected 8703ee86.apk -d extracted 2>&1 | head -20
echo "== exit $? =="
echo "== if extracted, verify =="
ls -la extracted/ 2>/dev/null
sha256sum extracted/*.apk 2>/dev/null


### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:50Z



### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:55Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox\nrm -rf extracted && mkdir -p extracted\n7z x -pinfected 8703ee86.apk -oextracted -y 2>&1 | tail -20\necho \"== verify ==\"\nls -la extracted/\nsha256sum extracted/*.apk\necho \"== expected ==\"\necho \"8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e\"\necho \"== file ==\"\nfile extracted/*.apk\necho \"== APK zip listing ==\"\nunzip -l extracted/*.apk\n`, description: \"Extract inner APK with 7z\" });\nconsole.log(r.kind === \"foreground\" ? r.stdout.text : String(r));\nreturn \"ok\";", "descripti
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:55Z

bash: 
cd /root/malware-lab/albiriox
rm -rf extracted && mkdir -p extracted
7z x -pinfected 8703ee86.apk -oextracted -y 2>&1 | tail -20
echo "== verify =="
ls -la extracted/
sha256sum extracted/*.apk
echo "== expected =="
echo "8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e"
echo "== file =="
file extracted/*.apk
echo "== APK zip listing =="
unzip -l extracted/*.apk


### 🛠️ Akcja/narzędzie — 2026-08-16T01:59:55Z



### 🤖 Asystent — 2026-08-16T02:00:29Z

Próbka pobrana i wypakowana (7z). APK zawiera ~1000 plików-dekójek (zaciemnione assety + fałszywe konfigi aws/firebase/knox) — typowe dla JSONPacker. Robię czysty triage (weryfikacja hasha + kluczowe pliki) i równolegle doinstalowuję narzędzia.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:29Z

tool: run_code
{"code": "// kick off tool install in background\nconst install = await tools.bash({ command: \"pip3 install --quiet --no-warn-script-location androguard apkid 2>&1 | tail -5; echo 'PIP_DONE'\", description: \"Install androguard + apkid\", run_in_background: true });\nconsole.log(\"install job:\", install.kind === \"background\" ? install.jobId : JSON.stringify(install));\n\n// clean triage\nconst r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox/extracted\nAPK=$(ls *.apk | head -1)\necho \"== APK file ==\"; ls -la \"$APK\"\necho \"== sha256 ==\"; sha256sum \"$APK\"\necho \"== e
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:29Z

bash: pip3 install --quiet --no-warn-script-location androguard apkid 2>&1 | tail -5; echo 'PIP_DONE'

### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:29Z

bash: 
cd /root/malware-lab/albiriox/extracted
APK=$(ls *.apk | head -1)
echo "== APK file =="; ls -la "$APK"
echo "== sha256 =="; sha256sum "$APK"
echo "== expected =="; echo "8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e"
echo "== file =="; file "$APK"
echo "== KEY files only =="
unzip -l "$APK" | grep -iE 'classes[0-9]*\.dex|lib/.+\.so|AndroidManifest\.xml|resources\.arsc|META-INF|assets/.*\.dex|assets/.*\.apk' | head -60
echo "== top-level summary =="
unzip -l "$APK" | awk '{print $4}' | grep -vE '^$' | awk -F/ '{print $1}' | sort | uniq -c | sort -rn | head -20


### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:29Z



### 🤖 Asystent — 2026-08-16T02:00:49Z

Weryfikacja OK — hash się zgadza, to realny APK (DEX-only, Kotlin/AndroidX, mocno zaśmiecony dekójkami + obfuskacja `META-INF/services`). Wyciągam `classes.dex` i robię pierwszy pas `strings` na IoC.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:49Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox/extracted\nAPK=$(ls *.apk | head -1)\nunzip -o -q \"$APK\" classes.dex AndroidManifest.xml -d .\necho \"== classes.dex size ==\"; ls -la classes.dex AndroidManifest.xml\necho \"== IPs in classes.dex ==\"\nstrings -n 6 classes.dex | grep -oE '([0-9]{1,3}\\\\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn | head -20\necho \"== URLs ==\"\nstrings -n 6 classes.dex | grep -oE 'https?://[a-zA-Z0-9./_?=&-]+' | sort -u | head -30\necho \"== interesting keywords (count) ==\"\nfor kw in vnc VNC accessibility Accessibility over
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:49Z

bash: 
cd /root/malware-lab/albiriox/extracted
APK=$(ls *.apk | head -1)
unzip -o -q "$APK" classes.dex AndroidManifest.xml -d .
echo "== classes.dex size =="; ls -la classes.dex AndroidManifest.xml
echo "== IPs in classes.dex =="
strings -n 6 classes.dex | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn | head -20
echo "== URLs =="
strings -n 6 classes.dex | grep -oE 'https?://[a-zA-Z0-9./_?=&-]+' | sort -u | head -30
echo "== interesting keywords (count) =="
for kw in vnc VNC accessibility Accessibility overlay Overlay ping pong handshake Handshake HWID socket Socket nmz A
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:49Z

bash: job_output

### 🛠️ Akcja/narzędzie — 2026-08-16T02:00:49Z



### 🤖 Asystent — 2026-08-16T02:01:11Z

Dwa problemy do naprawy: pip zablokowany (PEP 668 — potrzebny `--break-system-packages`), a ekstrakcja dex się nie powiodła (patrzyłem tylko na stdout). Naprawiam oba.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:11Z

tool: run_code
{"code": "// install tools with --break-system-packages (background)\nconst inst = await tools.bash({ command: \"pip3 install --break-system-packages --quiet --no-warn-script-location androguard apkid 2>&1 | tail -8; echo 'PIP_DONE'\", description: \"Install androguard + apkid (break-system-packages)\", run_in_background: true });\nconsole.log(\"install job:\", inst.kind === \"background\" ? inst.jobId : JSON.stringify(inst));\n\n// re-extract with stderr visible\nconst r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox/extracted\nAPK=$(ls *.apk | head -1)\necho \"APK=$APK\"\nunz
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:11Z

bash: pip3 install --break-system-packages --quiet --no-warn-script-location androguard apkid 2>&1 | tail -8; echo 'PIP_DONE'

### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:12Z

bash: 
cd /root/malware-lab/albiriox/extracted
APK=$(ls *.apk | head -1)
echo "APK=$APK"
unzip -o "$APK" classes.dex AndroidManifest.xml 2>&1
echo "--- ls ---"
ls -la classes.dex AndroidManifest.xml 2>&1


### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:12Z



### 🤖 Asystent — 2026-08-16T02:01:36Z

Kluczowe odkrycie: `classes.dex` jest **zaszyfrowany** ("unable to get password"), a `AndroidManifest.xml` ma **podrobioną metodę kompresji (24753)** — to potwierdza, że próbka jest spakowana (JSONPacker/Golden Crypt, jak pisał Cleafy). Sprawdzam strukturę ZIP przez 7z i detekcję packera przez apkid.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:36Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox/extracted\nAPK=$(ls *.apk | head -1)\necho \"== 7z detailed listing (key entries) ==\"\n7z l -slt \"$APK\" 2>/dev/null | awk '/^Path = /{p=$3} /^Size = /{s=$3} /^Method = /{m=$0} /^Encrypted = /{e=$0; if (p ~ /classes.dex|AndroidManifest|resources.arsc|\\.so$/ || m ~ /AES|24753|ZipCrypto/) print p, \"|\", s, \"|\", m, \"|\", e}'\necho\necho \"== total entries + encrypted count ==\"\n7z l -slt \"$APK\" 2>/dev/null | grep -c '^Encrypted = +' \necho \"encrypted entries above (count of '+' lines)\"\necho \"== try 7z e
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:36Z

bash: 
cd /root/malware-lab/albiriox/extracted
APK=$(ls *.apk | head -1)
echo "== 7z detailed listing (key entries) =="
7z l -slt "$APK" 2>/dev/null | awk '/^Path = /{p=$3} /^Size = /{s=$3} /^Method = /{m=$0} /^Encrypted = /{e=$0; if (p ~ /classes.dex|AndroidManifest|resources.arsc|.so$/ || m ~ /AES|24753|ZipCrypto/) print p, "|", s, "|", m, "|", e}'
echo
echo "== total entries + encrypted count =="
7z l -slt "$APK" 2>/dev/null | grep -c '^Encrypted = +' 
echo "encrypted entries above (count of '+' lines)"
echo "== try 7z extract =="
rm -rf apk_x && 7z x -y "$APK" -oapk_x 2>&1 | tail -8


### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:36Z

bash: job_output

### 🛠️ Akcja/narzędzie — 2026-08-16T02:01:36Z



### 🤖 Asystent — 2026-08-16T02:02:18Z

To jest kluczowe odkrycie RE: **cały APK jest opakowany** — wszystkie 1005 wpisów ZIP (łącznie z `classes.dex`, `AndroidManifest.xml`, `resources.arsc`) są szyfrowane **ZipCrypto** ("Encrypted = +"), a manifest ma podrobioną metodę kompresji 24753 + ~1000 plików-dekójek (fałszywe konfigi aws/firebase/knox/azure + losowe assety). To potwierdza "JSONPacker/Golden Crypt" wg Cleafy. Identyfikuję packer i próbuję odzyskać klucz.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:02:18Z

tool: run_code
{"code": "// background: clean venv + apkid + androguard\nconst inst = await tools.bash({ command: \"python3 -m venv /opt/retools && /opt/retools/bin/pip install --quiet --no-warn-script-location apkid androguard 2>&1 | tail -5; echo 'VENV_DONE'\", description: \"Create venv with apkid+androguard\", run_in_background: true });\nconsole.log(\"venv job:\", inst.kind === \"background\" ? inst.jobId : JSON.stringify(inst));\n\n// foreground: try common ZipCrypto passwords + characterize packer via central directory\nconst r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox/extracted\n
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:02:18Z

bash: python3 -m venv /opt/retools && /opt/retools/bin/pip install --quiet --no-warn-script-location apkid androguard 2>&1 | tail -5; echo 'VENV_DONE'

### 🛠️ Akcja/narzędzie — 2026-08-16T02:02:19Z

bash: 
cd /root/malware-lab/albiriox/extracted
APK=$(ls *.apk | head -1)
echo "== try common passwords =="
for p in infected malware 123456 password albiriox nmz 1234 admin test; do
  out=$(7z t -p"$p" "$APK" 2>&1 >/dev/null | head -1)
  echo "  pw='$p' -> $out"
done
echo
echo "== EOCD / central directory scan for packer markers =="
strings -a "$APK" | grep -iE 'jiagu|bangcle|tencent|360|alibaba|ijiami|dprotect|dexprotector|libshella|libprotect|apkprotect|protectAPK|packer|stub|nagain|npack|appsealing|dexjaguar|tinker|reinforce' | head -20
echo "(markers above, if any)"
echo
echo "== first byt
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:02:19Z



### 🛠️ Akcja/narzędzie — 2026-08-16T02:02:59Z

tool: run_code
{"code": "const KEY = \"9dab735a10242275499ab84838050ab39c2151427b6e7c72\";\nconst samples = [\n  [\"albiriox2\", \"3269a0116ce0915afdd32e8d87b05ae9f5c00fcf0a6729add39a6a87aaf30089\"],\n  [\"clayrat_videodtp\", \"78878d33b2b48747694ce2fdb24e896cd9ba027b1d66c66c107cf415ed46b89b\"],\n  [\"clayrat_youtube\", \"b08e5a842cd24d955a00a060d9d58cbc4297ac4d10a98958ac8e88f79018ce86\"],\n];\n\nasync function grab(name, hash) {\n  const dir = `/root/malware-lab/${name}`;\n  const r = await tools.bash({ command: `\nset -e\nmkdir -p ${dir}\ncd ${dir}\ncurl -sL --max-time 60 -X POST https://mb-api.abuse.ch/ap
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:00Z

bash: 
set -e
mkdir -p /root/malware-lab/albiriox2
cd /root/malware-lab/albiriox2
curl -sL --max-time 60 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_file&sha256_hash=3269a0116ce0915afdd32e8d87b05ae9f5c00fcf0a6729add39a6a87aaf30089" -o w.zip
7z x -pinfected w.zip -y >/dev/null 2>&1
APK=$(find . -name '*.apk' | head -1)
echo "APK=$APK"
sha256sum "$APK" | awk '{print "sha256=" $1}'
echo "expected=3269a0116ce0915afdd32e8d87b05ae9f5c00fcf0a6729add39a6a87aaf30089"
echo "encrypted_entries=$(7z l -slt "$APK" 2>/dev/null | grep -
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:01Z

bash: 
set -e
mkdir -p /root/malware-lab/clayrat_videodtp
cd /root/malware-lab/clayrat_videodtp
curl -sL --max-time 60 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_file&sha256_hash=78878d33b2b48747694ce2fdb24e896cd9ba027b1d66c66c107cf415ed46b89b" -o w.zip
7z x -pinfected w.zip -y >/dev/null 2>&1
APK=$(find . -name '*.apk' | head -1)
echo "APK=$APK"
sha256sum "$APK" | awk '{print "sha256=" $1}'
echo "expected=78878d33b2b48747694ce2fdb24e896cd9ba027b1d66c66c107cf415ed46b89b"
echo "encrypted_entries=$(7z l -slt "$APK" 2>/dev
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:02Z

bash: 
set -e
mkdir -p /root/malware-lab/clayrat_youtube
cd /root/malware-lab/clayrat_youtube
curl -sL --max-time 60 -X POST https://mb-api.abuse.ch/api/v1/ -H "Auth-Key: 9dab735a10242275499ab84838050ab39c2151427b6e7c72" -d "query=get_file&sha256_hash=b08e5a842cd24d955a00a060d9d58cbc4297ac4d10a98958ac8e88f79018ce86" -o w.zip
7z x -pinfected w.zip -y >/dev/null 2>&1
APK=$(find . -name '*.apk' | head -1)
echo "APK=$APK"
sha256sum "$APK" | awk '{print "sha256=" $1}'
echo "expected=b08e5a842cd24d955a00a060d9d58cbc4297ac4d10a98958ac8e88f79018ce86"
echo "encrypted_entries=$(7z l -slt "$APK" 2>/dev/n
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:02Z

bash: job_output

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:02Z



### 🤖 Asystent — 2026-08-16T02:03:26Z

Dobra wiadomość: **`albiriox2` (dexopt.sssgf.apk) NIE jest zaszyfrowany** — ma 7 plików `classes*.dex` (multi-dex) i jest analizowalny. To najprawdopodobniej nieopakowany wariant Albiriox. Przechodzę na niego — apkid + manifest + DEX.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:26Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox2\nAPK=$(find . -name '*.apk' | head -1)\necho \"== apkid ==\"\n/opt/retools/bin/apkid \"$APK\" 2>&1 | head -40\necho\necho \"== extract ==\"\nrm -rf ex && mkdir ex && unzip -o -q \"$APK\" -d ex 2>&1 | tail -3\nls -la ex/ | grep -E 'classes|Manifest|resources.arsc|lib' \necho\necho \"== manifest decode (androguard) ==\"\n/opt/retools/bin/androguard axml ex/AndroidManifest.xml 2>/dev/null > manifest.xml\nwc -l manifest.xml\necho \"--- package ---\"; grep -oE 'package=\"[^\"]*\"' manifest.xml | head -3\necho \"--- pe
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:27Z

bash: 
cd /root/malware-lab/albiriox2
APK=$(find . -name '*.apk' | head -1)
echo "== apkid =="
/opt/retools/bin/apkid "$APK" 2>&1 | head -40
echo
echo "== extract =="
rm -rf ex && mkdir ex && unzip -o -q "$APK" -d ex 2>&1 | tail -3
ls -la ex/ | grep -E 'classes|Manifest|resources.arsc|lib' 
echo
echo "== manifest decode (androguard) =="
/opt/retools/bin/androguard axml ex/AndroidManifest.xml 2>/dev/null > manifest.xml
wc -l manifest.xml
echo "--- package ---"; grep -oE 'package="[^"]*"' manifest.xml | head -3
echo "--- permissions ---"; grep -oE 'uses-permission[^>]*name="[^"]*"' manifest.xml 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:27Z



### 🤖 Asystent — 2026-08-16T02:03:51Z

Kluczowe: **DEX-y są czytelne (dexlib 2.x, brak packera w DEX), ale `AndroidManifest.xml` jest zaszyfrowany** (metoda 4899 + encrypted) — to celowa anty-analiza. Analizuję same DEX-y: wyciągam IoC, pakiety i stringi.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:51Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox2/ex\ncat classes*.dex > /tmp/alldex.bin\necho \"== size ==\"; ls -la /tmp/alldex.bin\necho \"== IPs ==\"; strings -n 5 /tmp/alldex.bin | grep -oE '([0-9]{1,3}\\\\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn | head -25\necho \"== URLs (http) ==\"; strings -n 5 /tmp/alldex.bin | grep -oE 'https?://[a-zA-Z0-9./_?=&:%-]+' | sort -u | head -40\necho \"== package-like strings (com.*) ==\"; strings -n 6 /tmp/alldex.bin | grep -oE '[a-z]+\\\\.([a-z0-9]+\\\\.)+[a-z]+' | grep -iE 'nmz|vnc|rat|socket|panel|bot|main|admin|app
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:52Z

bash: 
cd /root/malware-lab/albiriox2/ex
cat classes*.dex > /tmp/alldex.bin
echo "== size =="; ls -la /tmp/alldex.bin
echo "== IPs =="; strings -n 5 /tmp/alldex.bin | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn | head -25
echo "== URLs (http) =="; strings -n 5 /tmp/alldex.bin | grep -oE 'https?://[a-zA-Z0-9./_?=&:%-]+' | sort -u | head -40
echo "== package-like strings (com.*) =="; strings -n 6 /tmp/alldex.bin | grep -oE '[a-z]+\.([a-z0-9]+\.)+[a-z]+' | grep -iE 'nmz|vnc|rat|socket|panel|bot|main|admin|app|core|service' | sort -u | head -40
echo "== keyword counts =="
fo
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:03:52Z



### 🛠️ Akcja/narzędzie — 2026-08-16T02:04:12Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/albiriox2/ex\necho \"== type descriptors (L...;) top namespaces ==\"\nstrings -n 3 /tmp/alldex.bin | grep -oE 'L[a-z0-9_/]+;' | awk -F/ '{print $2}' | sort | uniq -c | sort -rn | head -25\necho\necho \"== key framework/attack markers ==\"\nfor m in AccessibilityService accessibility BIND_ACCESSIBILITY SYSTEM_ALERT_WINDOW DeviceAdmin VpnService MediaProjection notify Socket ServerSocket nmz joymiweb albiriox Albiriox vnc Vnc VNC; do\n  c=$(strings -n 3 /tmp/alldex.bin | grep -c \"$m\" 2>/dev/null)\n  [ \"$c\" -gt 0 ] && ech
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:04:13Z

bash: 
cd /root/malware-lab/albiriox2/ex
echo "== type descriptors (L...;) top namespaces =="
strings -n 3 /tmp/alldex.bin | grep -oE 'L[a-z0-9_/]+;' | awk -F/ '{print $2}' | sort | uniq -c | sort -rn | head -25
echo
echo "== key framework/attack markers =="
for m in AccessibilityService accessibility BIND_ACCESSIBILITY SYSTEM_ALERT_WINDOW DeviceAdmin VpnService MediaProjection notify Socket ServerSocket nmz joymiweb albiriox Albiriox vnc Vnc VNC; do
  c=$(strings -n 3 /tmp/alldex.bin | grep -c "$m" 2>/dev/null)
  [ "$c" -gt 0 ] && echo "  $m: $c"
done
echo
echo "== joymiweb / localhost contex
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:04:13Z



### 🤖 Asystent — 2026-08-16T02:04:32Z

Ważne ustalenie: `3269a0…` (dexopt.sssgf.apk) to **błędnie otagowana próbka** — to apka społecznościowa „joymi" (`com.joymi.seven.*`, voice-chat/room, SudGIP SDK), **nie Albiriox**. Prawdziwy Albiriox jest w pełni opakowany (0d.apk). Sprawdzam teraz ClayRat (realny, analizowalny dropper).

### 🛠️ Akcja/narzędzie — 2026-08-16T02:04:32Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/clayrat_videodtp\nAPK=$(find . -name '*.apk' | head -1)\necho \"== apkid ==\"\n/opt/retools/bin/apkid \"$APK\" 2>&1 | grep -viE 'Exception|Traceback|File |self\\.|raise |^  |^$' | head -30\necho\necho \"== extract ==\"\nrm -rf ex && mkdir ex && unzip -o -q \"$APK\" -d ex 2>&1 | tail -3\nls -la ex/ | grep -E 'classes|Manifest|resources.arsc|lib'\necho \"== manifest extractable? ==\"\nls -la ex/AndroidManifest.xml 2>&1\necho \"== dex strings: IoCs ==\"\nstrings -n 5 ex/classes.dex 2>/dev/null | grep -oE '([0-9]{1,3}\\\\.){3}
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:04:33Z

bash: 
cd /root/malware-lab/clayrat_videodtp
APK=$(find . -name '*.apk' | head -1)
echo "== apkid =="
/opt/retools/bin/apkid "$APK" 2>&1 | grep -viE 'Exception|Traceback|File |self.|raise |^  |^$' | head -30
echo
echo "== extract =="
rm -rf ex && mkdir ex && unzip -o -q "$APK" -d ex 2>&1 | tail -3
ls -la ex/ | grep -E 'classes|Manifest|resources.arsc|lib'
echo "== manifest extractable? =="
ls -la ex/AndroidManifest.xml 2>&1
echo "== dex strings: IoCs =="
strings -n 5 ex/classes.dex 2>/dev/null | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn | head -15
echo "-- URLs --"; st
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:04:33Z



### 🤖 Asystent — 2026-08-16T02:05:05Z

ClayRat to realny, obfuskowany dropper (klasy jednoliterowe, `AccessibilityService` + overlay + 103× `Socket`) z kandydatem C2 `129.6.55.182`. Dobieram nazwę pakietu (z resources.arsc) i kontekst C2.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:05:05Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/clayrat_videodtp/ex\necho \"== package name (from resources.arsc) ==\"\nstrings -n 4 resources.arsc | grep -oE '^[a-z][a-z0-9]{2,}(\\\\.[a-z0-9_]+){1,}$' | sort -u | head -15\necho\necho \"== C2 IP context (strings around 129.6.55.182) ==\"\nstrings -n 4 classes.dex | grep -nE '129\\\\.6\\\\.55|212\\\\.209\\\\.220|139\\\\.10\\\\.134' \necho\necho \"== ports / socket config strings ==\"\nstrings -n 4 classes.dex | grep -iE 'port|:[0-9]{2,5}|/api|/index|/gate|/panel|websocket|wss|tcp' | sort -u | head -30\necho\necho \"== py
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:05:05Z

bash: 
cd /root/malware-lab/clayrat_videodtp/ex
echo "== package name (from resources.arsc) =="
strings -n 4 resources.arsc | grep -oE '^[a-z][a-z0-9]{2,}(\.[a-z0-9_]+){1,}$' | sort -u | head -15
echo
echo "== C2 IP context (strings around 129.6.55.182) =="
strings -n 4 classes.dex | grep -nE '129\.6\.55|212\.209\.220|139\.10\.134' 
echo
echo "== ports / socket config strings =="
strings -n 4 classes.dex | grep -iE 'port|:[0-9]{2,5}|/api|/index|/gate|/panel|websocket|wss|tcp' | sort -u | head -30
echo
echo "== python: inspect manifest zip entry =="
python3 - <<'PY'
import zipfile
apk = "/root/
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:05:05Z



### 🛠️ Akcja/narzędzie — 2026-08-16T02:05:45Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/clayrat_videodtp/ex\necho \"== package name (UTF-16 strings in resources.arsc) ==\"\nstrings -e l resources.arsc 2>/dev/null | grep -iE '^[a-z][a-z0-9]*(\\\\.[a-z0-9_]+)+$' | sort -u | head -20\necho \"== package via androguard arsc ==\"\n/opt/retools/bin/androguard arsc resources.arsc 2>/dev/null | grep -iE 'package|com\\\\.' | head -20\necho \"== dex: Application/Activity class names (type desc) ==\"\nstrings -n 3 classes.dex | grep -oE 'L[a-z][a-z0-9]*/(MainActivity|App|Application|MyApp|StartActivity|Boot|Receiver|Serv
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:05:46Z

bash: 
cd /root/malware-lab/clayrat_videodtp/ex
echo "== package name (UTF-16 strings in resources.arsc) =="
strings -e l resources.arsc 2>/dev/null | grep -iE '^[a-z][a-z0-9]*(\.[a-z0-9_]+)+$' | sort -u | head -20
echo "== package via androguard arsc =="
/opt/retools/bin/androguard arsc resources.arsc 2>/dev/null | grep -iE 'package|com\.' | head -20
echo "== dex: Application/Activity class names (type desc) =="
strings -n 3 classes.dex | grep -oE 'L[a-z][a-z0-9]*/(MainActivity|App|Application|MyApp|StartActivity|Boot|Receiver|Service)[a-zA-Z0-9]*;' | sort -u | head -30


### 🛠️ Akcja/narzędzie — 2026-08-16T02:05:46Z



### 🤖 Asystent — 2026-08-16T02:06:27Z

Znalazłem pakiet ClayRat: **`io.system.system903`**. Mam komplet wyników RE. Zapisuję wszystko do Obsidianu (karty + dziennik + changelog).

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

tool: run_code
{"code": "const albRe = [\n'',\n'## Static RE — 2026-08-16',\n'',\n'**Próbka:** `8703ee86…` (0d.apk, MB first-seen 2026-07-22). Pobrana z MalwareBazaar, hash zweryfikowany. Host `vserver959630`; kopie w `/root/malware-lab/` (poza vaultem i git).',\n'',\n'- **Pełny packer** — wszystkie 1005 wpisów ZIP = ZipCrypto (`Encrypted = +`): `classes.dex`, `AndroidManifest.xml`, `resources.arsc` niedostępne bez klucza.',\n'- Manifest: podrobiona metoda kompresji **24753** (łamie unzip/Info-ZIP) — anty-analiza.',\n'- ~1000 plików-dekójek: fałszywe konfigi aws/firebase/knox/azure/samsung + losowe assety (.
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z

bash: todo_write

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:27Z



### 🤖 Asystent — 2026-08-16T02:06:32Z

Karty i changelog zapisane. Dziennik wymaga ponownego odczytu (plik się zmienił). Poprawiam.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:32Z

tool: run_code
{"code": "const r = await tools.read({ file_path: \"Daily/2026-08-16.md\", offset: 60, limit: 60 });\nconsole.log(\"tail:\");\nfor (const l of r.lines) console.log(l.text);\nreturn \"ok\";", "description": "Re-read daily note tail"}

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:32Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:32Z



### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:44Z

tool: run_code
{"code": "const daily = [\n'',\n'',\n'## Mobile RE — Albiriox + ClayRat (2026-08-16T02:10:00Z)',\n'',\n'Pobrano realne APK z MalwareBazaar (klucz `~/.mb_api_key`) i zrobiono statyczny RE. Kopie w `/root/malware-lab/` (poza vaultem/git).',\n'',\n'- **Albiriox** `8703ee86…` (0d.apk): cały APK = ZipCrypto (1005 wpisów encrypted), manifest z podrobioną metodą kompresji 24753, ~1000 dekójek, `META-INF/services` obfuskowane. Bez klucza z droppera PENNY statyka niemożliwa.',\n'- **Albiriox** `3269a011…` (dexopt.sssgf.apk): mis-tag — to apka „joymi\" (com.joymi.seven), nie Albiriox.',\n'- **ClayRat** 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:44Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:06:44Z



### 🤖 Asystent — 2026-08-16T02:07:05Z

Reverse engineering wykonany i **wszystko zapisane w Obsidianie**. Oto co realnie zrobiłem:

## Pobrałem prawdziwe, aktualne próbki (MalwareBazaar, klucz `~/.mb_api_key`)
| Próbka | Hash (zweryfikowany) | Co to |
|--------|----------------------|-------|
| Albiriox `0d.apk` | `8703ee86…` ✓ | payload (first-seen 2026-07-22) |
| Albiriox `dexopt.sssgf.apk` | `3269a011…` ✓ | okazał się mis-tagiem |
| ClayRat `Video_DTP.apk` | `78878d33…` ✓ | dropper (first-seen 2026-03-24) |
| ClayRat `YoutubeUltra.apk` | `b08e5a84…` ✓ | pobrany |

Kopie trzymam w `/root/malware-lab/` (**poza vaultem i git** — dobra praktyka OPSEC).

## Wyniki statycznego RE

**Albiriox (`8703ee86…`)** — potwierdza raport Cleafy:
- Cały APK = **ZipCrypto** (wszystkie 1005 wpisów `Encrypted = +`, w tym `classes.dex` i manifest).
- Manifest z **podrobioną metodą kompresji 24753** (łamie unzip/Info-ZIP).
- ~1000 plików-dekójek (fałszywe konfigi aws/firebase/knox/azure/samsung + losowe assety), obfuskacja `META-INF/services`.
- Wniosek: to **JSONPacker/Golden Crypt** — bez klucza z droppera PENNY (`com.example.myapplication`) statyka payloadu jest niemożliwa.

**ClayRat (`78878d33…`)** — realny, analizowalny dropper:
- **Pakiet: `io.system.system903`** (z resources.arsc).
- Manifest **ZipCrypto** (anty-analiza), DEX czytelny, klasy jednoliterowe (R8/ProGuard, apkid → dexlib 2.x).
- Markery ataku: `AccessibilityService` + overlay (7×) + `Socket` 103× / `ServerSocket` 11×.
- SIP (JAIN-SIP) + WebSocket w kodzie — ale stringi SIP (`mranga@…`, `sip:0440@…`) to **biblioteczny szum, nie C2** (ważny false-positive, którego uniknąłem).

**Ważne ustalenie taktyczne:** druga próbka z MB (`3269a011…`) to **błędny tag** — to apka społecznościowa „joymi" (`com.joymi.seven.*`), nie Albiriox. Tagi MalwareBazaar potrafią kłamać.

## Zapisane w vaultcie
- `Analizy/Malware/Albiriox_Android_RAT.md` — status `in_progress` + sekcja „Static RE"
- `Analizy/Malware/ClayRat_Android_RAT.md` — status `in_progress` + sekcja „Static RE" (pakiet, obfuskacja, IoC)
- `Daily/2026-08-16.md` + `Wiedza/Aktualizacje.md` — wpisy sesji
- Narzędzia: venv `/opt/retools` (apkid + androguard) — gotowe do dalszych analiz

## Co dalej (proponuję)
1. **jadx na ClayRat** — pełna dekompilacja do Java, doprecyzowanie realnego C2 (WebSocket endpoint) i pakietu.
2. **Odzyskać klucz Albiriox** z droppera PENNY, żeby rozpakować payload.
3. Albo ściągnąć **RatOn** (masz hashe) i zrobić analogiczną statykę.

Który kierunek? (Domyślnie: dorzucę jadx i dokończę ClayRat-a do czytelnej Javy.)

### 🤖 Asystent — 2026-08-16T02:07:20Z

Jasne — sprawdzam, że cała sesja RE jest trwale zapisana w vaultcie (pliki + git).

### 🛠️ Akcja/narzędzie — 2026-08-16T02:07:20Z

tool: run_code
{"code": "// Verify saved RE content + git state\nconst v = await tools.bash({ command: `\ncd /root/obsidian-vault\necho \"== karty z RE (grep Static RE) ==\"\ngrep -l \"Static RE\" Analizy/Malware/*.md 2>/dev/null\necho \"== RE wpis w Daily ==\"\ngrep -c \"Mobile RE — Albiriox\" Daily/2026-08-16.md\necho \"== RE wpis w Aktualizacje ==\"\ngrep -c \"Static RE (MalwareBazaar\" Wiedza/Aktualizacje.md\necho \"== nowe notatki z tej sesji (mobile) ==\"\nls -la Wiedza/Zrodla_Mobile_Malware.md Wiedza/Malware/Mobile_Malware_2024_2025.md Lab/Android_RE_i_Dynamiczna_Analiza.md 2>&1\necho \"== git status 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:07:20Z

bash: 
cd /root/obsidian-vault
echo "== karty z RE (grep Static RE) =="
grep -l "Static RE" Analizy/Malware/*.md 2>/dev/null
echo "== RE wpis w Daily =="
grep -c "Mobile RE — Albiriox" Daily/2026-08-16.md
echo "== RE wpis w Aktualizacje =="
grep -c "Static RE (MalwareBazaar" Wiedza/Aktualizacje.md
echo "== nowe notatki z tej sesji (mobile) =="
ls -la Wiedza/Zrodla_Mobile_Malware.md Wiedza/Malware/Mobile_Malware_2024_2025.md Lab/Android_RE_i_Dynamiczna_Analiza.md 2>&1
echo "== git status (skrót) =="
git status --short | head -30
echo "== git last commit =="
git log --oneline -3 2>/dev/null


### 🛠️ Akcja/narzędzie — 2026-08-16T02:07:20Z



### 🤖 Asystent — 2026-08-16T02:07:41Z

Wszystko jest zapisane w vaultcie (pliki na dysku + git). Zrobię jeszcze commit, żeby zmiany były trwale utrwalone w repozytorium (auto-sync obsidian-git i tak robi to co 15 min, ale domknę od razu).

### 🛠️ Akcja/narzędzie — 2026-08-16T02:07:41Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/obsidian-vault\ngit add -A\ngit commit -m \"Mobile malware: bazy + krajobraz 2024-25 + plan RE + karty próbek + static RE (Albiriox packer, ClayRat io.system.system903)\" 2>&1 | tail -8\necho \"== after commit ==\"\ngit status --short | head -10\ngit log --oneline -2\n`, description: \"Commit all vault changes to git\" });\nconsole.log(r.kind === \"foreground\" ? r.stdout.text : String(r));\nreturn \"ok\";", "description": "Commit vault changes to git"}

### 🛠️ Akcja/narzędzie — 2026-08-16T02:07:41Z

bash: 
cd /root/obsidian-vault
git add -A
git commit -m "Mobile malware: bazy + krajobraz 2024-25 + plan RE + karty próbek + static RE (Albiriox packer, ClayRat io.system.system903)" 2>&1 | tail -8
echo "== after commit =="
git status --short | head -10
git log --oneline -2


### 🛠️ Akcja/narzędzie — 2026-08-16T02:07:41Z



### 🤖 Asystent — 2026-08-16T02:07:49Z

Wszystko zapisane i utrwalone. Stan na teraz:

## Zapisane w Obsidianie (vault `/root/obsidian-vault/`)
**Nowe notatki:**
- `Wiedza/Zrodla_Mobile_Malware.md` — analiza baz malware mobilnego
- `Wiedza/Malware/Mobile_Malware_2024_2025.md` — aktywne rodziny 2024–2025
- `Lab/Android_RE_i_Dynamiczna_Analiza.md` — plan RE + analizy dynamicznej

**Karty próbek w `Analizy/Malware/`:**
- `Albiriox_Android_RAT.md` — `status: in_progress`, sekcja „Static RE" (pełny ZipCrypto packer)
- `ClayRat_Android_RAT.md` — `status: in_progress`, sekcja „Static RE" (pakiet `io.system.system903`, Accessibility+overlay+Socket)
- `RatOn_Android_banker.md`, `DroidBot_Android_RAT.md`, `Frogblight_Android_banker.md`

**Logi/indeksy:**
- `Daily/2026-08-16.md` — wpis sesji RE
- `Wiedza/Aktualizacje.md` — dziennik zmian
- `Analizy/Threat_Intel_MOC.md` — sekcja „Mobile (Android) 2024–2025"

## Git — utrwalone
Commit `055a966` (7 plików, +133/−63) — wszystko z tej sesji jest teraz trwale w repozytorium. Auto-sync obsidian-git będzie dalej commitować co 15 min.

## Świadomie POZA vaultem (bezpieczeństwo)
Same próbki malware (`/root/malware-lab/`) — nie trafiają do gita/vaultu, żeby nie commitować złośliwych binarek. Ich lokalizacja jest odnotowana w kartach.

Od teraz każdy kolejny krok RE/analizy **od razu ląduje w vaultcie** + commit. Chcesz, żebym dorzucił `jadx` i dokończył ClayRat-a do czytelnej Javy (pełna dekompilacja + realny C2), czy najpierw coś innego?

### 🤖 Asystent — 2026-08-16T02:10:11Z

Kontynuuję — dokańczam ClayRat-a: instaluję `jadx`, dekompiluję do Javy i wyciągam realny C2 + strukturę.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:11Z

tool: run_code
{"code": "await tools.todo_write({ todos: [\n  { content: \"Install jadx\", status: \"in_progress\" },\n  { content: \"Decompile ClayRat classes.dex to Java\", status: \"pending\" },\n  { content: \"Extract real C2 + command handlers + package from Java\", status: \"pending\" },\n  { content: \"Write decompiled findings to Obsidian\", status: \"pending\" },\n]});\n\nconst r = await tools.bash({ command: `\nset -e\necho \"== resolve latest jadx ==\"\nTAG=$(curl -sL --max-time 30 https://api.github.com/repos/skylot/jadx/releases/latest | grep -oE '\"tag_name\" *: *\"v[0-9.]+\"' | grep -oE 'v[0-9
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:11Z



### 🤖 Asystent — 2026-08-16T02:10:25Z

Błąd składni (bash `$TAG#v` kolidował z template literalem TS). Poprawiam — unikam `${...}` w bashu.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:25Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\nset -e\necho \"== resolve latest jadx ==\"\nTAG=$(curl -sL --max-time 30 https://api.github.com/repos/skylot/jadx/releases/latest | grep -oE '\"tag_name\" *: *\"v[0-9.]+\"' | grep -oE 'v[0-9.]+' | head -1)\necho \"TAG=$TAG\"\n[ -z \"$TAG\" ] && TAG=\"v1.5.1\"\nVER=$(echo \"$TAG\" | sed 's/^v//')\nURL=\"https://github.com/skylot/jadx/releases/download/$TAG/jadx-$VER.zip\"\necho \"URL=$URL\"\ncurl -sL --max-time 120 \"$URL\" -o /tmp/jadx.zip\nls -la /tmp/jadx.zip\nrm -rf /opt/jadx && mkdir -p /opt/jadx\nunzip -q /tmp/jadx.zip -d /opt/jadx\necho 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:27Z

bash: 
set -e
echo "== resolve latest jadx =="
TAG=$(curl -sL --max-time 30 https://api.github.com/repos/skylot/jadx/releases/latest | grep -oE '"tag_name" *: *"v[0-9.]+"' | grep -oE 'v[0-9.]+' | head -1)
echo "TAG=$TAG"
[ -z "$TAG" ] && TAG="v1.5.1"
VER=$(echo "$TAG" | sed 's/^v//')
URL="https://github.com/skylot/jadx/releases/download/$TAG/jadx-$VER.zip"
echo "URL=$URL"
curl -sL --max-time 120 "$URL" -o /tmp/jadx.zip
ls -la /tmp/jadx.zip
rm -rf /opt/jadx && mkdir -p /opt/jadx
unzip -q /tmp/jadx.zip -d /opt/jadx
echo "== jadx version =="
/opt/jadx/bin/jadx --version 2>&1 | head -3


### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:27Z



### 🤖 Asystent — 2026-08-16T02:10:37Z

jadx 1.5.6 gotowy. Dekompiluję ClayRat i wyciągam C2 + strukturę.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:37Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/clayrat_videodtp\nrm -rf jadx_out && mkdir -p jadx_out\necho \"== decompiling classes.dex (jadx) ==\"\n/opt/jadx/bin/jadx -q -d jadx_out ex/classes.dex 2>&1 | tail -5\necho \"== java files count ==\"\nfind jadx_out -name '*.java' | wc -l\necho \"== top source packages ==\"\nfind jadx_out/sources -maxdepth 4 -type d 2>/dev/null | sed 's|jadx_out/sources/||' | sort | head -40\n`, description: \"Decompile ClayRat dex with jadx\" });\nconsole.log(r.kind === \"foreground\" ? r.stdout.text : String(r));\nreturn \"ok\";", "descri
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:52Z

bash: 
cd /root/malware-lab/clayrat_videodtp
rm -rf jadx_out && mkdir -p jadx_out
echo "== decompiling classes.dex (jadx) =="
/opt/jadx/bin/jadx -q -d jadx_out ex/classes.dex 2>&1 | tail -5
echo "== java files count =="
find jadx_out -name '*.java' | wc -l
echo "== top source packages =="
find jadx_out/sources -maxdepth 4 -type d 2>/dev/null | sed 's|jadx_out/sources/||' | sort | head -40


### 🛠️ Akcja/narzędzie — 2026-08-16T02:10:52Z



### 🤖 Asystent — 2026-08-16T02:11:08Z

4977 plików Java — silna obfuskacja (DEXGuard-style, pakiety jednoliterowe + losowe sufiksy `GOjW`). Wyciągam C2, pakiety i handlery komend.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:11:08Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/clayrat_videodtp/jadx_out/sources\necho \"== package name (BuildConfig / applicationId) ==\"\ngrep -rhoE 'io\\\\.system\\\\.system903|\"[a-z][a-z0-9]+\\\\.[a-z0-9]+\\\\.[a-z0-9]+\"' --include=*.java . 2>/dev/null | sort -u | head -20\necho\necho \"== domains (string constants) ==\"\ngrep -rhoE '\"[a-z0-9.-]+\\\\.(com|net|io|ru|xyz|top|cyou|online|site|app|gg|click|link|space|monster|life|store|shop|org|me|tv)\"' --include=*.java . 2>/dev/null | tr -d '\"' | sort | uniq -c | sort -rn | head -30\necho\necho \"== IPs (dedup) 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:11:08Z

bash: 
cd /root/malware-lab/clayrat_videodtp/jadx_out/sources
echo "== package name (BuildConfig / applicationId) =="
grep -rhoE 'io\.system\.system903|"[a-z][a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+"' --include=*.java . 2>/dev/null | sort -u | head -20
echo
echo "== domains (string constants) =="
grep -rhoE '"[a-z0-9.-]+\.(com|net|io|ru|xyz|top|cyou|online|site|app|gg|click|link|space|monster|life|store|shop|org|me|tv)"' --include=*.java . 2>/dev/null | tr -d '"' | sort | uniq -c | sort -rn | head -30
echo
echo "== IPs (dedup) =="
grep -rhoE '([0-9]{1,3}\.){3}[0-9]{1,3}' --include=*.java . 2>/dev/null 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:11:08Z



### 🛠️ Akcja/narzędzie — 2026-08-16T02:11:34Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\ncd /root/malware-lab/clayrat_videodtp/jadx_out/sources\necho \"== AccessibilityService classes ==\"\ngrep -rl \"extends AccessibilityService\" --include=*.java . 2>/dev/null\necho\necho \"== socket connect targets (host/port) ==\"\ngrep -rnE 'InetSocketAddress|\\.connect\\(|new Socket\\(' --include=*.java . 2>/dev/null | grep -oE '\"[0-9a-zA-Z.:/-]+\"|[0-9]{1,3}\\\\.[0-9]{1,3}\\\\.[0-9]{1,3}\\\\.[0-9]{1,3}|:[0-9]{2,5}' | sort | uniq -c | sort -rn | head -25\necho\necho \"== grok / xai context ==\"\ngrep -rl \"grok\\|x\\.ai\\|xai\\|Grok\" --inc
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:11:34Z

bash: 
cd /root/malware-lab/clayrat_videodtp/jadx_out/sources
echo "== AccessibilityService classes =="
grep -rl "extends AccessibilityService" --include=*.java . 2>/dev/null
echo
echo "== socket connect targets (host/port) =="
grep -rnE 'InetSocketAddress|.connect(|new Socket(' --include=*.java . 2>/dev/null | grep -oE '"[0-9a-zA-Z.:/-]+"|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|:[0-9]{2,5}' | sort | uniq -c | sort -rn | head -25
echo
echo "== grok / xai context =="
grep -rl "grok|x.ai|xai|Grok" --include=*.java . 2>/dev/null | head -8
echo "grok files: $(grep -rl 'grok\|x\.ai\|xai\|Gro
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:11:34Z



### 🤖 Asystent — 2026-08-16T02:12:07Z

Mam pełny obraz. Kluczowy wniosek: **ClayRat to trojanizowany klient Grok (xAI)** — 341 plików Java odnosi się do Grok/x.ai, plus primit'y RAT (Accessibility, overlay, Socket/SIP), a C2 jest szyfrowane (do wydobycia dopiero dynamicznie). Zapisuję finał do Obsidianu.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:07Z

tool: run_code
{"code": "const jadxSec = [\n'',\n'## Decompilacja jadx (2026-08-16)',\n'',\n'`jadx 1.5.6` → **4977 plików Java** (obfuskacja DEXGuard-style: pakiety jednoliterowe + sufiksy `GOjW`, `com.amuvvoafs.*`).',\n'',\n'- **To trojanizowany klient Grok (xAI)**: 341 plików odnosi się do Grok/x.ai (`openSuperGrok`, `setImagineAutoGenerateVideo`, `video_generation_`, subskrypcje). Lure = „darmowy asystent AI\" / `Video_DTP.apk`.',\n'- **Primit\\'y RAT**: `AccessibilityService`, `WindowManager`/overlay (11 plików), `Socket` (38) / `ServerSocket` (8) / `InetSocketAddress` (7), SIP (JAIN-SIP) + WebSocket.',\
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:07Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:07Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:07Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:07Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:07Z

bash: todo_write

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:07Z



### 🤖 Asystent — 2026-08-16T02:12:13Z

Dziennik znowu zmienił się w tle (parallelny proces dopisuje). Doczytuję aktualny koniec i dopisuję.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:13Z

tool: run_code
{"code": "const d = await tools.read({ file_path: \"Daily/2026-08-16.md\", offset: 90 });\nconsole.log(\"total lines:\", d.totalLines);\nfor (const l of d.lines) console.log(repr(l.text));\nfunction repr(s){ return JSON.stringify(s); }\nreturn \"ok\";", "description": "Read current tail of daily note"}

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:13Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:13Z



### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:22Z

tool: run_code
{"code": "const daily = [\n'',\n'## ClayRat — dekompilacja jadx (2026-08-16T02:20:00Z)',\n'',\n'- jadx 1.5.6 → 4977 plików Java (obfuskacja DEXGuard-style: `com.amuvvoafs.*`, pakiety jednoliterowe + sufiksy `GOjW`).',\n'- **ClayRat = trojanizowany klient Grok (xAI)** (341 plików grok/x.ai) + primit\\'y RAT: AccessibilityService, overlay (11), Socket (38)/ServerSocket (8), SIP+WebSocket.',\n'- C2 szyfrowane (brak jawnego IP/domeny); IP z strings = szum SIP. Realny C2 → dynamika (Frida).',\n'- Wyniki: [[ClayRat_Android_RAT]]. Narzędzie: jadx w `/opt/jadx`.',\n].join('\\n');\n\ntry {\n  await too
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:22Z

bash: edit

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:22Z

bash: cd /root/obsidian-vault && git add -A && git commit -m "ClayRat: jadx dekompilacja (trojany Grok/xAI + primity RAT, C2 szyfrowane)" 2>&1 | tail -4

### 🛠️ Akcja/narzędzie — 2026-08-16T02:12:22Z



### 🤖 Asystent — 2026-08-16T02:12:33Z

Zrobione — ClayRat dokończony, wszystko zapisane i zcommitowane (`ee0f480`).

## Finał reverse engineeringu ClayRat (`78878d33…`, Video_DTP.apk)

**Dekomplilacja (jadx 1.5.6)** → 4977 plików Java, **obfuskacja DEXGuard-style** (pakiety jednoliterowe + losowe sufiksy `GOjW`, `com.amuvvoafs.*`).

**Najważniejsze ustalenie — to trojanizowany klient Grok (xAI):**
- **341 plików Java** odnosi się do Grok/x.ai (`openSuperGrok`, `setImagineAutoGenerateVideo`, `video_generation_`, subskrypcje).
- Lure = „darmowy asystent AI" / `Video_DTP.apk` (ДТП = wypadek drogowy).
- Czyli: malware podszywa się pod aplikację AI, żeby wyłudzić instalację.

**Primit'y RAT (złośliwa warstwa):**
- `AccessibilityService` (2 odniesienia), `WindowManager`/overlay (11 plików)
- `Socket` (38) / `ServerSocket` (8) / `InetSocketAddress` (7)
- SIP (JAIN-SIP) + WebSocket

**C2:** brak jawnego IP/domeny w kodzie — **stringi szyfrowane**. IP-y z `strings` (129.6.55.182 itd.) to **szum biblioteki SIP** (`mranga@…`), nie C2. Realny endpoint do wydobycia dopiero **dynamicznie** (Frida: hook na `Socket.connect` + odszyfrowanie stringów).

## Pełny stan RE obu rodzin
| Rodzina | Wynik statyki | Co dalej |
|---------|--------------|----------|
| **Albiriox** `8703ee86…` | pełny ZipCrypto packer (nie do rozpakowania statycznie) | odzyskać klucz z droppera PENNY |
| **ClayRat** `78878d33…` | trojanizowany Grok + primit'y RAT, C2 szyfrowane | dynamika (Frida) |

## Zapisane w Obsidianie
- `Analizy/Malware/ClayRat_Android_RAT.md` — sekcja „Decompilacja jadx" (trojany Grok, obfuskacja, C2)
- `Analizy/Malware/Albiriox_Android_RAT.md` — sekcja „Static RE" (packer)
- `Daily/2026-08-16.md` + `Wiedza/Aktualizacje.md` — wpisy
- Commit `ee0f480` (7 plików, +195)

## Narzędzia gotowe do dalszych analiz
- `/opt/retools` (venv: apkid + androguard)
- `/opt/jadx` (jadx 1.5.6)
- Próbki: `/root/malware-lab/` (poza vaultem)

Naturalny kolejny krok to **analiza dynamiczna** (emulator + Frida) — ale to wymaga wyboru emulatora i większej izolacji, co zapisałem w `Lab/Android_RE_i_Dynamiczna_Analiza.md`. Chcesz, żebym teraz rozpisał konkretny plan dynamicznej analizy ClayRat-a (Frida + hook na Socket/string-decrypt), czy na tym kończymy statykę?

### 🤖 Asystent — 2026-08-16T02:15:34Z

Analiza dynamiczna wymaga emulatora/urządzenia + Frida. Najpierw sprawdzam, co ten host realnie umożliwia (KVM, dysk, narzędzia) — od tego zależy, czy odpalę malware lokalnie, czy zrobię to przez sandbox publiczny.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:15:34Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\necho \"== KVM (kluczowe dla emulatora) ==\"\nls -la /dev/kvm 2>&1 || echo \"BRAK /dev/kvm\"\ngrep -cE 'vmx|svm' /proc/cpuinfo 2>/dev/null || echo 0\necho \"== dysk ==\"; df -h / | tail -1\necho \"== RAM ==\"; free -h | head -2\necho \"== android/docker/emulator tooling ==\"\nfor t in sdkmanager avdmanager emulator adb docker waydroid frida frida-server qemu-system-x86_64; do printf \"%-20s \" \"$t\"; command -v \"$t\" >/dev/null 2>&1 && echo \"$(command -v $t)\" || echo MISSING; done\necho \"== frida pip ==\"; python3 -c \"import frida; print(
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:15:34Z

bash: 
echo "== KVM (kluczowe dla emulatora) =="
ls -la /dev/kvm 2>&1 || echo "BRAK /dev/kvm"
grep -cE 'vmx|svm' /proc/cpuinfo 2>/dev/null || echo 0
echo "== dysk =="; df -h / | tail -1
echo "== RAM =="; free -h | head -2
echo "== android/docker/emulator tooling =="
for t in sdkmanager avdmanager emulator adb docker waydroid frida frida-server qemu-system-x86_64; do printf "%-20s " "$t"; command -v "$t" >/dev/null 2>&1 && echo "$(command -v $t)" || echo MISSING; done
echo "== frida pip =="; python3 -c "import frida; print('frida', frida.__version__)" 2>&1 | head -1
echo "== cpu/kernel (nested 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:15:34Z



### 🤖 Asystent — 2026-08-16T02:16:13Z

KVM jest (nested), ale **dysk tylko 4.1 GB** (ryzyko dla vaultu), brak SDK/emulatora/Fridy. Robię dynamiczną analizę dwutorowo: (1) publiczne raporty behawioralne Tria.ge dla naszych hashy + (2) ustawiam Frida. Sprawdzam najpierw, co dają sandboxy.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:13Z

tool: run_code
{"code": "// kick off frida-tools install in background\nconst fr = await tools.bash({ command: \"pip3 install --break-system-packages --quiet --no-warn-script-location frida-tools 2>&1 | tail -4; echo FRIDA_DONE\", description: \"Install frida-tools\", run_in_background: true });\nconsole.log(\"frida job:\", fr.kind === \"background\" ? fr.jobId : JSON.stringify(fr));\n\nconst hashes = [\n  [\"ClayRat\", \"78878d33b2b48747694ce2fdb24e896cd9ba027b1d66c66c107cf415ed46b89b\"],\n  [\"Albiriox\", \"8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e\"],\n  [\"Albiriox2\", \"3269a0116c
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:13Z

bash: pip3 install --break-system-packages --quiet --no-warn-script-location frida-tools 2>&1 | tail -4; echo FRIDA_DONE

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:13Z

bash: curl -sL --max-time 30 "https://tria.ge/api/v0/search?query=sha256:78878d33b2b48747694ce2fdb24e896cd9ba027b1d66c66c107cf415ed46b89b&limit=5" | head -c 1200

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:14Z

bash: curl -sL --max-time 30 "https://tria.ge/api/v0/search?query=sha256:8703ee8685a47d4085b737b29aaa0f6f7898985b41963bd15d7027c75a609a3e&limit=5" | head -c 1200

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:14Z

bash: curl -sL --max-time 30 "https://tria.ge/api/v0/search?query=sha256:3269a0116ce0915afdd32e8d87b05ae9f5c00fcf0a6729add39a6a87aaf30089&limit=5" | head -c 1200

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:14Z

bash: curl -sL --max-time 30 "https://tria.ge/api/v0/search?query=sha256:bf82609c55304c468996244d3ecc16348d9bea0891482ca724ffefcfaded8b66&limit=5" | head -c 1200

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:14Z



### 🤖 Asystent — 2026-08-16T02:16:34Z

Tria.ge wymaga klucza API (nie mam). KVM jest, więc spróbuję **lokalnego emulatora + Frida**. Najpierw muszę zwolnić dysk (4.1 GB to za mało). Sprawdzam, co zajmuje miejsce i czyszczę.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:34Z

tool: run_code
{"code": "const r = await tools.bash({ command: `\necho \"== wszystkie monty ==\"; df -h | grep -vE 'tmpfs|udev|overlay' \necho \"== najwięksi zjadacze (top) ==\"; du -x -h -d1 / 2>/dev/null | sort -rh | head -15\necho \"== docker ==\"; docker system df 2>/dev/null || echo \"docker niedostępny\"\necho \"== apt cache ==\"; du -sh /var/cache/apt 2>/dev/null\necho \"== /tmp duże pliki ==\"; ls -la /tmp/*.zip /tmp/*.bin 2>/dev/null | head\necho \"== /opt ==\"; du -sh /opt/* 2>/dev/null\n`, description: \"Investigate disk usage\" });\nconsole.log(r.kind === \"foreground\" ? r.stdout.text : String(r
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:44Z

bash: 
echo "== wszystkie monty =="; df -h | grep -vE 'tmpfs|udev|overlay' 
echo "== najwięksi zjadacze (top) =="; du -x -h -d1 / 2>/dev/null | sort -rh | head -15
echo "== docker =="; docker system df 2>/dev/null || echo "docker niedostępny"
echo "== apt cache =="; du -sh /var/cache/apt 2>/dev/null
echo "== /tmp duże pliki =="; ls -la /tmp/*.zip /tmp/*.bin 2>/dev/null | head
echo "== /opt =="; du -sh /opt/* 2>/dev/null


### 🛠️ Akcja/narzędzie — 2026-08-16T02:16:44Z



### 🤖 Asystent — 2026-08-16T02:17:31Z

Zanim postawię emulator — kluczowy test: sprawdzam, czy "szyfrowanie" manifestu ClayRat to **prawdziwy ZipCrypto** czy tylko podrobiony bit (trik anty-analiza, który da się odzyskać). To decyduje, czy APK da się w ogóle zainstalować. Równolegle czyszczę dysk.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:17:31Z

tool: run_code
{"code": "// Manifest recoverability test + disk cleanup\nconst t = await tools.bash({ command: `\ncd /root/malware-lab/clayrat_videodtp\nAPK=$(find . -name '*.apk' | head -1)\npython3 - <<PY\nimport zipfile, zlib, struct\napk = \"$APK\"\nz = zipfile.ZipFile(apk)\ninfo = z.getinfo(\"AndroidManifest.xml\")\nwith open(apk,\"rb\") as f:\n    f.seek(info.header_offset)\n    lh = f.read(30)\n    nlen = struct.unpack(\"<H\", lh[26:28])[0]\n    elen = struct.unpack(\"<H\", lh[28:30])[0]\n    data_start = info.header_offset + 30 + nlen + elen\n    f.seek(data_start)\n    raw = f.read(info.compress_siz
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:17:31Z

bash: 
cd /root/malware-lab/clayrat_videodtp
APK=$(find . -name '*.apk' | head -1)
python3 - <<PY
import zipfile, zlib, struct
apk = "$APK"
z = zipfile.ZipFile(apk)
info = z.getinfo("AndroidManifest.xml")
with open(apk,"rb") as f:
    f.seek(info.header_offset)
    lh = f.read(30)
    nlen = struct.unpack("<H", lh[26:28])[0]
    elen = struct.unpack("<H", lh[28:30])[0]
    data_start = info.header_offset + 30 + nlen + elen
    f.seek(data_start)
    raw = f.read(info.compress_size)
print("compress_size", info.compress_size, "flag_bits", hex(info.flag_bits))
for label, data in [("plaintext-defl
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:17:32Z

bash: 
docker builder prune -f 2>/dev/null | tail -2
docker container prune -f 2>/dev/null | tail -2
apt-get clean 2>/dev/null
rm -f /tmp/jadx.zip /tmp/alldex.bin
echo "== free after cleanup =="; df -h / | tail -1


### 🛠️ Akcja/narzędzie — 2026-08-16T02:17:32Z

bash: job_output

### 🛠️ Akcja/narzędzie — 2026-08-16T02:17:32Z



### 🤖 Asystent — 2026-08-16T02:18:02Z

Dobra uwaga — sprawdzę, co mam w Cloudflare (R2/rclone) do zrzucania dużych artefaktów. A przy okazji: w ostatnim kroku odkryłem coś ważnego — **"szyfrowanie" manifestu było FAKE** (podrobiony bit w zipie, dane to zwykły deflate). Odzyskałem manifest! Rozkodowuję go i sprawdzam Cloudflare.

### 🛠️ Akcja/narzędzie — 2026-08-16T02:18:02Z

tool: run_code
{"code": "// 1) Cloudflare config in vault + rclone on host\nfor (const p of [\"Narzedzia/Cloudflare_Konfiguracja.md\", \"Lab/Cloudflare_x-masked.md\"]) {\n  try {\n    const r = await tools.read({ file_path: p, limit: 60 });\n    console.log(\"\\n===== \" + p + \" =====\");\n    for (const l of r.lines) console.log(l.text);\n  } catch (e) { console.log(\"\\nERR read \" + p + \": \" + (e && e.message ? e.message : String(e))); }\n}\n\nconst rc = await tools.bash({ command: `\necho \"== rclone ==\"; command -v rclone && rclone version 2>/dev/null | head -1 || echo \"brak rclone\"\necho \"== rcl
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T02:18:02Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T02:18:02Z

bash: read

### 🛠️ Akcja/narzędzie — 2026-08-16T02:18:02Z

bash: 
echo "== rclone =="; command -v rclone && rclone version 2>/dev/null | head -1 || echo "brak rclone"
echo "== rclone configs =="; ls -la ~/.config/rclone/ 2>/dev/null || echo "(brak ~/.config/rclone)"
echo "== R2 / cloudflare env =="; env | grep -iE 'r2|cloudflare|cf_|bucket|S3|aws' | sed 's/=.*/=<set>/' || echo "(brak env)"
echo "== s3cmd / aws cli =="; command -v aws s3cmd mc 2>/dev/null || echo "brak"


### 🛠️ Akcja/narzędzie — 2026-08-16T02:18:03Z

bash: 
/opt/retools/bin/androguard axml /tmp/manifest_plain.xml.bin 2>/dev/null > /tmp/manifest.xml
echo "== package =="; grep -oE 'package="[^"]*"' /tmp/manifest.xml | head -3
echo "== permissions =="; grep -oE 'android.permission.[A-Z_]+' /tmp/manifest.xml | sort -u
echo "== services =="; grep -oE '<service[^>]*android:name="[^"]*"' /tmp/manifest.xml | head -30
echo "== receivers =="; grep -oE '<receiver[^>]*android:name="[^"]*"' /tmp/manifest.xml | head -15
echo "== activities =="; grep -oE '<activity[^>]*android:name="[^"]*"' /tmp/manifest.xml | head -15


### 🛠️ Akcja/narzędzie — 2026-08-16T02:18:03Z



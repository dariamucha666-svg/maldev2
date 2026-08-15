---
tags: [lab, goose, deepseek, session]
date: 2026-08-15
updated: 2026-08-15
status: active
---

# Goose + DeepSeek na `.133`

Powiązane: [[Lab/Hosts]] · [[Daily/2026-08-15]] · [[Lab/Recap 2026-08-15]] · [[Obsidian_Workflow]]

Agent **Goose** działa **na VPS** `vserver959630` (`5.175.189.133`), model DeepSeek. Okno terminala jest na Kali i trzyma SSH.

Hasła i klucze API **poza** vaultem.

## Stan (2026-08-15 ~09:53 UTC)

| Pole | Wartość |
|------|---------|
| Host | `root@5.175.189.133` (`vserver959630`, Ubuntu 24.04) |
| Binarka | `/root/.local/bin/goose` **1.46.0** |
| Provider | `custom_deepseek` |
| Model | `deepseek-v4-pro` |
| Sesja Goose | `deepseek-vps` (`goose session -n deepseek-vps`) |
| Config | `/root/.config/goose/config.yaml` (`active_provider: custom_deepseek`) |
| Env (klucze) | `/root/.config/goose/deepseek.env` (nie commituj, nie wklejaj tu) |
| Okno na Kali | qterminal → helper `goose-vps-133` |
| Helper | `/home/kali/.local/bin/goose-vps-133` |
| SSH z Kali | klucz `~/.ssh/id_ed25519` (komentarz `kali-goose-vps-133`) w `/root/.ssh/authorized_keys` |

## Jak odpalić znowu (Kali)

```bash
/home/kali/.local/bin/goose-vps-133
# albo
qterminal -w /home/kali -e /home/kali/.local/bin/goose-vps-133
```

Helper robi `ssh -t root@5.175.189.133` i na hoście:

```bash
export PATH=/root/.local/bin:$PATH
set -a && . /root/.config/goose/deepseek.env && set +a
cd /root
goose session -n deepseek-vps --provider custom_deepseek --model deepseek-v4-pro
```

## Zasady

- Goose ma developer tools na `.133` — traktuj sesję jak pracę na tym hoście.
- Każda decyzja / instalacja / werdykt z tej sesji → od razu `Daily/YYYY-MM-DD.md` + w razie potrzeby ta karta.
- Nie wklejać haseł, tokenów DeepSeek, kluczy SSH do vaultu.

## Next

- [ ] Jak Goose skończy zadanie — dopisać werdykt tutaj i do dziennika.
- [ ] Nie trzymać sekretów w `config.yaml` (zostają w `deepseek.env` / `secrets.yaml`).

## Druga sesja (15.08 wieczór)

| Pole | Wartość |
|------|---------|
| Sesja | `deepseek-vps-2` |
| Okno Kali | 🪿 / `Goose DeepSeek — .133 #2` |
| Stara `deepseek-vps` | **zostaje** (osobna historia) |

Nowe okna Goose wczytują haczyk Obsidian (`top_of_mind.md`). Żeby stara sesja też go miała — zamknij i odpal ponownie helper (historia `deepseek-vps` wraca po `-n`).

Logowanie z sesji Goose:

```bash
/root/obsidian-vault/Narzedzia/log_to_obsidian.sh "Goose — temat" "co zrobiono"
```

## Stabilność TUI (2026-08-15 wieczór)

Goose **nie** odpalamy już gołym SSH+TUI w qterminalu — to zapychało bufor (myślenie DeepSeek `max` + dużo tooli) i każda konsola wyglądała jak martwa.

| Co | Jak |
|----|-----|
| Proces | `tmux` na `.133`: `g-deepseek-vps`, `g-deepseek-vps-2`, `g-deepseek-vps-3` |
| Helper Kali | `goose-vps-133` / `-2` / `-3` tylko **attach** |
| Wrapper | `/root/.local/bin/goose-tmux` |
| Myślenie | `GOOSE_THINKING_EFFORT: medium` (było `max`) |
| Limit tur | `GOOSE_MAX_TURNS: 40` + compact 0.6 |

Zamknięcie okna na Kali **nie** zabija Goose. Ponowne odpalenie helpera = powrót do tego samego tmux.

- Detach: `Ctrl-b d`
- Lista: `tmux ls` na `.133`
- Nie wznawiać starej `deepseek-vps` (2000+ wiadomości) — nowa nazwa albo #3.


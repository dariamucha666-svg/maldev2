---
tags: [ioc, chrome, stealer]
sha256: 1b3ceba6a82929b53c72e137e257f7f8924173d8b0de5852253b7437723f153e
updated: 2026-08-15
---

# IoC — 1b3ceba6 (Receita Federal MV3)

Próbka: [[1b3ceba6 Chrome bank stealer]]

```
sha256   1b3ceba6a82929b53c72e137e257f7f8924173d8b0de5852253b7437723f153e
name     Receita Federal
version  11.0.0
```

## Sieć

| Host | Port / path | Rola |
|------|-------------|------|
| `ws.servpopads.com` | 443 (Socket.IO) | kanał operatora (hardcoded) |
| `servpopads.com` | `/api/config/public` | config, podmiana endpointu |
| `suahoje.com` | 3000 | host_permissions; LIVE Express 13.08 |
| `off-game.com` | 3000 | host_permissions; timeout 13.08 |
| `cobrowse.io` | 443 | zdalny pulpit sesji |
| `serpopwin.com` | `/update.xml` | update_url CRX |
| `ws.servpopads.com` | — | ads/C2 sibling |

## License / ID

```
CobrowseIO.license = ECbGBdE7OV_o_g
```

## Rozszerzenie

```
update_url   https://serpopwin.com/update.xml
permissions  tabs, storage, activeTab, scripting, cookies
hosts        <all_urls> + bradesco + bb.com.br + caixa.gov.br
```

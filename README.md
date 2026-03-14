# 📊 Investmentbolag — Marknadsöversikt

Svenska investmentbolag på Nasdaq Stockholm — live marknadsdata via Yahoo Finance, hostad på GitHub Pages.

---

## 📁 Filer i detta repo

| Fil | Syfte |
|-----|-------|
| `index.html` | **Live-rapporten** — öppnas i webbläsaren, hämtar realtidsdata. Hostas på GitHub Pages. |
| `email_template.html` | **E-postmall** — statisk HTML med illustrativa siffror. Klistra in i ditt e-postprogram. |
| `README.md` | Denna fil |

---

## 🚀 Sätt upp GitHub Pages (steg för steg)

### Steg 1 — Skapa ett GitHub-konto
Gå till [github.com](https://github.com) och skapa ett gratis konto om du inte redan har ett.

### Steg 2 — Skapa ett nytt repo
1. Klicka på **"New"** (grön knapp uppe till vänster)
2. Namnge repot, t.ex. `investmentbolag` eller `swedish-stocks`
3. Välj **Public** (krävs för gratis GitHub Pages)
4. Klicka **"Create repository"**

### Steg 3 — Ladda upp filerna
1. I ditt nya repo, klicka **"uploading an existing file"** (eller dra och släpp)
2. Ladda upp `index.html`, `email_template.html` och `README.md`
3. Klicka **"Commit changes"**

### Steg 4 — Aktivera GitHub Pages
1. Gå till **Settings** (kugghjul-ikonen i repot)
2. Scrolla ner till **"Pages"** i vänstermenyn
3. Under **"Source"**, välj **"Deploy from a branch"**
4. Välj branch: **`main`** och mapp: **`/ (root)`**
5. Klicka **"Save"**

### Steg 5 — Hämta din URL
Efter ca 1–2 minuter visas din live-URL i Pages-inställningarna:
```
https://DITT-ANVÄNDARNAMN.github.io/REPO-NAMN/
```
T.ex: `https://andersson.github.io/investmentbolag/`

---

## 📧 Uppdatera e-postmallen med din URL

Öppna `email_template.html` i en textredigerare och ersätt **båda** förekomsterna av:
```
https://VictorFisk.github.io/Weekly-Report---Investment-Companies/
```
med din riktiga GitHub Pages URL, t.ex:
```
https://andersson.github.io/investmentbolag/
```

---

## 📬 Använda e-postmallen

### Outlook (Windows/Mac)
1. Öppna `email_template.html` i en webbläsare (t.ex. Chrome)
2. Välj allt (Ctrl+A / Cmd+A) och kopiera (Ctrl+C / Cmd+C)
3. Klistra in direkt i ett nytt e-postmeddelande i Outlook
4. Formatering bevaras i de flesta fall

### Gmail
1. Öppna `email_template.html` i Chrome
2. Kopiera innehållet
3. Klistra in i Gmail (observera: Gmail kan ta bort viss formatering)
4. Alternativt: skicka som bilaga och länka till live-rapporten

### Tips: Uppdatera siffror manuellt
Siffrorna i e-postmallen är **statiska** och behöver uppdateras manuellt varje dag du skickar.
Live-rapporten (`index.html`) hämtar alltid aktuell data automatiskt vid sidladdning.

---

## 📊 Data & källor

| Datapunkt | Källa | Typ |
|-----------|-------|-----|
| Aktiekurs, dag %, volym | Yahoo Finance via CORS-proxy | Fördröjd ~15 min |
| YTD-avkastning | Beräknat från Yahoo Finance historik | Fördröjd |
| NAV-rabatt/premie | Estimat baserat på publika rapporter | Manuellt uppdaterat |
| Direktavkastning | Senast deklarerad utdelning | Manuellt uppdaterat |
| Portföljinnehav | Publika portföljrapporter | Manuellt uppdaterat |
| Analytikerdata | Illustrativa estimat | Manuellt uppdaterat |

> **Notera:** Yahoo Finance CORS-proxy (`allorigins.win`) är en gratis tjänst utan garantier. Om live-rapporten inte laddar data, försök igen om en stund.

---

## 🔄 Uppdatera NAV och analytikerdata

För att uppdatera NAV-estimat, direktavkastning eller analytikerdata:
1. Öppna `index.html` i en textredigerare
2. Hitta arrayen `const COMPANIES = [...]` längst upp i `<script>`-taggen
3. Uppdatera värdena för `navDiscount`, `dividendYield`, `priceTarget` etc.
4. Ladda upp den uppdaterade filen till GitHub — sidan uppdateras automatiskt inom minuter

---

## ⚠️ Ansvarsfriskrivning

Denna rapport tillhandahålls uteslutande i informationssyfte och utgör inte investeringsrådgivning.
Historisk avkastning är ingen garanti för framtida avkastning.

---

*Byggd med HTML, Chart.js och Yahoo Finance · Hostad gratis på GitHub Pages*

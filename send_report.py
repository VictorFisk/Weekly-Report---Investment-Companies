#!/usr/bin/env python3
"""
Weekly Investment Companies Report — Email Sender
Fetches live data from Yahoo Finance and sends a formatted HTML email via Gmail.
"""

import os
import smtplib
import json
import urllib.request
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time

# ── CONFIG (injected via GitHub Secrets) ──
GMAIL_USER     = os.environ["GMAIL_USER"]       # your Gmail address
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]   # Gmail App Password
RECIPIENT      = os.environ.get("RECIPIENT_EMAIL", GMAIL_USER)  # defaults to sender

# ── COMPANIES ──
COMPANIES = [
    {"name": "Investor B",           "ticker": "INVE-B.ST",  "nav": -5.2,  "div": 2.1},
    {"name": "Industrivärden C",     "ticker": "INDU-C.ST",  "nav": -8.1,  "div": 3.4},
    {"name": "Kinnevik B",           "ticker": "KINV-B.ST",  "nav": -22.5, "div": 0.0},
    {"name": "Latour B",             "ticker": "LATO-B.ST",  "nav": 12.3,  "div": 1.8},
    {"name": "Lundbergföretagen B",  "ticker": "LUND-B.ST",  "nav": -3.8,  "div": 2.6},
    {"name": "Ratos B",              "ticker": "RATO-B.ST",  "nav": -10.2, "div": 4.1},
    {"name": "Svolder B",            "ticker": "SVOL-B.ST",  "nav": -6.7,  "div": 3.8},
    {"name": "Öresund",              "ticker": "ORES.ST",    "nav": -9.4,  "div": 3.2},
]

GITHUB_PAGES_URL = "https://VictorFisk.github.io/Weekly-Report---Investment-Companies/"

# ── FETCH LIVE DATA ──
def fetch_quote(ticker):
    """Fetch live quote from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(ticker)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("quoteResponse", {}).get("result", [])
            return results[0] if results else {}
    except Exception as e:
        print(f"  Warning: could not fetch {ticker}: {e}")
        return {}

def fetch_history(ticker):
    """Fetch 1-year daily closes for YTD calculation."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}?interval=1d&range=1y"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("chart", {}).get("result", [{}])[0]
    except Exception as e:
        print(f"  Warning: could not fetch history for {ticker}: {e}")
        return {}

def calc_ytd(hist):
    """Calculate YTD % from historical data."""
    try:
        closes = [v for v in hist["indicators"]["quote"][0]["close"] if v is not None]
        timestamps = hist["timestamp"]
        year_start = datetime(datetime.now().year, 1, 1).timestamp()
        first_close = next(
            (closes[i] for i, t in enumerate(timestamps) if t >= year_start and closes[i] is not None),
            None
        )
        if not first_close or not closes:
            return None
        return ((closes[-1] - first_close) / first_close) * 100
    except Exception:
        return None

# ── FORMAT HELPERS ──
def fmt_sek(val):
    if val is None:
        return "–"
    return f"{val:,.2f}".replace(",", " ").replace(".", ",")

def fmt_pct(val, plus=True):
    if val is None:
        return "–"
    sign = "+" if val > 0 and plus else ""
    return f"{sign}{val:.1f}%".replace(".", ",")

def pct_badge(val):
    if val is None:
        return '<span style="color:#8b97a8;">–</span>'
    color = "#1a7a4a" if val > 0 else "#b82c2c" if val < 0 else "#8b97a8"
    bg    = "#eaf6ef" if val > 0 else "#fdf0f0" if val < 0 else "#f0f3f7"
    sign  = "+" if val > 0 else ""
    return (f'<span style="background-color:{bg};color:{color};font-family:Courier,monospace;'
            f'font-size:11px;font-weight:700;padding:2px 6px;border-radius:2px;">'
            f'{sign}{val:.1f}%</span>').replace(".", ",")

# ── BUILD HTML EMAIL ──
def build_html(rows_html, report_date, best, worst):
    return f"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Investmentbolag — Veckouppdatering</title>
</head>
<body style="margin:0;padding:0;background-color:#f0f3f7;font-family:Georgia,serif;">
<div style="max-width:640px;margin:0 auto;padding:24px 16px;">

  <!-- HEADER -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0A2342;border-radius:5px 5px 0 0;">
    <tr>
      <td style="padding:22px 28px 18px;">
        <p style="margin:0 0 4px 0;color:#C9A84C;font-size:9px;letter-spacing:3px;text-transform:uppercase;font-family:Arial,sans-serif;">Nasdaq Stockholm</p>
        <p style="margin:0 0 3px 0;color:#ffffff;font-size:22px;font-weight:700;font-family:Georgia,serif;">Svenska Investmentbolag</p>
        <p style="margin:0;color:#8AAFD4;font-size:12px;font-family:Arial,sans-serif;">Veckouppdatering — Måndag Middag</p>
      </td>
      <td style="padding:22px 28px 18px;text-align:right;vertical-align:top;">
        <p style="margin:0 0 3px 0;color:#C9A84C;font-size:11px;font-family:Arial,sans-serif;font-weight:600;">{report_date}</p>
        <p style="margin:0;color:#8AAFD4;font-size:10px;font-family:Arial,sans-serif;">Kurser fördröjda ~15 min</p>
      </td>
    </tr>
  </table>

  <!-- HIGHLIGHTS -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0f2d52;border-left:1px solid #1a3d6e;border-right:1px solid #1a3d6e;">
    <tr>
      <td style="padding:10px 28px;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="color:#8AAFD4;font-size:10px;font-family:Arial,sans-serif;">
              📈 <strong style="color:#C9A84C;">Bäst idag:</strong>
              <span style="color:#ffffff;">{best}</span>
              &nbsp;&nbsp;&nbsp;
              📉 <strong style="color:#C9A84C;">Sämst idag:</strong>
              <span style="color:#ffffff;">{worst}</span>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>

  <!-- NOTICE -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fff8e6;border-left:3px solid #C9A84C;border-right:1px solid #dde3ed;">
    <tr>
      <td style="padding:10px 18px;">
        <p style="margin:0;color:#7a5c00;font-size:11px;font-family:Arial,sans-serif;">
          📊 Data hämtad live vid sändningstillfället.
          <a href="{GITHUB_PAGES_URL}" style="color:#0A2342;font-weight:600;">Öppna interaktiv rapport →</a>
        </p>
      </td>
    </tr>
  </table>

  <!-- TABLE -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border:1px solid #dde3ed;border-top:none;">
    <tr style="background-color:#0A2342;">
      <td style="padding:9px 14px;color:#8AAFD4;font-size:9px;font-family:Arial,sans-serif;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;">BOLAG</td>
      <td style="padding:9px 10px;color:#8AAFD4;font-size:9px;font-family:Arial,sans-serif;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;text-align:right;">KURS (SEK)</td>
      <td style="padding:9px 10px;color:#8AAFD4;font-size:9px;font-family:Arial,sans-serif;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;text-align:right;">DAG %</td>
      <td style="padding:9px 10px;color:#8AAFD4;font-size:9px;font-family:Arial,sans-serif;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;text-align:right;">YTD %</td>
      <td style="padding:9px 10px;color:#8AAFD4;font-size:9px;font-family:Arial,sans-serif;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;text-align:right;">NAV %</td>
      <td style="padding:9px 14px;color:#8AAFD4;font-size:9px;font-family:Arial,sans-serif;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;text-align:right;">DIREKT %</td>
    </tr>
    {rows_html}
  </table>

  <!-- LEGEND -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f7f9fc;border:1px solid #dde3ed;border-top:none;">
    <tr>
      <td style="padding:9px 14px;">
        <p style="margin:0;color:#8b97a8;font-size:10px;font-family:Arial,sans-serif;line-height:1.6;">
          <strong style="color:#555;">NAV %</strong> = Substansvärdesrabatt/premie (estimerat) ·
          <strong style="color:#555;">YTD</strong> = Avkastning sedan årets start ·
          <strong style="color:#555;">Direkt %</strong> = Senast deklarerad utdelning
        </p>
      </td>
    </tr>
  </table>

  <!-- CTA -->
  <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;">
    <tr>
      <td style="text-align:center;padding:4px 0 8px;">
        <a href="{GITHUB_PAGES_URL}"
           style="display:inline-block;background-color:#0A2342;color:#C9A84C;text-decoration:none;
                  font-family:Arial,sans-serif;font-size:12px;font-weight:700;letter-spacing:1.5px;
                  text-transform:uppercase;padding:12px 32px;border-radius:3px;border:1px solid #C9A84C;">
          Öppna Interaktiv Rapport →
        </a>
      </td>
    </tr>
    <tr>
      <td style="text-align:center;">
        <p style="margin:0;color:#aab2bf;font-size:10px;font-family:Arial,sans-serif;">
          NAV-historik · Portföljinnehav · Analytikerdata · Jämförelsetabell
        </p>
      </td>
    </tr>
  </table>

  <!-- FOOTER -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0A2342;border-radius:0 0 5px 5px;margin-top:12px;">
    <tr>
      <td style="padding:14px 28px;">
        <p style="margin:0 0 3px 0;color:#8AAFD4;font-size:10px;font-family:Arial,sans-serif;">
          Källa: Yahoo Finance / Nasdaq Stockholm · Automatiskt utskick varje måndag kl. 12:00
        </p>
        <p style="margin:0;color:#C9A84C;font-size:10px;font-family:Arial,sans-serif;font-style:italic;">
          ⚠️ Detta är ej investeringsrådgivning. Informationen tillhandahålls i informationssyfte.
        </p>
      </td>
    </tr>
  </table>

</div>
</body>
</html>"""

def build_row(company, quote, ytd, zebra=False):
    bg = 'background-color:#fafbfd;' if zebra else ''
    price = quote.get("regularMarketPrice")
    chg   = quote.get("regularMarketChangePercent")
    return f"""
    <tr>
      <td style="padding:11px 14px;border-bottom:1px solid #eef1f6;{bg}">
        <span style="color:#0A2342;font-size:13px;font-weight:700;font-family:Arial,sans-serif;display:block;">{company['name']}</span>
        <span style="color:#8AAFD4;font-size:10px;font-family:Courier,monospace;">{company['ticker']}</span>
      </td>
      <td style="padding:11px 10px;text-align:right;font-family:Courier,monospace;font-size:13px;border-bottom:1px solid #eef1f6;{bg}">{fmt_sek(price)}</td>
      <td style="padding:11px 10px;text-align:right;border-bottom:1px solid #eef1f6;{bg}">{pct_badge(chg)}</td>
      <td style="padding:11px 10px;text-align:right;border-bottom:1px solid #eef1f6;{bg}">{pct_badge(ytd)}</td>
      <td style="padding:11px 10px;text-align:right;border-bottom:1px solid #eef1f6;{bg}">{pct_badge(company['nav'])}</td>
      <td style="padding:11px 14px;text-align:right;font-family:Courier,monospace;font-size:13px;color:#0A2342;font-weight:600;border-bottom:1px solid #eef1f6;{bg}">{company['div']:.1f}%</td>
    </tr>"""

# ── MAIN ──
def main():
    print(f"🔄 Fetching live data for {len(COMPANIES)} companies...")
    quotes = {}
    ytds   = {}

    for i, c in enumerate(COMPANIES):
        print(f"  [{i+1}/{len(COMPANIES)}] {c['ticker']}")
        quotes[c["ticker"]] = fetch_quote(c["ticker"])
        hist = fetch_history(c["ticker"])
        ytds[c["ticker"]] = calc_ytd(hist)
        time.sleep(0.3)  # be polite to Yahoo Finance

    # Build rows
    rows_html = ""
    changes = []
    for i, c in enumerate(COMPANIES):
        q   = quotes[c["ticker"]]
        ytd = ytds[c["ticker"]]
        rows_html += build_row(c, q, ytd, zebra=(i % 2 == 1))
        chg = q.get("regularMarketChangePercent")
        if chg is not None:
            changes.append((c["name"], chg))

    # Best / worst
    changes.sort(key=lambda x: x[1], reverse=True)
    best  = f"{changes[0][0]}  ({fmt_pct(changes[0][1])})"  if changes else "–"
    worst = f"{changes[-1][0]} ({fmt_pct(changes[-1][1])})" if changes else "–"

    # Date
    report_date = datetime.now().strftime("%-d %B %Y").replace(
        "January","januari").replace("February","februari").replace(
        "March","mars").replace("April","april").replace(
        "May","maj").replace("June","juni").replace(
        "July","juli").replace("August","augusti").replace(
        "September","september").replace("October","oktober").replace(
        "November","november").replace("December","december")

    html_body = build_html(rows_html, report_date, best, worst)

    # ── SEND EMAIL ──
    print(f"\n📧 Sending email to {RECIPIENT}...")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📊 Investmentbolag — Veckouppdatering {report_date}"
    msg["From"]    = GMAIL_USER
    msg["To"]      = RECIPIENT
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASS)
        smtp.sendmail(GMAIL_USER, RECIPIENT, msg.as_string())

    print("✅ Email sent successfully!")

if __name__ == "__main__":
    main()

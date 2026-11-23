#!/usr/bin/env python3
"""Generate the Roomleft topic pages (static HTML) into the repo folder given as argv[1]."""
import json, sys, html, os

OUT = sys.argv[1]
SITE = "https://roomleft.ca"
E = html.escape

CSS = """
:root{color-scheme:light dark;--bg:light-dark(#e7e4df,#171513);--panel:light-dark(#fff,#221f1c);--ink:light-dark(#111,#f1ede7);--mute:light-dark(#5d5853,#a59f97);--rule:light-dark(#d3cec7,#3a3531);--brick:#c8371e;--track:light-dark(#ece8e2,#2e2a26)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 "Schibsted Grotesk",system-ui,sans-serif;overflow-x:clip}
a{color:inherit}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:max(14px,env(safe-area-inset-top)) max(5vw,16px) 14px;max-width:1240px;margin:0 auto}
.brand{font-weight:800;font-size:20px;text-decoration:none;display:flex;align-items:center;gap:8px}
.brand i{display:inline-block;width:26px;height:26px;border-radius:7px;background:var(--brick);position:relative}
.brand i::before,.brand i::after{content:"";position:absolute;left:5px;height:4px;border-radius:2px;background:#fff}
.brand i::before{top:8px;width:14px}.brand i::after{top:14px;width:9px}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;background:var(--brick);color:#fff;font-weight:700;text-decoration:none;border-radius:12px;white-space:nowrap}
.btn.alt{background:var(--ink);color:var(--bg)}
main{max-width:860px;margin:0 auto;padding:8px max(5vw,16px) max(40px,env(safe-area-inset-bottom))}
.crumb{font-size:14px;color:var(--mute);margin:0 0 8px}.crumb a{color:var(--mute)}
h1{font-size:clamp(30px,5vw,46px);line-height:1.08;margin:0 0 12px;font-weight:800;text-wrap:balance}
.lead{font-size:19px;margin:0 0 20px;max-width:65ch}
.keys{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:1px;background:var(--rule);border-top:3px solid var(--brick);margin:0 0 28px}
.keys div{padding:16px 18px;background:var(--panel)}
.keys b{display:block;font-size:clamp(24px,3vw,30px);line-height:1.1;font-weight:800}
.keys span{font-size:14px;color:var(--mute)}
h2{font-size:26px;line-height:1.2;margin:34px 0 10px}
h3{font-size:19px;margin:20px 0 6px}
p,ul,ol{max-width:70ch}li{margin:0 0 6px}
.box{background:var(--panel);padding:18px 20px;margin:18px 0}
.box.cta{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;border-left:4px solid var(--brick)}
.box.cta p{margin:0;font-weight:600}
table{width:100%;border-collapse:collapse;background:var(--panel);font-size:16px}
th{text-align:left;font-size:13px;color:var(--mute);font-weight:500;border-bottom:2px solid var(--ink);padding:8px 10px}
td{border-bottom:1px solid var(--rule);padding:9px 10px;vertical-align:top}
.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
tr.hi td{font-weight:700}
.scroll{overflow-x:auto}
.faq details{border-bottom:1px solid var(--rule)}
.faq summary{cursor:pointer;font-weight:700;padding:13px 0;min-height:44px}
.faq details p{margin:0 0 14px}
.note{font-size:14px;color:var(--mute)}
.more{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;padding:0;list-style:none;max-width:none}
.more a{display:block;background:var(--panel);padding:14px 16px;text-decoration:none;font-weight:700;min-height:44px}
.more a span{display:block;font-weight:400;font-size:14px;color:var(--mute)}
a:focus-visible,summary:focus-visible{outline:3px solid var(--brick);outline-offset:2px}
@media(max-width:600px){body{font-size:16px}table{font-size:14px}.keys{grid-template-columns:1fr 1fr}.keys div:last-child:nth-child(odd){grid-column:1/-1}.top .btn{padding:0 14px}}
"""

PAGES = {}

def page(slug, title, desc, crumb, h1, lead, keys, body, faq, cta):
    PAGES[slug] = dict(title=title, desc=desc, crumb=crumb, h1=h1, lead=lead, keys=keys, body=body, faq=faq, cta=cta)

# ---------------- TFSA ----------------
TFSA_LIMITS = [(2009,5000),(2010,5000),(2011,5000),(2012,5000),(2013,5500),(2014,5500),(2015,10000),(2016,5500),(2017,5500),(2018,5500),
               (2019,6000),(2020,6000),(2021,6000),(2022,6000),(2023,6500),(2024,7000),(2025,7000),(2026,7000)]
cum = 0; rows = []
for y, v in TFSA_LIMITS:
    cum += v; rows.append((y, v, cum))
assert cum == 109000
tfsa_table = '<div class="scroll"><table><thead><tr><th>Year</th><th class="num">Annual limit</th><th class="num">Total room since 2009</th></tr></thead><tbody>' + \
    ''.join(f'<tr{" class=\"hi\"" if y==2026 else ""}><td>{y}</td><td class="num">${v:,}</td><td class="num">${c:,}</td></tr>' for y, v, c in reversed(rows)) + \
    '</tbody></table></div>'

page("tfsa-room-2026",
 "TFSA Contribution Room 2026 | Roomleft",
 "The 2026 TFSA limit is $7,000, and total room since 2009 is $109,000. See how your room is calculated and track it across banks — free.",
 "TFSA room 2026",
 "TFSA contribution room for 2026",
 "The TFSA dollar limit for 2026 is <b>$7,000</b>. If you’ve been eligible since the TFSA began in 2009 and have never contributed, your total room is <b>$109,000</b>.",
 [("$7,000","2026 annual limit"),("$109,000","Total room since 2009"),("Jan 1","Withdrawals come back as room")],
 f"""
<h2>How your TFSA room is calculated</h2>
<p>Your room for the year is:</p>
<ol>
<li><b>Every annual limit</b> since the year you turned 18 (or 2009, whichever is later) while living in Canada,</li>
<li><b>minus</b> everything you’ve contributed,</li>
<li><b>plus</b> anything you withdrew in <i>earlier</i> years — withdrawals come back as room on January 1 of the next year, not right away.</li>
</ol>
<p>That last rule is the one that catches people: if you take $5,000 out in June and put it back in August, that August deposit uses new room. If you had no room left, it’s an over-contribution.</p>

<h2>TFSA limits by year</h2>
{tfsa_table}
<p class="note">The 2027 limit had not been confirmed by CRA when this page was written; it’s widely expected to rise to $7,500.</p>

<h2>Why CRA My Account can show the wrong number</h2>
<p>Banks and brokerages report your TFSA deposits and withdrawals to CRA after the year ends. So in November, CRA My Account usually still shows your room as of January 1 — without this year’s contributions. If you deposit based on that number, you can over-contribute without realizing it, especially with TFSAs at more than one institution.</p>
<p>The fix is to start from CRA’s January 1 figure and subtract every deposit you’ve made this year, at every bank. That’s exactly what Roomleft does.</p>

<h2>What happens if you over-contribute</h2>
<p>CRA charges a tax of <b>1% a month</b> on the highest excess amount for every month it stays in the account. Withdrawing the excess stops the clock, but remember the withdrawal itself doesn’t create new room until next January.</p>

<h2>What to hold in a TFSA</h2>
<p>Growth investments suit a TFSA best, since gains are never taxed. US-listed dividend ETFs are a weaker fit: the 15% US withholding tax on dividends is lost in a TFSA, while it’s waived in an RRSP under the Canada–US tax treaty.</p>
""",
 [("How much TFSA room do I have in 2026?","Add up every annual limit since you turned 18 (from 2009 onward), subtract your contributions, and add back withdrawals from previous years. If you’ve been eligible since 2009 and never contributed, it’s $109,000."),
  ("What is the TFSA limit for 2026?","$7,000 — the same as in 2024 and 2025."),
  ("When do TFSA withdrawals give room back?","On January 1 of the following year. Re-contributing a withdrawal in the same year uses new room."),
  ("Why doesn’t CRA show this year’s contributions?","Institutions report TFSA activity to CRA after year-end, so CRA My Account typically lags until the following spring."),
  ("What is the TFSA over-contribution penalty?","1% a month on the highest excess amount, for each month the excess stays in your TFSA.")],
 "Track your TFSA room across every bank — free, and your data stays on your device.")

# ---------------- RRSP ----------------
page("rrsp-limit-2026",
 "RRSP Contribution Limit 2026 | Roomleft",
 "The 2026 RRSP limit is 18% of your 2025 earned income, up to $33,810. Deadline: March 1, 2027. Track your RRSP room across banks — free.",
 "RRSP limit 2026",
 "RRSP contribution limit for 2026",
 "Your 2026 RRSP limit is <b>18% of your 2025 earned income, up to $33,810</b>, plus any unused room from earlier years. The deadline to contribute for the 2026 tax year is <b>March 1, 2027</b>.",
 [("18%","Of 2025 earned income"),("$33,810","2026 maximum"),("Mar 1, 2027","Deadline for 2026"),("$35,390","2027 maximum")],
 """
<h2>Where to find your exact RRSP limit</h2>
<p>Your personal limit — called your <b>RRSP deduction limit</b> — is printed on your Notice of Assessment from your last tax return, and in CRA My Account under RRSP. It already includes unused room carried forward and subtracts any pension adjustment from a workplace pension.</p>

<h2>Which contributions count toward 2026</h2>
<p>Contributions made from <b>March 3, 2026 to March 1, 2027</b> can be deducted on your 2026 return. Contributions made in the first 60 days of 2026 (January 1 to March 2) could be claimed on your 2025 return instead — those are usually already reflected in your Notice of Assessment.</p>

<h2>The $2,000 over-contribution buffer</h2>
<p>Unlike a TFSA, an RRSP lets you go up to <b>$2,000 over</b> your limit without penalty. You can’t deduct that $2,000, but it can grow tax-sheltered. Past the buffer, CRA charges <b>1% a month</b> on the excess.</p>

<h2>Spousal RRSPs</h2>
<p>Contributions to a spousal RRSP use <i>your</i> room, while the money belongs to your spouse in retirement — a common way to even out retirement income between partners.</p>

<h2>Using your RRSP to buy a first home</h2>
<p>The Home Buyers’ Plan lets you withdraw up to <b>$60,000</b> from your RRSP for a qualifying first home, repaid over 15 years. You can combine it with a First Home Savings Account withdrawal for the same home.</p>

<h2>When an RRSP must end</h2>
<p>You must convert your RRSP to a RRIF (or an annuity) by December 31 of the year you turn 71.</p>
""",
 [("What is the RRSP limit for 2026?","18% of your 2025 earned income, up to a maximum of $33,810, plus unused room from earlier years and minus any pension adjustment."),
  ("What is the RRSP deadline for the 2026 tax year?","March 1, 2027 — 60 days after the end of 2026."),
  ("What is the RRSP limit for 2027?","The 2027 dollar maximum is $35,390."),
  ("Can I go over my RRSP limit?","Yes, by up to $2,000 without penalty, though that amount isn’t deductible. Beyond $2,000, the excess is taxed at 1% a month."),
  ("How much can I take out under the Home Buyers’ Plan?","Up to $60,000 from your RRSP for a qualifying first home, repaid over 15 years.")],
 "Track RRSP room for you and your spouse across every bank — free and private.")

# ---------------- FHSA ----------------
page("fhsa-room-2026",
 "FHSA Contribution Room 2026 | Roomleft",
 "FHSA room is $8,000 a year and $40,000 lifetime. Contribute by Dec 31 — there’s no 60-day grace period. Track your FHSA room free.",
 "FHSA room 2026",
 "FHSA contribution room for 2026",
 "A First Home Savings Account gives <b>$8,000 of room a year</b>, up to <b>$40,000 over your lifetime</b>. Contributions for 2026 must be made by <b>December 31, 2026</b> — unlike an RRSP, there’s no 60-day grace period.",
 [("$8,000","Room per year"),("$40,000","Lifetime limit"),("Dec 31","2026 deadline"),("$16,000","Most in one year, with carry-forward")],
 """
<h2>How FHSA room works</h2>
<ul>
<li><b>Room starts when you open the account</b>, not when you turn 18. Opening one early — even with $0 in it — starts the clock.</li>
<li><b>Up to $8,000 of unused room carries forward</b> to the next year. So the most you can put in during a single year is $16,000.</li>
<li><b>Withdrawals don’t give room back.</b></li>
<li><b>Over-contributing costs 1% a month</b> on the excess, the same as a TFSA.</li>
</ul>

<h2>Who can open an FHSA</h2>
<p>You must be a Canadian resident, between 18 and 71, and a first-time home buyer.</p>

<h2>Why it’s the best account for a down payment</h2>
<p>The FHSA is the only registered account that’s <b>tax-deductible going in and tax-free coming out</b> for a qualifying first home. An RRSP is deductible but taxed on withdrawal; a TFSA is tax-free on withdrawal but not deductible.</p>
<p>You can also combine an FHSA withdrawal with the RRSP Home Buyers’ Plan (up to $60,000) for the same home.</p>

<h2>What if you never buy a home?</h2>
<p>The account can stay open for up to 15 years, or until the end of the year you turn 71, whichever comes first. If you don’t buy, you can transfer the money to your RRSP or RRIF tax-free — and it doesn’t use any of your RRSP room.</p>
""",
 [("How much can I put in an FHSA in 2026?","$8,000, plus up to $8,000 of unused room carried forward from 2025 — so up to $16,000 if you opened the account in 2025 or earlier and didn’t contribute."),
  ("What is the FHSA lifetime limit?","$40,000."),
  ("What is the FHSA deadline for 2026?","December 31, 2026. FHSA contributions don’t get the 60-day grace period RRSPs have."),
  ("Do FHSA withdrawals give room back?","No. Once contributed, that room is used even if you withdraw."),
  ("What happens to my FHSA if I don’t buy a home?","After up to 15 years (or by the year you turn 71), you can move it to an RRSP or RRIF tax-free without using RRSP room.")],
 "Track FHSA room alongside your TFSA and RRSP — free, with data kept on your device.")

# ---------------- Brokerage fees ----------------
BROKERS=[
 ('Interactive Brokers',1.5,0.03,False,'Small per-share commissions; converts at near-interbank rates (0.002%, US$2 minimum).'),
 ('moomoo Canada',2,0,False,'About $1.49–US$1.99 minimum per trade; 0% FX fee, though the rate includes a variable spread.'),
 ('National Bank Direct Brokerage',0,1.75,True,'$0 Canadian and US stock and ETF trades, with USD accounts.'),
 ('Questrade',0,1.5,False,'$0 stock and ETF trades; 1.5% FX; every account holds CAD and USD.'),
 ('Qtrade',0,1.4,True,'$0 stock and ETF trades; conversion about 0.9%–1.9% by amount.'),
 ('BMO InvestorLine',0,1.75,True,'$0 stock and ETF trades since September 2026; no account admin fees.'),
 ('Wealthsimple',0,1.5,False,'$0 trades; 1.5% FX on every US trade from a CAD account.'),
 ('Desjardins Online Brokerage',0,1.75,True,'$0 stock and ETF commissions.'),
 ('CIBC Investor’s Edge',6.95,1.75,True,'$6.95 per trade; free for ages 18–24.'),
 ('RBC Direct Investing',9.95,2.25,True,'$9.95 per trade; 50+ iShares ETFs trade free.'),
 ('Scotia iTRADE',9.99,1.75,True,'$9.99 per trade; select ETFs free.'),
 ('TD Direct Investing',9.99,2.75,True,'$9.99 per trade; measured FX spread about 2.6%–3.3%.'),
]
ranked = sorted([(n, c, fx, est, d, 24*c + 10000*fx/100) for n, c, fx, est, d in BROKERS], key=lambda r: (r[5], r[0]))
brk_table = '<div class="scroll"><table><thead><tr><th>#</th><th>Brokerage</th><th class="num">Per trade</th><th class="num">FX cost</th><th class="num">Est. yearly cost*</th></tr></thead><tbody>' + \
  ''.join(f'<tr{" class=\"hi\"" if i<3 else ""}><td>{i+1}</td><td>{E(n)}<br><span class="note">{E(d)}</span></td><td class="num">{"$0" if not c else f"${c:.2f}"}</td><td class="num">{"~" if est else ""}{(f"{fx:g}%") if fx else "0%"}</td><td class="num">${round(t):,}</td></tr>' for i, (n, c, fx, est, d, t) in enumerate(ranked)) + \
  '</tbody></table></div>'

page("brokerage-fees",
 "Best Brokerage Fees in Canada | Roomleft",
 "Canadian brokerages ranked by trading fees and FX costs. Most trades are now $0 — currency conversion is where costs differ. Free calculator.",
 "Brokerage fees",
 "Best brokerage fees in Canada: trading and FX costs ranked",
 "Most Canadian online brokerages now charge <b>$0 to trade</b> stocks and ETFs. The real difference is the cost of <b>converting Canadian dollars to US dollars</b> — from almost nothing to over 2.5% at some banks.",
 [("$0","Trades at most brokers"),("1.5%–2.75%","Typical FX cost"),("~0.1%","With Norbert’s Gambit")],
 f"""
<h2>Ranking for a typical investor</h2>
<p>Estimated yearly cost for someone making 24 trades a year and converting $10,000 CAD to USD once:</p>
{brk_table}
<p class="note">*24 trades × per-trade commission + one $10,000 CAD→USD conversion. Converting back costs about the same again. Fees checked November 2026 from brokers’ fee schedules and published comparisons. Banks don’t publish their currency spreads, so figures marked ~ are typical estimates. Promotions, small-account fees and options pricing aren’t included — confirm on each broker’s site before switching.</p>

<div class="box cta"><p>Your numbers are different? Rank them by your own trades and conversions.</p><a class="btn" href="/#brokers">Open the calculator</a></div>

<h2>Why FX costs matter more than commissions</h2>
<p>A $9.99 commission on a $5,000 trade is 0.2%. A 1.5% currency conversion on the same trade is $75 — and you pay it again when you convert back. If you buy US-listed stocks or ETFs, the conversion method usually matters more than which broker charges $0.</p>

<h2>Norbert’s Gambit: converting for about 0.1%</h2>
<p>Norbert’s Gambit converts currency by buying a stock or ETF listed in both Canadian and US dollars (commonly DLR and DLR.U), then journaling it to the other currency and selling. The cost is the bid-ask spread plus any commissions or journal fee — roughly <b>0.1%</b> for conversions of a few thousand dollars or more, instead of 1.5%–2.5%. Most Canadian brokerages support it, though some need a phone call to journal the shares, and Questrade and Wealthsimple charge a $9.95 journal fee.</p>

<h2>Other ways to cut currency costs</h2>
<ul>
<li><b>Hold USD in a USD account</b> so dividends and sale proceeds stay in US dollars until you need them.</li>
<li><b>Use Canadian-listed versions</b> of US index ETFs if you don’t want to convert at all — though in an RRSP, US-listed ETFs avoid the 15% US withholding tax on dividends.</li>
</ul>
""",
 [("Which Canadian brokerage has the lowest fees?","For CAD-only investors, any $0-commission broker (Questrade, Wealthsimple, National Bank, Qtrade, BMO InvestorLine, Desjardins) costs essentially nothing. For US investing, Interactive Brokers and moomoo have the lowest currency conversion costs."),
  ("Are $0-commission trades really free?","The commission is free, but you can still pay currency conversion fees on US trades, ECN fees on some order types, and the bid-ask spread."),
  ("What is Norbert’s Gambit?","A way to convert CAD to USD (or back) by buying an inter-listed security like DLR, journaling it to the other currency and selling — usually around 0.1% instead of 1.5%–2.5%."),
  ("Which big-bank brokerage is cheapest?","BMO InvestorLine, which moved to $0 stock and ETF trades in September 2026. CIBC Investor’s Edge charges $6.95 per trade; TD, RBC and Scotia charge about $10."),
  ("How much do Canadian banks charge to convert USD?","Typically 1.5%–2.5% built into the exchange rate; independent measurements have put TD’s spread at about 2.6%–3.3%.")],
 "Rank brokerages by your own trading — and track TFSA, RRSP and FHSA room for free.")

# ---------------- render ----------------
NAV = [("tfsa-room-2026","TFSA room 2026","$7,000 limit, $109,000 total"),("rrsp-limit-2026","RRSP limit 2026","18% up to $33,810"),
       ("fhsa-room-2026","FHSA room 2026","$8,000 a year, $40,000 lifetime"),("brokerage-fees","Brokerage fees","Trading and FX costs ranked")]

def render(slug, p):
    url = f"{SITE}/{slug}"
    faq_ld = {"@context":"https://schema.org","@graph":[
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]},
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Roomleft","item":SITE+"/"},{"@type":"ListItem","position":2,"name":p["crumb"],"item":url}]}]}
    keys = ''.join(f'<div><b>{E(k)}</b><span>{E(v)}</span></div>' for k, v in p["keys"])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in p["faq"])
    more = ''.join(f'<li><a href="/{s}">{E(t)}<span>{E(d)}</span></a></li>' for s, t, d in NAV if s != slug)
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["desc"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{E(p["title"])}">
<meta property="og:description" content="{E(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<meta name="theme-color" content="#e7e4df" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#171513" media="(prefers-color-scheme: dark)">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<header class="top"><a class="brand" href="/"><i aria-hidden="true"></i>Roomleft</a><a class="btn" href="/">Open the tracker</a></header>
<main>
<p class="crumb"><a href="/">Roomleft</a> › {E(p["crumb"])}</p>
<h1>{E(p["h1"])}</h1>
<p class="lead">{p["lead"]}</p>
<div class="keys">{keys}</div>
{p["body"]}
<div class="box cta"><p>{E(p["cta"])}</p><a class="btn" href="/">Open Roomleft</a></div>
<section class="faq"><h2>Common questions</h2>{faq}</section>
<h2>More guides</h2>
<ul class="more">{more}</ul>
<p class="note">General information for Canadians, not tax or investment advice. Confirm your contribution room with CRA.</p>
</main>
<script>if('serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{{}})</script>
</body>
</html>
"""

for slug, p in PAGES.items():
    assert len(p["desc"]) <= 155, (slug, len(p["desc"]))
    with open(os.path.join(OUT, slug + ".html"), "w") as f:
        f.write(render(slug, p))
    print(slug, "title", len(p["title"]), "desc", len(p["desc"]))

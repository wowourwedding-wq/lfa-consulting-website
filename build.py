# Builds every page of the LFA Consulting site from one shared header/footer.
# Run:  python build.py   (then commit + push -> GitHub Action deploys to Cloudflare Pages)
import re, pathlib
ROOT = pathlib.Path(__file__).parent
WA = "https://wa.me/27615359002?text="
EMAIL = "lfaconsulting1@outlook.com"
LOGO = ('<svg width="{s}" height="{s}" viewBox="0 0 100 100" fill="none"><circle cx="50" cy="50" r="46" stroke="#D4AF37" stroke-width="4"/>'
        '<g fill="#D4AF37"><rect x="33" y="44" width="11" height="26" rx="1"/><rect x="45.5" y="34" width="11" height="36" rx="1"/>'
        '<rect x="58" y="50" width="9" height="20" rx="1"/></g></svg>')
NAV = [("index.html", "Home"), ("business.html", "Business"), ("personal-tax.html", "Personal Tax"),
       ("immigration.html", "Immigration"), ("work.html", "Our Work"), ("about.html", "About"), ("contact.html", "Contact")]

def head(title, desc, active):
    links = "\n".join(f'      <a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://lfa-consulting.pages.dev/images/lilian.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0A2342">
<link rel="icon" href="data:image/svg+xml,{LOGO.format(s=64).replace('#', '%23').replace('"', "'")}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=20261125">
</head>
<body>

<header class="nav">
  <div class="wrap">
    <a class="logo" href="index.html">{LOGO.format(s=40)}<span class="nm">LFA <b>Consulting</b></span></a>
    <nav class="navlinks" id="menu">
{links}
      <a href="contact.html" class="btn">Free Consultation</a>
    </nav>
    <button class="burger" aria-label="Menu">&#9776;</button>
  </div>
</header>
'''

FOOT = f'''
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div class="fabout">
        <a class="logo" href="index.html">{LOGO.format(s=32)}<span class="nm">LFA <b>Consulting</b></span></a>
        <p>Accounting, tax, compliance, non-profit and immigration support — helping businesses and individuals in South Africa and Zimbabwe stay compliant, organised and financially confident.</p>
        <p style="margin-top:12px">Led by Lilian Ngubane · Management Accountant · MBL · Est. 2025</p>
      </div>
      <div>
        <h4>Services</h4>
        <a href="business.html">Business Accounting &amp; Tax</a>
        <a href="business.html#nonprofit">Non-Profit &amp; Church Registration</a>
        <a href="personal-tax.html">Personal Tax</a>
        <a href="immigration.html">Immigration &amp; Visas</a>
        <a href="business.html#zimbabwe">Zimbabwe Services</a>
        <a href="https://lfa-bizlaunch.pages.dev" target="_blank" rel="noopener">LFA BizLaunch (company registration)</a>
      </div>
      <div>
        <h4>Get in touch</h4>
        <a href="tel:+27615359002">SA: +27 61 535 9002</a>
        <a href="tel:+263783238554">Zim: +263 78 323 8554</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="{WA}Hi%20LFA%20Consulting%2C%20I%27d%20like%20a%20free%20consultation.">WhatsApp us</a>
        <a href="downloads/LFA-SARS-Compliance-Checklist.pdf" download>Free SARS Compliance Checklist</a>
      </div>
    </div>
    <div class="fbottom">© <span id="yr"></span> LFA Consulting. All rights reserved. &nbsp;·&nbsp; Professional fees do not guarantee outcomes; final decisions rest with SARS, CIPC, Home Affairs and the relevant authorities.</div>
  </div>
</footer>

<a class="wa" href="{WA}Hi%20LFA%20Consulting%2C%20I%27d%20like%20a%20free%20consultation." title="Chat on WhatsApp" aria-label="Chat on WhatsApp" data-icon="whatsapp"></a>
<script src="main.js?v=20261125"></script>
'''

def page(fname, title, desc, body, extra_script=""):
    html = head(title, desc, fname) + body + FOOT + extra_script + "</body>\n</html>\n"
    (ROOT / fname).write_text(html, encoding="utf-8")
    print("wrote", fname, len(html))

def old_body(fname):
    t = (ROOT / "src" / fname).read_text(encoding="utf-8")
    b = t.split("</header>", 1)[1].split("<footer>", 1)[0]
    return b

def old_script(fname):
    t = (ROOT / "src" / fname).read_text(encoding="utf-8")
    m = re.search(r"(?s)(<script>.*?</script>)", t)
    return (m.group(1) + "\n") if m else ""

# ---------------------------------------------------------------- shared blocks
CASES = [
  ("Grant reporting · Arts NPC", "R360k", "government grant fully accounted for",
   "Independent expenditure report for a national arts grant",
   "A music-heritage foundation received a Department of Sport, Arts &amp; Culture grant for a community gospel festival. We traced every payment to an invoice, agreement or till slip and to the bank statements.",
   ["24 of 24 payments traced", "Bank balance reconciled to R0.00", "Report, evidence pack &amp; expense register"]),
  ("Non-profits · Churches", "NPC+NPO+PBO", "registered in one process",
   "Non-profit &amp; church registrations",
   "Registration of two Non-Profit Companies for a ministry — a foundation and a church — with director requirements, founding documents and a clear fixed-fee quote.",
   ["One founding document for CIPC, DSD &amp; SARS", "Section 18A pathway for donor certificates", "Governance templates included"]),
  ("Compliance clean-up", "CIPC + SARS", "brought back into good standing",
   "Church NPC compliance rescue",
   "A registered church NPC had fallen behind. We scoped the outstanding CIPC annual returns, beneficial ownership filing, SARS income-tax activation, outstanding ITR14s and tax clearance.",
   ["Outstanding annual returns", "Beneficial ownership declaration", "Tax Compliance Status (tax clearance)"]),
  ("Funding · Logistics", "R4.3m", "bank-funding business plan",
   "Funding-ready plans for a haulage start-up",
   "Two separate document sets for a new container &amp; road-haulage company: a bank-funding plan (asset finance + working capital) and a lean equity plan for private investors, each with a company profile.",
   ["27-page bank business plan", "25-page investor plan", "Two 13-page company profiles"]),
  ("Start-up · Cleaning &amp; facilities", "Level 1", "B-BBEE positioning",
   "Launch kit for a woman-owned cleaning company",
   "Everything a new facilities company needs to tender: company profile, business plan with three-year financials, B-BBEE EME affidavit, a quotation tool, letterhead and a services flyer.",
   ["8-page company profile", "14-page business plan", "Quotation generator &amp; flyer"]),
  ("Immigration · Family", "s18", "relative's visa application pack",
   "Visa pack for a widowed parent of SA citizens",
   "A full application pack for a foreign parent caring for South African children after her husband's death: covering letter grounded in Constitutional Court case law, document checklist and sworn affidavit.",
   ["Case-law-backed covering letter", "Document checklist", "Sole-caregiver affidavit"]),
]
def case_html(c, i):
    tag, metric, mlbl, h, p, items = c
    lis = "".join(f"<li>{x}</li>" for x in items)
    return (f'<div class="case reveal d{i%3}"><span class="tag">{tag}</span><div class="metric">{metric}</div>'
            f'<div class="mlbl">{mlbl}</div><h3>{h}</h3><p>{p}</p><ul>{lis}</ul></div>')

MARQUEE_ITEMS = ["SARS", "CIPC", "SARS eFiling", "Dept. of Social Development", "COIDA", "B-BBEE", "CSD &amp; Tenders",
                 "Home Affairs", "ZIMRA", "Section 18A", "UIF · PAYE · SDL"]
MARQUEE = ('<div class="creds" aria-label="Authorities we work with"><div class="wrap"><div class="track">'
           + "".join(f"<span>{x}</span>" for x in MARQUEE_ITEMS * 2) + "</div></div></div>\n")

RESOURCE = '''
<section style="padding:70px 0">
  <div class="wrap">
    <div class="resource reveal">
      <div class="doc">LFA</div>
      <div><span class="kicker">Free download</span><h3>The SARS Compliance Checklist</h3>
        <p>The monthly, VAT-period and yearly tasks South African businesses forget — plus 14 blind spots that cause SARS penalties. One page, print it and tick it off.</p></div>
      <a class="btn btn-navy" href="downloads/LFA-SARS-Compliance-Checklist.pdf" download>Download free PDF <i data-icon="download"></i></a>
    </div>
  </div>
</section>
'''

CTA = f'''
<section class="ctaband">
  <div class="wrap reveal">
    <h2>Let's get you compliant</h2>
    <p>Book your free 15–30 minute consultation. We'll scope exactly what you need and give you a clear, honest quote.</p>
    <div class="cta-row">
      <a href="{WA}Hi%20LFA%20Consulting%2C%20I%27d%20like%20a%20free%20consultation." class="btn">Chat on WhatsApp <i data-icon="arrow"></i></a>
      <a href="contact.html" class="btn btn-ghost">Send an enquiry</a>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- HOME
home = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">South Africa · Zimbabwe · Clients worldwide</span>
      <h1>Accounting, tax &amp; immigration — <span>handled personally.</span></h1>
      <p class="lead">Company and non-profit registrations, SARS returns, funding-ready business plans and visa support. Clear prices, no hidden fees, and an advisor who answers her own WhatsApp.</p>
      <div class="cta-row">
        <a href="contact.html" class="btn">Book a free consultation <i data-icon="arrow"></i></a>
        <a href="work.html" class="btn btn-ghost">See our work</a>
      </div>
      <div class="trust">
        <div class="t"><b>10<em>+</em></b><span>Companies registered</span></div>
        <div class="t"><b>R360<em>k</em></b><span>Grant funds accounted for</span></div>
        <div class="t"><b>14</b><span>Visa destinations</span></div>
      </div>
    </div>
    <div class="portrait" aria-hidden="true">
      <div class="ring"></div>
      <div class="frame"><img src="images/lilian.jpg" alt=""><div class="cap"><b>Lilian Ngubane</b><span>Founder &amp; Principal</span></div></div>
      <div class="chip k1 float"><span class="ic" data-icon="badgecheck"></span><div><b>Founder-led</b>Every file handled personally</div></div>
      <div class="chip k2 float d1"><span class="ic" data-icon="calendar"></span><div><b>Free</b>15–30 min consultation</div></div>
    </div>
  </div>
</section>
{MARQUEE}
<section id="services">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">What we do</span>
      <h2>Four ways we help you move forward</h2>
      <p>Whether you run a business, lead a church or non-profit, file your own tax, or plan a move abroad.</p>
    </div>
    <div class="cards four">
      <div class="card reveal"><div class="icon-tile"><span class="ic" data-icon="building"></span></div><h3>Business Accounting &amp; Tax</h3><p>Company registration, monthly bookkeeping, SARS returns, VAT, B-BBEE, tenders and business plans.</p><a class="more" href="business.html">Business services <i data-icon="arrow"></i></a></div>
      <div class="card reveal d1"><div class="icon-tile"><span class="ic" data-icon="church"></span></div><h3>Non-Profits &amp; Churches</h3><p>NPC, NPO and PBO / Section 18A registration, compliance clean-ups and grant expenditure reports.</p><a class="more" href="business.html#nonprofit">Non-profit services <i data-icon="arrow"></i></a></div>
      <div class="card reveal d2"><div class="icon-tile"><span class="ic" data-icon="receipt"></span></div><h3>Personal Tax</h3><p>ITR12 returns, provisional tax, eFiling set-up, objections, refunds and tax clearance for foreign transfers.</p><a class="more" href="personal-tax.html">Personal tax <i data-icon="arrow"></i></a></div>
      <div class="card reveal d3"><div class="icon-tile"><span class="ic" data-icon="plane"></span></div><h3>Immigration &amp; Visas</h3><p>Visa support for 14 destinations, SA permits, residence, waivers and relative's visas.</p><a class="more" href="immigration.html">Immigration <i data-icon="arrow"></i></a></div>
    </div>
  </div>
</section>

<section class="dark" id="work">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">Recent work</span>
      <h2>Real work for real clients</h2>
      <p>A few recent engagements. Client names are kept confidential.</p>
    </div>
    <div class="cases">
      {"".join(case_html(c, i) for i, c in enumerate(CASES[:3]))}
    </div>
    <div class="center"><a class="morelink" href="work.html">See all our work <i data-icon="arrow"></i></a></div>
  </div>
</section>

<section class="alt" id="packages">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">Popular packages</span>
      <h2>Clear prices, chosen most often</h2>
      <p>Fixed starting prices. Your exact scope is confirmed at the free consultation.</p>
    </div>
    <div class="packs">
      <div class="pack reveal"><h3>LaunchPack</h3><div class="who">New company, set up properly</div>
        <div class="price">R1,499 <small>once-off</small></div>
        <ul><li>Pty Ltd registration (CIPC)</li><li>SARS tax number</li><li>Beneficial ownership filing</li><li>B-BBEE EME affidavit</li><li>MOI &amp; share certificates</li></ul>
        <a class="btn btn-navy" href="https://lfa-bizlaunch.pages.dev" target="_blank" rel="noopener">Start with BizLaunch</a></div>
      <div class="pack hot reveal d1"><span class="flag">Most popular</span><h3>Docs + Books</h3><div class="who">Growing small businesses</div>
        <div class="price">R1,200 <small>/ month</small></div>
        <ul><li>Branded invoices, quotes &amp; statements</li><li>Monthly bookkeeping &amp; reconciliations</li><li>SARS monitoring &amp; deadline reminders</li><li>Email &amp; WhatsApp support</li></ul>
        <a class="btn" href="business.html#packages">See all monthly packages</a></div>
      <div class="pack reveal d2"><h3>Non-Profit Package</h3><div class="who">Churches, foundations &amp; NGOs</div>
        <div class="price">R4,999 <small>all-in</small></div>
        <ul><li>Non-Profit Company (CIPC)</li><li>NPO registration (DSD)</li><li>PBO / Section 18A (SARS)</li><li>Founding document &amp; governance templates</li><li>All statutory fees included</li></ul>
        <a class="btn btn-navy" href="business.html#nonprofit">Non-profit details</a></div>
    </div>
  </div>
</section>

<section class="alt" id="how" style="padding-top:20px">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">How it works</span>
      <h2>Simple, transparent, done properly</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="no">1</div><h3>Free consultation</h3><p>WhatsApp, call or send the form. We listen and assess your needs at no charge.</p></div>
      <div class="step reveal d1"><div class="no">2</div><h3>Clear scope &amp; quote</h3><p>A written quote showing exactly what's included. No hidden fees.</p></div>
      <div class="step reveal d2"><div class="no">3</div><h3>We handle it</h3><p>Registrations, returns and applications are prepared, checked and submitted.</p></div>
      <div class="step reveal d3"><div class="no">4</div><h3>Stay compliant</h3><p>Ongoing reminders and support, so a deadline never catches you out.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="founder-img reveal"><img src="images/lilian.jpg" alt="Lilian Ngubane, Founder and Principal of LFA Consulting"></div>
      <div class="reveal d1">
        <span class="kicker">Meet your advisor</span>
        <h2>Real advice from a real person, not a call centre</h2>
        <p>Every quote, return and application is handled personally by Lilian Ngubane. Your work is never handed to a junior. You get an advisor who knows your file by name and explains things in plain language.</p>
        <div class="creds-list"><span>Management Accountant</span><span>Master's in Business Leadership (MBL)</span><span>CIMA studies</span></div>
        <ul class="checklist">
          <li><span class="ic" data-icon="check"></span> Clear, upfront pricing with no hidden fees</li>
          <li><span class="ic" data-icon="check"></span> Same-business-day responses</li>
          <li><span class="ic" data-icon="check"></span> Fully remote, across South Africa and Zimbabwe</li>
        </ul>
        <a href="about.html" class="btn">More about LFA <i data-icon="arrow"></i></a>
      </div>
    </div>
  </div>
</section>
{RESOURCE}{CTA}'''
page("index.html", "LFA Consulting — Accounting, Tax, Non-Profit &amp; Immigration | South Africa &amp; Zimbabwe",
     "Founder-led accounting, tax, compliance, non-profit registration and immigration support in South Africa and Zimbabwe. Clear prices, free initial consultation.", home)

# ---------------------------------------------------------------- WORK (new)
docs = [("file", "Company profiles"), ("chart", "Business plans"), ("coins", "Financial projections"), ("clipboard", "Grant expenditure reports"),
        ("badgecheck", "B-BBEE affidavits"), ("receipt", "Quotations &amp; invoices"), ("scale", "Founding documents (MOI)"), ("shield", "Sworn affidavits"),
        ("globe", "Visa covering letters"), ("check", "Document checklists"), ("user", "Cruise-ship CVs"), ("building", "Letterheads &amp; branding")]
work = f'''
<section class="hero sm">
  <div class="wrap">
    <span class="pill">Our work</span>
    <h1>Work we've <span>delivered.</span></h1>
    <p class="lead">From government grant reports to non-profit registrations, funding plans and visa packs. Here's the kind of work LFA does every month.</p>
    <div class="trust">
      <div class="t"><b>10<em>+</em></b><span>Companies registered</span></div>
      <div class="t"><b>R360<em>k</em></b><span>Grant funds accounted for</span></div>
      <div class="t"><b>R4.3<em>m</em></b><span>Funding plan prepared</span></div>
      <div class="t"><b>2</b><span>Countries: SA &amp; Zimbabwe</span></div>
    </div>
  </div>
</section>

<section class="light-cases">
  <div class="wrap">
    <div class="sec-head reveal"><span class="kicker">Case studies</span><h2>Selected engagements</h2>
      <p>Client names and identifying details are withheld to protect confidentiality.</p></div>
    <div class="cases">
      {"".join(case_html(c, i) for i, c in enumerate(CASES))}
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head reveal"><span class="kicker">Ongoing</span><h2>Everyday compliance work</h2></div>
    <div class="rgrid">
      <div class="ritem reveal"><div class="n">10+</div><div class="l">Companies registered</div><div class="d">CIPC registration and SARS tax numbers</div></div>
      <div class="ritem reveal d1"><div class="n">Monthly</div><div class="l">Returns managed</div><div class="d">SARS and CIPC compliance for retainer clients</div></div>
      <div class="ritem reveal d2"><div class="n">COIDA</div><div class="l">Letters of Good Standing</div><div class="d">Registration and compliance</div></div>
      <div class="ritem reveal d3"><div class="n">SA &amp; Zim</div><div class="l">Business admin</div><div class="d">Invoices, statements and books, done for you</div></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal"><span class="kicker">What we produce</span><h2>Professional documents, in your brand</h2>
      <p>Every document is prepared, checked and ready to submit, sign or send.</p></div>
    <div class="doclist reveal">
      {"".join(f'<div><span class="ic" data-icon="{i}"></span>{t}</div>' for i, t in docs)}
    </div>
  </div>
</section>
{RESOURCE}{CTA}'''
page("work.html", "Our Work — LFA Consulting", "Case studies from LFA Consulting: grant expenditure reports, non-profit registrations, funding business plans, compliance clean-ups and visa application packs.", work)

# ---------------------------------------------------------------- BUSINESS (existing body + new sections)
b = old_body("business.html")
b = b.replace('<div class="from"><b>from R750<small style="text-transform:none">/mo</small></b><small>Full back-office from R2,500/mo</small></div>',
              '<div class="from"><b>from R450<small style="text-transform:none">/mo</small></b><small>Full back-office from R2,500/mo</small></div>')
b = b.replace('<tr><td>Business Admin (invoices, quotes &amp; statements, done-for-you)</td><td class="price">R750/mo</td></tr>',
              '<tr><td>Non-Profit Company only (CIPC)</td><td class="price">R1,500</td></tr>\n      <tr><td>Non-profit compliance clean-up (CIPC + SARS)</td><td class="price">R2,700</td></tr>')
b = b.replace('<tr><td>Starter Compliance Retainer (monthly)</td><td class="price">R1,200/mo</td></tr>\n      <tr><td>Growing Business Retainer (monthly)</td><td class="price">R2,200/mo</td></tr>',
              '<tr><td>Financial Projections &amp; Cash Flow</td><td class="price">R2,200</td></tr>\n      <tr><td>Tender &amp; CSD Compliance</td><td class="price">R1,500</td></tr>\n      <tr><td>Payroll &amp; HR Advisory</td><td class="price">R900</td></tr>\n      <tr><td>Due Diligence &amp; Reporting</td><td class="price">R1,500</td></tr>')
b = b.replace('<div class="card reveal"><div class="icon-tile"><span class="ic" data-icon="badgecheck"></span></div><h3>Non-Profit',
              '<div class="card reveal d2"><div class="icon-tile"><span class="ic" data-icon="church"></span></div><h3>Non-Profit')
b = b.replace('<div class="card reveal"><div class="icon-tile"><span class="ic" data-icon="receipt"></span></div><h3>Invoicing',
              '<div class="card reveal"><div class="icon-tile"><span class="ic" data-icon="file"></span></div><h3>Invoicing')
b = b.replace("South Africa &amp; Zimbabwe.</p>", "South Africa &amp; Zimbabwe.</p>", 1)
packs = f'''
<section id="packages">
  <div class="wrap">
    <div class="sec-head reveal"><span class="kicker">Monthly packages</span><h2>Your back office, done for you</h2>
      <p>Invoicing, bookkeeping, statements and tax handled every month. Prices scale with transaction volume.</p></div>
    <div class="packs">
      <div class="pack reveal"><h3>Starter</h3><div class="who">Sole props &amp; side businesses</div><div class="price">R450 <small>/ month</small></div>
        <ul><li>Branded invoices &amp; quotations</li><li>Monthly customer statements</li><li>Or use our app to do it yourself</li><li>Email &amp; WhatsApp support</li></ul>
        <a class="btn btn-navy" href="{WA}Hi%20LFA%2C%20I%27m%20interested%20in%20the%20Starter%20package.">Start with Starter</a></div>
      <div class="pack hot reveal d1"><span class="flag">Most popular</span><h3>Docs + Books</h3><div class="who">Growing small businesses</div><div class="price">R1,200 <small>/ month</small></div>
        <ul><li>Everything in Starter</li><li>Monthly bookkeeping &amp; reconciliations</li><li>Know who owes you, always</li><li>SARS monitoring &amp; reminders</li></ul>
        <a class="btn" href="{WA}Hi%20LFA%2C%20I%27m%20interested%20in%20the%20Docs%20%2B%20Books%20package.">Choose Docs + Books</a></div>
      <div class="pack reveal d2"><h3>Full Package</h3><div class="who">Your whole finance function</div><div class="price">R2,500 <small>/ month</small></div>
        <ul><li>Everything in Docs + Books</li><li>VAT &amp; SARS returns filed</li><li>Payroll add-ons available</li><li>Dedicated accountant support</li></ul>
        <a class="btn btn-navy" href="{WA}Hi%20LFA%2C%20I%27m%20interested%20in%20the%20Full%20Package.">Go Full Package</a></div>
    </div>
    <p class="note">Just need to register a company and stay compliant? See <a href="https://lfa-bizlaunch.pages.dev" target="_blank" rel="noopener">LFA BizLaunch: LaunchPack R1,499 &amp; compliance from R399/month</a>.<br>Once-off bundles: Starter R3,200 (CIPC + tax number) · Growth R8,600 (CIPC + tax number + ITR14 + VAT).</p>
  </div>
</section>

<section class="alt" id="nonprofit">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="kicker">Non-profits &amp; churches</span>
        <h2>Register once, register right</h2>
        <p>A non-profit needs three registrations to receive donations and issue tax certificates: an NPC at CIPC, an NPO at the Department of Social Development, and PBO / Section 18A status at SARS. We draft one founding document that satisfies all three, so nothing has to be redone later.</p>
        <ul class="checklist">
          <li><span class="ic" data-icon="check"></span> <span><b>Full package R4,999</b>: NPC + NPO + PBO/18A, all statutory fees included</span></li>
          <li><span class="ic" data-icon="check"></span> <span><b>NPC only R1,500</b>: CIPC registration</span></li>
          <li><span class="ic" data-icon="check"></span> <span><b>Compliance clean-up from R2,700</b>: outstanding CIPC returns, beneficial ownership, SARS returns &amp; tax clearance</span></li>
          <li><span class="ic" data-icon="check"></span> <span><b>Grant expenditure reports</b>: funds traced to invoices and bank statements for your funder (quoted per grant)</span></li>
        </ul>
        <a href="{WA}Hi%20LFA%2C%20I%27d%20like%20help%20registering%20a%20non-profit%20%2F%20church." class="btn">Talk about your non-profit <i data-icon="arrow"></i></a>
      </div>
      <div class="simg reveal d1"><img src="images/meeting.jpg" alt="Board members meeting"><div class="badge-float"><div class="n">R4,999</div><span>NPC + NPO + PBO<br>all-inclusive</span></div></div>
    </div>
  </div>
</section>

<section id="zimbabwe">
  <div class="wrap">
    <div class="zim">
      <div class="reveal">
        <span class="kicker">Zimbabwe</span>
        <h2>Also serving businesses in Zimbabwe</h2>
        <p>The same done-for-you service, priced in US dollars and built around ZIMRA. Invoices, statements, bookkeeping and annual returns, handled remotely.</p>
        <a href="tel:+263783238554" class="btn btn-navy">Call +263 78 323 8554</a>
      </div>
      <div class="zprices reveal d1">
        <div class="zp"><em>Starter</em><b>$35<small style="font-size:13px">/mo</small></b><span>Invoices, quotes &amp; statements</span></div>
        <div class="zp"><em>Docs + Books</em><b>$90<small style="font-size:13px">/mo</small></b><span>Plus monthly bookkeeping</span></div>
        <div class="zp"><em>Full Package</em><b>$150<small style="font-size:13px">/mo</small></b><span>Books + ZIMRA tax filing</span></div>
        <div class="zp"><em>Annual ZIMRA return</em><b>from $80</b><span>Once-off</span></div>
      </div>
    </div>
  </div>
</section>
'''
b = b.replace('<section class="alt" id="pricing">', packs + '\n<section class="alt" id="pricing">', 1)
b = b.replace('<section class="ctaband">', RESOURCE + '<section class="ctaband">', 1)
page("business.html", "Business Accounting, Tax, Non-Profit &amp; Zimbabwe Services — LFA Consulting",
     "Company registration, monthly bookkeeping packages, SARS returns, B-BBEE, tenders, business plans, non-profit registration (R4,999) and Zimbabwe services.", b)

# ---------------------------------------------------------------- PERSONAL TAX
p = old_body("personal-tax.html")
p = p.replace('<section class="ctaband">', RESOURCE.replace("The SARS Compliance Checklist", "The SARS Compliance Checklist (for business owners)") + '<section class="ctaband">', 1)
page("personal-tax.html", "Personal Tax Returns (ITR12), Provisional Tax &amp; Refunds — LFA Consulting",
     "Individual SARS tax returns from R650, provisional tax, eFiling set-up, objections, refunds and tax clearance for foreign transfers.", p)

# ---------------------------------------------------------------- IMMIGRATION
im = old_body("immigration.html")
extra = '''      <div class="card reveal"><div class="icon-tile"><span class="ic" data-icon="users"></span></div><h3>Relative's &amp; Family Visas</h3><p>Application packs for parents, spouses and relatives of South African citizens: covering letter, document checklist and affidavits.</p><div class="from"><b>from R1,500</b><small>Quoted per case</small></div></div>
      <div class="card reveal d1"><div class="icon-tile"><span class="ic" data-icon="file"></span></div><h3>Cruise-Ship &amp; Overseas Job CVs</h3><p>Cruise-industry CVs, cover letters and interview coaching. We never charge placement fees, and we tell you if an agency asks for one.</p><div class="from"><b>from US$30</b><small>With coaching US$70–90</small></div></div>
    </div>
  </div>
</section>'''
im = im.replace('''<div class="from"><b>from R3,000</b></div></div>
    </div>
  </div>
</section>''', '<div class="from"><b>from R3,000</b></div></div>\n' + extra, 1)
im = im.replace("Processing times and final decisions rest with the relevant immigration authority (IRCC, Home Affairs, etc.). Professional fees are for guidance and application support and do not guarantee outcomes.",
                "Processing times and final decisions rest with the relevant immigration authority (IRCC, Home Affairs, etc.). Our fees are for guidance, document preparation and application support, not regulated representation. Where a licensed representative is legally required, we refer you to one. Fees do not guarantee outcomes.")
page("immigration.html", "Immigration &amp; Visa Support for 14 Destinations — LFA Consulting",
     "Visa guidance and application support for the UK, Canada, Australia, USA, UAE, Europe and more, plus SA permits, residence, waivers and relative's visas.", im)

# ---------------------------------------------------------------- ABOUT
about = f'''
<section class="hero sm">
  <div class="wrap">
    <span class="pill">About LFA Consulting</span>
    <h1>Helping you stay <span>compliant, organised &amp; financially confident.</span></h1>
    <p class="lead">An accounting, tax, advisory and immigration consultancy serving South Africa and Zimbabwe, built on clear pricing, personal service and doing things properly.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="founder-img reveal"><img src="images/lilian.jpg" alt="Lilian Ngubane, Founder and Principal of LFA Consulting"></div>
      <div class="reveal d1">
        <span class="kicker">Meet the founder</span>
        <h2>Lilian Ngubane</h2>
        <div class="sign">Founder &amp; Principal</div>
        <div class="creds-list"><span>Management Accountant</span><span>Master's in Business Leadership (MBL)</span><span>CIMA studies</span><span>Biblical studies</span></div>
        <p>Lilian founded LFA Consulting in 2025 to give small businesses, churches, non-profits and individuals the accountable, straight-talking support that larger firms often keep for their biggest clients.</p>
        <p>She handles every engagement personally, from a first company registration to a government grant report or a family visa application. Clients deal with the person doing the work.</p>
        <a href="contact.html" class="btn">Book a free call with Lilian <i data-icon="arrow"></i></a>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head reveal"><span class="kicker">What we stand for</span><h2>What clients value most</h2></div>
    <div class="why-grid">
      <div class="why-c reveal"><div class="icon-tile"><span class="ic" data-icon="badgecheck"></span></div><h3>Qualified &amp; accountable</h3><p>Led by a Management Accountant with a Master's in Business Leadership.</p></div>
      <div class="why-c reveal d1"><div class="icon-tile"><span class="ic" data-icon="rand"></span></div><h3>Clear, honest pricing</h3><p>Published starting prices and a written quote before any work begins.</p></div>
      <div class="why-c reveal d2"><div class="icon-tile"><span class="ic" data-icon="headset"></span></div><h3>Personal &amp; remote</h3><p>Everything can be done by WhatsApp, email and secure document sharing, anywhere in SA or Zimbabwe.</p></div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="sec-head reveal"><span class="kicker">Recent work</span><h2>The proof is in the work</h2></div>
    <div class="cases">{"".join(case_html(c, i) for i, c in enumerate(CASES[3:]))}</div>
    <div class="center"><a class="morelink" href="work.html">See all our work <i data-icon="arrow"></i></a></div>
  </div>
</section>
{CTA}'''
page("about.html", "About LFA Consulting — Founder Lilian Ngubane", "LFA Consulting is founder-led by Lilian Ngubane, Management Accountant (MBL), serving businesses, non-profits and individuals in South Africa and Zimbabwe.", about)

# ---------------------------------------------------------------- CONTACT
c = old_body("contact.html")
c = c.replace('<div class="cline"><div class="k" data-icon="globe"></div><a href="https://www.lfaconsulting.co.za">www.lfaconsulting.co.za</a></div>',
              '<div class="cline"><div class="k" data-icon="globe"></div><a href="tel:+263783238554">Zimbabwe: +263 78 323 8554</a></div>')
c = c.replace('<span>Serving clients nationwide · Remote available</span>', '<span>South Africa &amp; Zimbabwe · Fully remote</span>')
c = c.replace('<option>Company registration</option>', '<option>Company registration</option><option>Non-profit / church registration</option><option>Business plan or funding documents</option><option>Zimbabwe services</option>')
script = old_script("contact.html")
page("contact.html", "Contact LFA Consulting — Free Consultation", "Book a free 15–30 minute consultation with LFA Consulting by WhatsApp, phone or email.", c, script)

"""Build the animated SVG panels for the profile README from real data.

Reads analytics/activity.json and analytics/repositories.json (written by
update_analytics.py and build_dashboard.py) and writes:
  analytics/profile-pulse.svg     streak ring + key numbers
  analytics/profile-calendar.svg  full-year calendar with streaks highlighted
  analytics/profile-recent.svg    most recently updated repositories
No third-party services are used, so the README cannot show broken images.
"""
from pathlib import Path
from datetime import date, datetime, timezone, timedelta
from collections import Counter
from xml.sax.saxutils import escape
import json, math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analytics'
activity = json.loads((OUT / 'activity.json').read_text())
repos = [r for r in json.loads((OUT / 'repositories.json').read_text())['repos'] if not r.get('fork')]
days = [{'date': date.fromisoformat(d['date']), 'count': int(d['count'])} for d in activity['days']]
counts = [d['count'] for d in days]
fetched = datetime.fromisoformat(activity['fetched_at'].replace('Z', '+00:00'))

BG, SURF, LINE, TEXT, MUTED, DIM = '#0D1117', '#101B20', '#1F333A', '#E9F0ED', '#8DA3A8', '#5E767C'
MINT, TEAL, DEEP, AMBER = '#B5F5D2', '#63C8B5', '#2E7E6E', '#F4C77A'
HEAT = ['#16252B', '#1F4A44', '#2E7E6E', '#63C8B5', '#B5F5D2']
FONT = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'Cascadia Code',Consolas,monospace"

# ---------- facts ----------
def streak_runs(ds):
    runs, cur = [], None
    for i, d in enumerate(ds):
        if d['count'] > 0:
            if cur is None: cur = [i, i]
            else: cur[1] = i
        elif cur is not None:
            runs.append(tuple(cur)); cur = None
    if cur is not None: runs.append(tuple(cur))
    return runs

runs = streak_runs(days)
best = max(runs, key=lambda r: r[1] - r[0], default=(0, -1))
best_len = best[1] - best[0] + 1
k = len(days) - 1
if days[k]['count'] == 0: k -= 1          # today may still be in progress
cur_len, cur_start = 0, None
while k >= 0 and days[k]['count'] > 0:
    cur_len += 1; cur_start = days[k]['date']; k -= 1
total = sum(counts)
active = sum(1 for c in counts if c)
week = sum(counts[-7:]); prev_week = sum(counts[-14:-7])
best_day = max(days, key=lambda d: d['count'])
fmt = lambda d: d.strftime('%-d %b %Y') if hasattr(d, 'strftime') else str(d)
short = lambda d: d.strftime('%-d %b')

def card(w, h, body, title=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<style>
text{{font-family:{FONT}}}
.mono{{font-family:{MONO}}}
.fade{{animation:fade .8s ease both}}
@keyframes fade{{from{{opacity:0}}}}
.grow{{transform-box:fill-box;transform-origin:bottom;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}}
@keyframes grow{{from{{transform:scaleY(0)}}}}
.pop{{animation:pop .35s ease both}}
@keyframes pop{{from{{opacity:0}}}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{50%{{opacity:.35}}}}
@media (prefers-reduced-motion:reduce){{.fade,.grow,.pop{{animation:none;opacity:1;transform:none}}.pulse{{animation:none}}}}
</style>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{SURF}" stroke="{LINE}"/>
{body}
</svg>'''

# ---------- 1. pulse ----------
def pulse():
    W, H = 1120, 250
    r, cx, cy = 74, 150, 125
    circ = 2 * math.pi * r
    frac = min(1, cur_len / best_len) if best_len else 0
    off = circ * (1 - frac)
    ring = f'''<g transform="rotate(-90 {cx} {cy})">
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#16252B" stroke-width="12"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#rg)" stroke-width="12" stroke-linecap="round" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}">
<animate attributeName="stroke-dashoffset" from="{circ:.1f}" to="{off:.1f}" dur="1.4s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></circle></g>
<text x="{cx}" y="{cy+14}" text-anchor="middle" class="mono" font-size="54" font-weight="700" fill="{MINT}">{cur_len}</text>
<text x="{cx}" y="{cy+42}" text-anchor="middle" font-size="11" font-weight="600" letter-spacing="1.6" fill="{MUTED}">DAY STREAK</text>'''
    to_beat = best_len - cur_len + 1
    msg = 'New personal best, still running' if cur_len >= best_len else f'{to_beat} days to beat my record'
    since = f'since {short(cur_start)}' if cur_start else ''
    head = f'''<text x="270" y="62" font-size="11" font-weight="600" letter-spacing="1.6" fill="{MUTED}">CURRENT STREAK {('· ' + since.upper()) if since else ''}</text>
<text x="270" y="96" font-size="22" font-weight="600" fill="{TEXT}">{escape(msg)}</text>
<rect x="270" y="116" width="300" height="6" rx="3" fill="#16252B"/>
<rect x="270" y="116" width="0" height="6" rx="3" fill="{TEAL}"><animate attributeName="width" from="0" to="{300*frac:.0f}" dur="1.4s" fill="freeze"/></rect>
<text x="270" y="142" font-size="12" fill="{MUTED}" class="mono">{cur_len} / {best_len} days to personal best</text>'''
    wk_delta = '—' if prev_week == 0 else f"{'+' if week >= prev_week else '−'}{abs(round((week - prev_week) / prev_week * 100))}%"
    stats = [
        (f'{total:,}', 'CONTRIBUTIONS', 'past 12 months'),
        (f'{active}', 'ACTIVE DAYS', f'{round(active / len(days) * 100)}% of the year'),
        (f'{best_len}', 'LONGEST STREAK', f'{short(days[best[0]]["date"])} – {short(days[best[1]]["date"])}'),
        (f'{week}', 'LAST 7 DAYS', f'{wk_delta} vs previous week'),
    ]
    tiles = ''
    for i, (v, l, s) in enumerate(stats):
        x = 600 + (i % 2) * 255; y = 34 + (i // 2) * 98
        tiles += f'''<g class="fade" style="animation-delay:{.15 + i * .12:.2f}s"><rect x="{x}" y="{y}" width="240" height="86" rx="12" fill="{BG}" stroke="{LINE}"/>
<text x="{x+18}" y="{y+26}" font-size="10.5" font-weight="600" letter-spacing="1.4" fill="{MUTED}">{l}</text>
<text x="{x+18}" y="{y+60}" class="mono" font-size="28" font-weight="700" fill="{TEXT}">{v}</text>
<text x="{x+222}" y="{y+60}" text-anchor="end" font-size="11.5" fill="{MUTED}">{escape(s)}</text></g>'''
    today = days[-1]
    live = f'''<circle cx="278" cy="196" r="5" fill="{MINT if today['count'] else AMBER}" class="pulse"/>
<text x="292" y="200" font-size="12.5" fill="{TEXT}">{('Active today · ' + str(today['count']) + ' contributions') if today['count'] else 'No contribution yet today'}</text>
<text x="292" y="220" font-size="11" fill="{DIM}" class="mono">Updated {fetched.strftime('%-d %b %Y, %H:%M')} UTC · refreshed daily</text>'''
    defs = f'<defs><linearGradient id="rg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{MINT}"/></linearGradient></defs>'
    return card(W, H, defs + ring + head + live + tiles, f'Current GitHub streak {cur_len} days; longest {best_len} days; {total} contributions and {active} active days in the past year')

# ---------- 2. calendar ----------
def calendar():
    cs, gap = 14, 4
    pad = (days[0]['date'].weekday() + 1) % 7          # Sunday-first rows like GitHub
    cols = math.ceil((pad + len(days)) / 7)
    left, top = 54, 62
    W = left + cols * (cs + gap) + 30; H = 250
    mx = max(counts) or 1
    lvl = lambda c: 0 if c == 0 else min(4, math.ceil(c / mx * 4))
    in_streak = {}
    for a, b in runs:
        if (a, b) == best:
            for i in range(a, b + 1): in_streak[i] = (a, b) == best
    cells, months, last_m = '', '', None
    for i, d in enumerate(days):
        j = i + pad; c, r = divmod(j, 7)
        x, y = left + c * (cs + gap), top + r * (cs + gap)
        stroke = ''
        if i in in_streak:
            stroke = f' stroke="{AMBER if in_streak[i] else MINT}" stroke-width="{1.6 if in_streak[i] else .9}" stroke-opacity="{1 if in_streak[i] else .55}"'
        delay = c * 0.018
        cells += f'<rect class="pop" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{cs}" height="{cs}" rx="3" fill="{HEAT[lvl(d["count"])]}"{stroke}><title>{d["count"]} contributions on {fmt(d["date"])}</title></rect>'
        if r == 0 or i == 0:
            m = d['date'].month
            if m != last_m and (d['date'].day <= 7 or i == 0):
                months += f'<text x="{x}" y="{top-10}" font-size="11" fill="{MUTED}">{d["date"].strftime("%b")}</text>'; last_m = m
    today_i = len(days) - 1 + pad; tc, tr = divmod(today_i, 7)
    tx, ty = left + tc * (cs + gap), top + tr * (cs + gap)
    marker = f'<rect x="{tx-2.5}" y="{ty-2.5}" width="{cs+5}" height="{cs+5}" rx="5" fill="none" stroke="{TEXT}" stroke-width="1.4" class="pulse"/>'
    wd = ''.join(f'<text x="{left-12}" y="{top + r*(cs+gap) + 11}" text-anchor="end" font-size="10.5" fill="{DIM}">{n}</text>' for r, n in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')])
    head = f'''<text x="26" y="34" font-size="15" font-weight="600" fill="{TEXT}">{total:,} contributions · {active} active days</text>
<text x="{W-26}" y="34" text-anchor="end" font-size="11.5" fill="{MUTED}">{fmt(days[0]['date'])} – {fmt(days[-1]['date'])}</text>'''
    ly = top + 7 * (cs + gap) + 22
    legend = f'<text x="{left}" y="{ly+10}" font-size="11" fill="{MUTED}">Less</text>' + ''.join(f'<rect x="{left+32+i*16}" y="{ly}" width="12" height="12" rx="3" fill="{c}"/>' for i, c in enumerate(HEAT)) + f'<text x="{left+32+5*16+4}" y="{ly+10}" font-size="11" fill="{MUTED}">More</text>'
    key = f'''<rect x="{W-330}" y="{ly}" width="12" height="12" rx="3" fill="none" stroke="{AMBER}" stroke-width="1.6"/><text x="{W-312}" y="{ly+10}" font-size="11" fill="{MUTED}">Longest streak ({best_len} days)</text>
<rect x="{W-150}" y="{ly}" width="12" height="12" rx="3" fill="none" stroke="{TEXT}" stroke-width="1.4"/><text x="{W-132}" y="{ly+10}" font-size="11" fill="{MUTED}">Today</text>'''
    return card(W, H, head + months + wd + cells + marker + legend + key, f'Contribution calendar: {total} contributions over {len(days)} days with streaks highlighted')

# ---------- 3. recent + languages ----------
LC = {'Python': MINT, 'Jupyter Notebook': TEAL, 'HTML': '#87BBD7', 'Java': AMBER, 'JavaScript': '#E9D97A', 'R': '#9DB7F5'}
def ago(ts):
    dt = datetime.fromisoformat(ts.replace('Z', '+00:00')); d = (fetched - dt).total_seconds() / 86400
    if d < 1: return 'today'
    if d < 2: return 'yesterday'
    if d < 7: return f'{int(d)}d ago'
    if d < 30: return f'{int(d // 7)}w ago'
    return f'{int(d // 30)}mo ago'
def recent():
    W, H = 1120, 300
    rs = sorted([r for r in repos if r['name'].lower() != 'naveenvarma999'], key=lambda r: r['updated_at'], reverse=True)[:6]
    rows = f'<text x="26" y="40" font-size="15" font-weight="600" fill="{TEXT}">Recently shipped</text><text x="26" y="60" font-size="11.5" fill="{MUTED}">Latest updated public repositories</text>'
    for i, r in enumerate(rs):
        y = 84 + i * 34; lang = r['language'] or 'Other'
        rows += f'''<g class="fade" style="animation-delay:{i*.1:.2f}s"><line x1="26" x2="660" y1="{y-14}" y2="{y-14}" stroke="{LINE}"/>
<circle cx="34" cy="{y+2}" r="4.5" fill="{LC.get(lang, DIM)}"/><text x="48" y="{y+7}" class="mono" font-size="14" fill="{TEXT}">{escape(r['name'])}</text>
<text x="470" y="{y+7}" font-size="12" fill="{MUTED}">{escape(lang)}</text><text x="660" y="{y+7}" text-anchor="end" class="mono" font-size="12" fill="{MINT if ago(r['updated_at']) in ('today','yesterday') or ago(r['updated_at']).endswith('d ago') else MUTED}">{ago(r['updated_at'])}</text></g>'''
    cnt = Counter((r['language'] or 'Other') for r in repos).most_common(6); n = sum(v for _, v in cnt)
    x0, y0, bw = 720, 84, 370
    lang = f'<text x="{x0}" y="40" font-size="15" font-weight="600" fill="{TEXT}">Languages</text><text x="{x0}" y="60" font-size="11.5" fill="{MUTED}">Public repositories by primary language</text>'
    for i, (l, v) in enumerate(cnt):
        y = y0 + i * 34; w = max(4, bw * v / cnt[0][1])
        lang += f'''<text x="{x0}" y="{y}" font-size="12.5" fill="{TEXT}">{escape(l)}</text><text x="{x0+bw}" y="{y}" text-anchor="end" class="mono" font-size="12" fill="{MUTED}">{v} · {round(v/n*100)}%</text>
<rect x="{x0}" y="{y+7}" width="{bw}" height="7" rx="3.5" fill="#16252B"/><rect x="{x0}" y="{y+7}" width="0" height="7" rx="3.5" fill="{LC.get(l, DIM)}"><animate attributeName="width" from="0" to="{w:.0f}" dur="1s" begin="{.2+i*.08:.2f}s" fill="freeze"/></rect>'''
    return card(W, H, rows + lang, 'Recently updated repositories and language mix')

(OUT / 'profile-pulse.svg').write_text(pulse(), encoding='utf-8')
(OUT / 'profile-calendar.svg').write_text(calendar(), encoding='utf-8')
(OUT / 'profile-recent.svg').write_text(recent(), encoding='utf-8')
print(f'Profile SVGs: streak {cur_len}/{best_len}, {total} contributions, {active} active days')

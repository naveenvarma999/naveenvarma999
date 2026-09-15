"""Render real public GitHub activity. --cached uses the included snapshot."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone, date
from urllib.request import Request, urlopen
from PIL import Image, ImageDraw, ImageFont
import json, math, re, sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analytics'
OUT.mkdir(exist_ok=True)
USERNAME='naveenvarma999'
class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__();self.cells={};self.tips={};self.tip=None;self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='td' and 'data-date' in a:self.cells[a['id']]=a['data-date']
        if tag=='tool-tip':self.tip=a.get('for');self.text=[]
    def handle_data(self,data):
        if self.tip:self.text.append(data)
    def handle_endtag(self,tag):
        if tag=='tool-tip' and self.tip:
            self.tips[self.tip]=''.join(self.text).strip();self.tip=None
def fetch_calendar():
    req=Request(f'https://github.com/users/{USERNAME}/contributions',headers={'User-Agent':'GitHub-profile-analytics','Accept':'text/html'})
    with urlopen(req,timeout=60) as r:html=r.read().decode()
    p=CalendarParser();p.feed(html);days=[]
    for key,day in p.cells.items():
        text=p.tips.get(key,'');m=re.match(r'^(No|[\d,]+) contributions? on',text)
        if not m:raise RuntimeError('GitHub calendar format changed: '+text)
        count=0 if m[1]=='No' else int(m[1].replace(',',''))
        days.append({'date':day,'count':count})
    days.sort(key=lambda d:d['date'])
    if len(days)<300:raise RuntimeError('Incomplete contribution calendar; preserving previous images.')
    return {'username':USERNAME,'fetched_at':datetime.now(timezone.utc).isoformat(),'days':days}

data=json.loads((OUT/'activity.json').read_text()) if '--cached' in sys.argv else fetch_calendar()
days=data['days'];counts=[d['count'] for d in days];total=sum(counts);active=sum(c>0 for c in counts);peak=max(counts)
streak=best=0
for c in counts:
    streak=streak+1 if c else 0;best=max(streak,best)
BG='#080E12';FG='#F0F4F2';MINT='#B5F5D2';MUTED='#9AABA9';BORDER='#29403F'
def font(size,bold=False):
    candidates=[Path('C:/Windows/Fonts')/('segoeuib.ttf' if bold else 'segoeui.ttf'),Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in candidates:
        if p.exists():return ImageFont.truetype(str(p),size)
    return ImageFont.load_default(size=size)
def shell(title,subtitle,h):
    im=Image.new('RGB',(1120,h),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,1118,h-2),radius=18,outline=BORDER)
    d.text((34,23),'NAVEEN VARMA / GITHUB ANALYTICS',font=font(12,True),fill=MUTED)
    d.text((32,49),title,font=font(30,True),fill=FG)
    d.text((34,94),subtitle,font=font(13),fill=MUTED)
    return im

# Isometric calendar: height always encodes the actual daily count.
base=shell('A year of building. In perspective.',f"{days[0]['date']} to {days[-1]['date']}  |  {total:,} contributions  |  {active} active days",470)
nweeks=(len(days)+6)//7
frames=[]
for frame in range(60):
    im=base.copy();d=ImageDraw.Draw(im);phase=frame/60*math.tau
    tilt=.13+.01*math.sin(phase)
    def pt(w,r,h=0):return (116+w*16-r*10,195+w*16*tilt+r*8-h)
    scan=frame/60*nweeks
    for w in range(nweeks):
        for r in range(7):
            idx=w*7+r
            if idx>=len(days):continue
            c=counts[idx];height=2+(c/peak*95 if peak else 0)
            x,y=pt(w,r);a=(x,y-height);b=(x+12,y+12*tilt-height);cc=(x+5,y+12*tilt+5.6-height);e=(x-7,y+5.6-height)
            if c:
                intensity=.4+.6*c/peak
                top=tuple(int(k*intensity) for k in (181,245,210));side=(30,80,67);front=(47,121,96)
            else:top=(29,51,51);side=(15,28,31);front=(23,41,43)
            if abs(w-scan)<.7:top=(192,248,225) if c else (62,92,87)
            d.polygon([e,cc,(cc[0],cc[1]+height),(e[0],e[1]+height)],fill=front)
            d.polygon([b,cc,(cc[0],cc[1]+height),(b[0],b[1]+height)],fill=side)
            d.polygon([a,b,cc,e],fill=top)
    d.text((35,412),'Each bar = one day. Height = contribution count. Moving light is decorative.',font=font(12),fill=MUTED)
    d.text((35,439),'PUBLIC PROFILE CALENDAR  /  '+data['fetched_at'][:10],font=font(10),fill=MUTED)
    d.text((896,439),f'PEAK DAY / {peak}',font=font(10,True),fill=MINT)
    if frame==15:im.save(OUT/'contributions-3d.png')
    frames.append(im.quantize(colors=96))
frames[0].save(OUT/'contributions-3d.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1)

# Exact figures plus a weekly series for the most recent 26 complete/partial groups.
im=shell('Consistency, measured.', 'Public contribution activity, not a measure of code quality or skill.',410);d=ImageDraw.Draw(im)
for x,value,label in [(34,total,'CONTRIBUTIONS'),(300,active,'ACTIVE DAYS'),(566,best,'LONGEST STREAK / DAYS'),(832,peak,'MOST IN ONE DAY')]:
    d.text((x,137),f'{value:,}',font=font(37,True),fill=MINT)
    d.text((x,185),label,font=font(10,True),fill=MUTED)
recent=days[-182:];weekly=[sum(v['count'] for v in recent[i:i+7]) for i in range(0,len(recent),7)];mx=max(weekly) or 1
d.text((34,227),'RECENT ACTIVITY / 7-DAY TOTALS',font=font(11,True),fill=FG)
for k in [0,.5,1]:
    yy=350-85*k;d.line((34,yy,1045,yy),fill=BORDER);d.text((1050,yy-6),str(round(mx*k)),font=font(9),fill=MUTED)
for i,v in enumerate(weekly):
    x=38+i*38.5;top=350-v/mx*85
    if v:d.rounded_rectangle((x,top,x+23,350),radius=2,fill='#73D5BF')
d.text((34,367),recent[0]['date'],font=font(10),fill=MUTED)
d.text((934,367),recent[-1]['date'],font=font(10),fill=MUTED)
im.save(OUT/'activity-summary.png')
(OUT/'activity.json').write_text(json.dumps(data,indent=2)+'\n')
print(f'Rendered {len(days)} days, {total} contributions. GIF bytes: {(OUT/"contributions-3d.gif").stat().st_size}')

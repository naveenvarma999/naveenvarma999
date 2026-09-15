from pathlib import Path
from datetime import datetime,timezone,date
from urllib.request import Request,urlopen
from collections import Counter
from PIL import Image,ImageDraw,ImageFont
import json,math,sys,os

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analytics'
if '--cached' not in sys.argv:
    repos=[]
    for page in range(1,101):
        headers={'User-Agent':'NaveenProfileAnalytics','Accept':'application/vnd.github+json'}
        token=os.environ.get('GITHUB_TOKEN')
        if token:headers['Authorization']='Bearer '+token
        req=Request(f'https://api.github.com/users/naveenvarma999/repos?per_page=100&page={page}',headers=headers)
        with urlopen(req,timeout=60) as r:batch=json.load(r)
        repos.extend({'name':r['name'],'language':r['language'],'stars':r['stargazers_count'],'forks':r['forks_count'],'fork':r['fork'],'updated_at':r['updated_at'],'url':r['html_url']} for r in batch)
        if len(batch)<100:break
    else:raise RuntimeError('Repository pagination incomplete')
    (OUT/'repositories.json').write_text(json.dumps({'fetched_at':datetime.now(timezone.utc).isoformat(),'repos':repos},indent=2))
activity=json.loads((OUT/'activity.json').read_text());repository_data=json.loads((OUT/'repositories.json').read_text());repos=repository_data['repos'];days=activity['days'];counts=[d['count'] for d in days]
total=sum(counts);active=sum(c>0 for c in counts);best=streak=0
for c in counts:streak=streak+1 if c else 0;best=max(best,streak)
def f(n,b=False):
    for p in [Path('C:/Windows/Fonts')/('segoeuib.ttf' if b else 'segoeui.ttf'),Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf')]:
        if p.exists():return ImageFont.truetype(str(p),n)
    return ImageFont.load_default(size=n)
im=Image.new('RGB',(1120,890),'#090F13');d=ImageDraw.Draw(im)
fg='#E9F0ED';muted='#93A8AD';mint='#B5F5D2';teal='#63C8B5';line='#263A40';surface='#101C21'
def text(x,y,s,n=12,color=muted,b=False):d.text((x,y),str(s),font=f(n,b),fill=color)
def panel(x,y,w,h):d.rounded_rectangle((x,y,x+w,y+h),radius=12,fill=surface,outline=line)
text(30,23,'NV.  /  GITHUB OBSERVATORY',13,mint,True);text(820,26,'SNAPSHOT / '+activity['fetched_at'][:10],11)
text(28,61,'Every contribution tells a story.',34,fg,True)
text(30,109,'PUBLIC ACTIVITY   /   '+days[0]['date']+' — '+days[-1]['date'],12)
for x,v,title,sub in [(30,total,'CONTRIBUTIONS','Full displayed calendar'),(299,active,'ACTIVE DAYS',f'{active/len(days)*100:.1f}% of {len(days)} days'),(568,best,'LONGEST STREAK','Consecutive active days'),(837,len(repos),'PUBLIC REPOSITORIES','Account snapshot')]:
    panel(x,151,253,113);text(x+19,168,title,10);text(x+17,188,v,34,mint,True);text(x+19,235,sub,10)
panel(30,280,672,257);text(50,299,'Contribution momentum',17,fg,True);text(50,328,'Last 182 days / seven-day totals',11)
recent=days[-182:];weeks=[sum(x['count'] for x in recent[i:i+7]) for i in range(0,len(recent),7)];peak=max(weeks) or 1
for k in [0,.5,1]:
    y=486-k*120;d.line((50,y,674,y),fill=line);text(678,y-5,round(peak*k),8)
for i,c in enumerate(weeks):
    x=53+i*23.7;y=486-c/peak*120
    if c:d.rounded_rectangle((x,y,x+14,486),radius=2,fill=teal)
text(50,507,recent[0]['date'],9);text(602,507,recent[-1]['date'],9)
panel(718,280,372,257);text(738,299,'Repository language mix',17,fg,True);text(738,328,'Public repositories by primary language',11)
groups=Counter(r['language'] or 'Not classified' for r in repos).most_common();colors=[mint,teal,'#87BBD7','#5A8C9B','#546B79','#344B56'];start=-90
for i,(name,n) in enumerate(groups):
    end=start+n/max(1,len(repos))*360;d.arc((740,367,872,499),start,end,fill=colors[i%len(colors)],width=17);start=end
    yy=365+i*24;d.rounded_rectangle((893,yy+4,900,yy+11),radius=2,fill=colors[i%len(colors)]);text(910,yy,name,10);text(1060,yy,n,10,fg)
text(785,404,len(repos),29,fg,True);text(777,444,'REPOS',9)
panel(30,553,672,179);text(50,570,'The daily rhythm',17,fg,True);text(50,597,'Every day in the public calendar · darker cells indicate less activity',10)
maximum=max(counts) or 1;heat=['#1B2D32','#28554E','#388273',teal,mint]
for i,c in enumerate(counts):
    x=51+(i//7)*11.7;y=621+(i%7)*11;col=heat[min(4,math.ceil(c/maximum*4)) if c else 0];d.rounded_rectangle((x,y,x+8.5,y+8.5),radius=1,fill=col)
text(51,706,days[0]['date'],8);text(602,706,days[-1]['date'],8)
panel(718,553,372,179);text(738,570,'When activity happens',17,fg,True);text(738,597,'Contributions by weekday · full period',10)
weekday=[0]*7
for day in days:weekday[date.fromisoformat(day['date']).weekday()]+=day['count']
peak=max(weekday) or 1
for i,c in enumerate(weekday):
    x=744+i*48;y=695-c/peak*57;text(x+2,y-17,c,10,mint)
    if c:d.rounded_rectangle((x,y,x+25,695),radius=2,fill=teal)
    text(x,702,['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][i],9)
panel(30,749,1060,83);text(50,765,'EXPLORE THE INTERACTIVE DASHBOARD',12,mint,True);text(50,791,'Date filters  /  3D rotation  /  Daily inspection  /  CSV export',13,fg)
text(30,850,'Activity indicators, not code quality or proficiency. Language mix counts repositories, not bytes.',11)
text(30,870,'Source: github.com/naveenvarma999 · Updated by the included GitHub workflow after installation.',9)
im.save(OUT/'dashboard-overview.png')
bundle={'activity':activity,'repositories':repository_data}
payload=json.dumps(bundle).replace('<','\\u003c')
template=(ROOT/'dashboard/template.html').read_text(encoding='utf-8')
assert template.count('__DATA_JSON__')==1
(ROOT/'dashboard/index.html').write_text(template.replace('__DATA_JSON__',payload),encoding='utf-8')
print(f'Built dashboard for {len(days)} days / {total} contributions / {len(repos)} repositories')

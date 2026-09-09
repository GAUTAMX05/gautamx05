#!/usr/bin/env python3
import argparse,json,math,os,urllib.request
GREEN="#39D353"
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
def make(title,axes,dark=True):
    bg="#0d1117" if dark else "#ffffff"; fg="#e6edf3" if dark else "#24292f"; muted="#8b949e" if dark else "#57606a"
    cx,cy,r=300,255,175;n=len(axes); rings=[]; lines=[]; labels=[]
    for level in (25,50,75,100):
        p=[]
        for i in range(n):
            a=-math.pi/2+2*math.pi*i/n; rr=r*level/100;p.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
        rings.append(f'<polygon points="{" ".join(p)}" fill="none" stroke="{muted}" stroke-opacity=".35"/>')
    poly=[]
    for i,x in enumerate(axes):
        a=-math.pi/2+2*math.pi*i/n; rr=r*max(0,min(100,float(x["value"])))/100
        poly.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
        ex=cx+r*math.cos(a);ey=cy+r*math.sin(a)
        lx=cx+(r+34)*math.cos(a);ly=cy+(r+34)*math.sin(a)
        anchor="middle" if abs(math.cos(a))<.35 else ("start" if math.cos(a)>0 else "end")
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{muted}" stroke-opacity=".3"/>')
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{fg}" font-size="13" text-anchor="{anchor}" dominant-baseline="middle">{esc(x["label"])} — {x["value"]}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="510"><rect width="600" height="510" rx="18" fill="{bg}"/><text x="300" y="32" fill="{fg}" font-family="Arial" font-size="21" font-weight="700" text-anchor="middle">{esc(title)}</text>{"".join(rings)}{"".join(lines)}<polygon points="{" ".join(poly)}" fill="{GREEN}" fill-opacity=".22" stroke="{GREEN}" stroke-width="3"/>{"".join(labels)}</svg>'
def langs(user,limit,exclude):
    req=urllib.request.Request(f"https://api.github.com/users/{user}/repos?per_page=100&type=owner",headers={"User-Agent":"gautamx05"})
    with urllib.request.urlopen(req,timeout=20) as r: repos=json.load(r)
    totals={}
    for repo in repos:
        if repo.get("fork"): continue
        try:
            req=urllib.request.Request(repo["languages_url"],headers={"User-Agent":"gautamx05"})
            with urllib.request.urlopen(req,timeout=15) as r: data=json.load(r)
            for k,v in data.items():
                if k.lower() not in exclude: totals[k]=totals.get(k,0)+v
        except Exception: pass
    return sorted(totals.items(),key=lambda x:x[1],reverse=True)[:limit]
def main():
    p=argparse.ArgumentParser();p.add_argument("--data");p.add_argument("--github");p.add_argument("-o","--out",default="assets/radar");p.add_argument("--limit",type=int,default=7);p.add_argument("--values",action="store_true");p.add_argument("--curve",type=float,default=.4);p.add_argument("--exclude",default="");a=p.parse_args()
    if a.data:
        d=json.load(open(a.data,encoding="utf-8"))["axes"];base=a.out
        for dark in (True,False):open(f"{base}-{'dark' if dark else 'light'}.svg","w",encoding="utf-8").write(make("Skill Radar",d,dark))
    if a.github:
        xs=langs(a.github,a.limit,{x.strip().lower() for x in a.exclude.split(",") if x.strip()})
        mx=max([v for _,v in xs],default=1);d=[{"label":k,"value":round(100*(v/mx)**a.curve)} for k,v in xs]
        base=a.out
        for dark in (True,False):open(f"{base}-{'dark' if dark else 'light'}.svg","w",encoding="utf-8").write(make("GitHub Language Radar",d,dark))
if __name__=="__main__":main()

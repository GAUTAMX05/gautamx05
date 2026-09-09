#!/usr/bin/env python3
import argparse,os,urllib.request,json
p=argparse.ArgumentParser();p.add_argument("--user",required=True);p.add_argument("--out",default="assets");a=p.parse_args();os.makedirs(a.out,exist_ok=True)
try:
 req=urllib.request.Request(f"https://api.github.com/users/{a.user}",headers={"User-Agent":"gautamx05"})
 with urllib.request.urlopen(req,timeout=20) as r:u=json.load(r)
 text=f'Public repositories: {u.get("public_repos",0)} • Followers: {u.get("followers",0)} • GitHub: {a.user}'
except Exception:text=f'GitHub profile: {a.user}'
for d in (True,False):
 bg="#0d1117" if d else "#fff";fg="#e6edf3" if d else "#24292f"
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="230"><rect width="900" height="230" rx="18" fill="{bg}" stroke="#39D353"/><text x="40" y="55" fill="#39D353" font-family="Arial" font-size="26" font-weight="700">GitHub Metrics</text><text x="40" y="105" fill="{fg}" font-family="Arial" font-size="18">{text}</text><text x="40" y="165" fill="{fg}" font-family="Arial" font-size="15">Metrics refreshed by GitHub Actions.</text></svg>'
 open(f"{a.out}/metrics-calendar-{'dark' if d else 'light'}.svg","w").write(s)

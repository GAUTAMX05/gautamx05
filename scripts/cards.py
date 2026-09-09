#!/usr/bin/env python3
import argparse,json,os,urllib.request
def esc(s):return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
def svg(title,body,dark=True,w=760,h=240):
    bg="#0d1117" if dark else "#fff";fg="#e6edf3" if dark else "#24292f"
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="{w}" height="{h}" rx="18" fill="{bg}" stroke="#39D353"/><text x="30" y="52" fill="#39D353" font-family="Arial" font-size="25" font-weight="700">{esc(title)}</text><text x="30" y="98" fill="{fg}" font-family="Arial" font-size="16">{esc(body)}</text><text x="30" y="195" fill="#8b949e" font-family="Arial" font-size="13">Generated automatically for gautamx05</text></svg>'
def get(url):
    r=urllib.request.Request(url,headers={"User-Agent":"gautamx05"}); 
    with urllib.request.urlopen(r,timeout=20) as x:return json.load(x)
def main():
    p=argparse.ArgumentParser();p.add_argument("--user",required=True);p.add_argument("--out",default="assets");a=p.parse_args();os.makedirs(a.out,exist_ok=True)
    try:u=get(f"https://api.github.com/users/{a.user}");body=f'Public repos: {u.get("public_repos",0)} • Followers: {u.get("followers",0)} • Following: {u.get("following",0)}'
    except Exception:body=f'GitHub profile: {a.user}'
    for d in (True,False):open(f"{a.out}/stats-{'dark' if d else 'light'}.svg","w").write(svg("GitHub Stats",body,d))
    ps=json.load(open(f"{a.out}/projects.json",encoding="utf-8"))["projects"]
    for pr in ps:
        try:r=get(f'https://api.github.com/repos/{a.user}/{pr["repo"]}');body=f'{pr["description"]} • ★ {r.get("stargazers_count",0)} • Forks {r.get("forks_count",0)} • {r.get("language") or "Mixed"}'
        except Exception:body=pr["description"]
        for d in (True,False):open(f'{a.out}/card-{pr["repo"]}-{"dark" if d else "light"}.svg',"w").write(svg(pr["repo"],body,d,760,220))
if __name__=="__main__":main()

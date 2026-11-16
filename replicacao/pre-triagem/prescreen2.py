import json, re, sys, urllib.request, urllib.error

H = {"User-Agent": "research-prescreen", "Accept": "application/vnd.github+json"}

def get(url):
    req = urllib.request.Request(url, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.load(r), r.headers.get("Link", "")
    except urllib.error.HTTPError as e:
        return e.code, None, ""

_, rl, _ = get("https://api.github.com/rate_limit")
print("rate limit:", rl["resources"]["core"])

# (repo, branch) dos candidatos Java com >=3 contribuidores; spinnaker so commits
CAND = [("ewolff/microservice-consul", "master"), ("microservices-patterns/ftgo-application", "master"),
        ("Microservice-API-Patterns/LakesideMutual", "master"), ("ewolff/microservice", "master"),
        ("spring-petclinic/spring-petclinic-microservices", "main"),
        ("yidongnan/spring-cloud-netflix-example", "master"), ("spinnaker/spinnaker", "main")]

for r, b in CAND:
    st, c, link = get(f"https://api.github.com/repos/{r}/commits?sha={b}&per_page=1")
    m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
    n = int(m.group(1)) if m else (len(c) if c else None)
    print("COMMITS", r, st, n)

for r, b in CAND:
    if r == "spinnaker/spinnaker":
        continue
    st, items, _ = get(f"https://api.github.com/repos/{r}/contents?ref={b}")
    if items:
        print("ROOT", r, [i["name"] + ("/" if i["type"] == "dir" else "") for i in items])
    else:
        print("ROOT", r, st)

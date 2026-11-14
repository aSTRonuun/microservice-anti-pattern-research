import json, re, sys, urllib.request, urllib.error

OUT = sys.argv[1]
REPOS = """ewolff/microservice-consul
benwilcock/cqrs-microservice-sampler
venkataravuri/e-commerce-microservices-sample
gfawcett22/EnterprisePlanner
dotnet-architecture/eShopOnContainers
microservices-patterns/ftgo-application
Microservice-API-Patterns/LakesideMutual
lelylan/lelylan
fernandoabcampos/spring-netflix-oss-microservices
ewolff/microservice
DivanteLtd/open-loyalty
EdwinVW/pitstop
instana/robot-shop
JoeCao/qbike
spinnaker/spinnaker
zpng/spring-cloud-microservice-examples
spring-petclinic/spring-petclinic-microservices
yidongnan/spring-cloud-netflix-example
jferrater/Tap-And-Eat-MicroServices
mohamed-abdo/vehicle-tracking-microservices""".split()

H = {"User-Agent": "research-prescreen", "Accept": "application/vnd.github+json"}

def get(url):
    req = urllib.request.Request(url, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.load(r), r.headers.get("Link", "")
    except urllib.error.HTTPError as e:
        return e.code, None, ""

st, rl, _ = get("https://api.github.com/rate_limit")
core = rl["resources"]["core"]
print("rate limit:", core)
if core["remaining"] < 40:
    sys.exit("limite insuficiente")

res = {}
for r in REPOS:
    st, meta, _ = get(f"https://api.github.com/repos/{r}")
    row = {"status": st}
    if meta:
        row.update({k: meta.get(k) for k in
                    ("full_name", "archived", "fork", "language", "created_at",
                     "pushed_at", "default_branch", "license")})
        row["license"] = (meta.get("license") or {}).get("spdx_id")
    st2, c, link = get(f"https://api.github.com/repos/{r}/contributors?per_page=1&anon=true")
    m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
    row["contributors"] = int(m.group(1)) if m else (len(c) if c else None)
    res[r] = row
    print(r, row)

json.dump(res, open(OUT, "w"), indent=1)

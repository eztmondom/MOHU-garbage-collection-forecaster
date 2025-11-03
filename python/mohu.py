import json, requests
from bs4 import BeautifulSoup

BASE = "https://mohubudapest.hu/hulladeknaptar"
HEAD = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": BASE, "Origin": "https://mohubudapest.hu", "Accept": "*/*",
}
HU_MONTHS = {m:i+1 for i,m in enumerate(
    "január február március április május június július augusztus szeptember október november december".split())}

def pick_option(html, label):
    """Visszaadja az <option> value-t a megadott felirat alapján."""
    soup, labs = BeautifulSoup(html, "html.parser"), []
    norm = lambda s: s.lower().replace("–","-").replace("—","-").strip()
    for o in soup.select("option"):
        v,l = (o.get("value") or "").strip(), (o.text or "").strip()
        if not l: continue
        labs.append((v,l))
        if l==label or l.lower()==label.lower() or norm(label) in norm(l): return v or l
    raise RuntimeError(f"Nem találtam: '{label}'  minták: {labs}")

def extract_dates(text):
    data = json.loads(text)
    html = data.get("ajax/calSearchResults","")
    soup = BeautifulSoup(html, "html.parser")
    return [tds[1].text.strip()
            for tds in (tr.find_all("td") for tr in soup.select("tbody tr"))
            # if len(tds)>=3 and tds[2].select_one(".communal")]
            if len(tds)>=3 and tds[2].select_one(".selective")]

def fetch_szelektiv(district, street, house):
    with requests.Session() as s:
        s.get(BASE, timeout=15)
        def post(handler, part, data):
            r=s.post(BASE, headers={**HEAD,
                "X-OCTOBER-REQUEST-HANDLER":handler,
                "X-OCTOBER-REQUEST-PARTIALS":part}, data=data, timeout=15)
            r.raise_for_status(); return json.loads(r.text).get(part,"")

        streets = post("onSelectDistricts", "ajax/publicPlaces", {"district":district})
        houses  = post("onSavePublicPlace", "ajax/houseNumbers", {"district":district,"publicPlace":pick_option(streets,street)})
        html3   = s.post(BASE, headers={**HEAD,
                    "X-OCTOBER-REQUEST-HANDLER":"onSearch",
                    "X-OCTOBER-REQUEST-PARTIALS":"ajax/calSearchResults"},
                    data={"houseNumber":pick_option(houses,house)}, timeout=15).text
        return extract_dates(html3)

if __name__ == "__main__":
    dates = fetch_szelektiv("1062", "Andrássy", "57") # szelektív, kommunális
    print("Szelektív napok:", dates)

"""
MOHU Budapest selective waste calendar scraper.

This module provides utilities to query the public waste pickup calendar at
https://mohubudapest.hu/hulladeknaptar and extract upcoming garbage 
collection dates for a given district, street, and house number

Main entry point:
    - fetch_garbage(district, street, house) -> List[str]

The module parses the dynamic (AJAX) HTML fragments returned by the site and
collects the date strings found in the result table for garbage collections.
"""

import logging
import json, requests
from bs4 import BeautifulSoup

# --- Introductory log --------------------------------------------------------
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
logger.info("Loaded MOHU Budapest waste calendar scraper module.")

# --- Constants ----------------------------------------------------------------
BASE = "https://mohubudapest.hu/hulladeknaptar"
HEAD = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": BASE, "Origin": "https://mohubudapest.hu", "Accept": "*/*",
}
HU_MONTHS = {m:i+1 for i,m in enumerate(
    "január február március április május június július augusztus szeptember október november december".split())}


def pick_option(html, label):
    """
    Return the `<option>` value matching a human-readable label.

    The function parses an HTML snippet containing one or more `<option>` elements
    and tries to find the best match for the provided label. Matching is case-insensitive
    and tolerant to different dash characters (–, — replaced by -). If the `<option>`
    has an empty `value`, the visible text is returned as a fallback.

    Parameters
    ----------
    html : str
        HTML content that contains `<option>` elements (e.g., a `<select>` partial).
    label : str
        Human-readable label to match against the text of each `<option>`.

    Returns
    -------
    str
        The `value` attribute of the matching `<option>`; if not present, the option's text.

    Raises
    ------
    RuntimeError
        If no option could be matched to the given label. The error message includes
        a list of candidate (value, label) pairs to help with debugging.

    Examples
    --------
     >html = '<select><option value="123">Andrássy út</option></select>'
     >pick_option(html, "Andrássy")
     '123'
    """
    soup, labs = BeautifulSoup(html, "html.parser"), []
    norm = lambda s: s.lower().replace("–","-").replace("—","-").strip()
    for o in soup.select("option"):
        v,l = (o.get("value") or "").strip(), (o.text or "").strip()
        if not l: continue
        labs.append((v,l))
        if l==label or l.lower()==label.lower() or norm(label) in norm(l): return v or l
    raise RuntimeError(f"Nem találtam: '{label}'  minták: {labs}")

def extract_dates(text):
    """
    Extract selective collection date strings from an AJAX response.

    The MOHU site returns JSON with HTML partials. This function expects the raw
    response text (JSON), pulls out the "ajax/calSearchResults" partial, parses it,
    and collects date strings from the result table where the row corresponds to
    **selective** collection (identified by a `.selective` element in the 3rd column).

    Parameters
    ----------
    text : str
        Raw JSON response text from the MOHU search request.

    Returns
    -------
    list[str]
        A list of date strings (as displayed on the site), typically in Hungarian
        date format (e.g., "2025.01.12.").

    Notes
    -----
    The function intentionally filters to rows that contain a `.selective` element
    in the third table column. If you need **communal** pickup dates instead,
    adjust the selector condition accordingly (e.g., look for `.communal`).
    """
    data = json.loads(text)
    html = data.get("ajax/calSearchResults","")
    soup = BeautifulSoup(html, "html.parser")
    return [tds[1].text.strip()
            for tds in (tr.find_all("td") for tr in soup.select("tbody tr"))
            # if len(tds)>=3 and tds[2].select_one(".communal")]
            if len(tds)>=3 and tds[2].select_one(".selective")]

def fetch_garbage(district, street, house):
    """
    Fetch selective waste pickup dates for a given address in Budapest.

    This function emulates the interactive steps of the MOHU Budapest waste
    calendar:
      1) Load the main page to establish a session.
      2) POST the chosen district to get available public places (streets).
      3) POST the chosen street to get available house numbers.
      4) POST the chosen house number to retrieve the result table.
      5) Parse and return the selective pickup date strings.

    Parameters
    ----------
    district : str
        District code as expected by the site (e.g., "1062"). This is not always the
        simple district number; use the exact value seen in the website's `<option>`.
    street : str
        Street name (label) as seen on the site (e.g., "Andrássy").
        Partial matches are allowed (case-insensitive, dash-normalized).
    house : str
        House number (label) as seen on the site (e.g., "57").
        Partial matches are allowed.

    Returns
    -------
    list[str]
        List of selective collection date strings for the given address.

    Raises
    ------
    requests.HTTPError
        If any HTTP request returns a non-success status code.
    RuntimeError
        If the requested street or house cannot be matched among the returned options.

    Examples
    --------
    >fetch_garbage("1062", "Andrássy", "57")
    ['2025.01.12.', '2025.02.09.', ...]
    """
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
    logger.info("Running example query for selective collection dates...")
    dates = fetch_garbage("1062", "Andrássy", "57") # szelektív, kommunális
    print("Szelektív napok:", dates)
    logger.info("Found %d selective dates for the sample address.", len(dates))

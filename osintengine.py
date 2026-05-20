import os
import re
import requests
from urllib.parse import quote

try:
    from googlesearch import search
    googlesearchavailable = True
except ImportError:
    googlesearchavailable = False

def gatherallinfo(number):
    data = {}
    data["googleresults"] = searchphonenumber(number)
    data["sociallinks"] = buildsociallinks(number)
    return data

def searchphonenumber(phonenumber):
    if not googlesearchavailable:
        return ["install googlesearch python library for google results"]
    results = []
    try:
        for url in search(phonenumber, num_results=15):
            results.append(url)
    except Exception:
        results.append("google search failed")
    return results

def buildsociallinks(phonenumber):
    encoded = phonenumber.replace("+", "")
    links = {}
    links["facebook"] = f"https://www.facebook.com/search/top?q={encoded}"
    links["twitter"] = f"https://twitter.com/search?q={encoded}"
    links["instagram"] = f"https://www.instagram.com/web/search/top/?q={encoded}"
    links["linkedin"] = f"https://www.linkedin.com/search/results/all/?keywords={encoded}"
    links["tiktok"] = f"https://www.tiktok.com/search?q={encoded}"
    links["reddit"] = f"https://www.reddit.com/search/?q={encoded}"
    return links

def findipsforphonenumber(phonenumber):
    ipv4pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ipv6pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
    foundips = set()
    if googlesearchavailable:
        try:
            for url in search(phonenumber, num_results=10):
                try:
                    resp = requests.get(url, timeout=5)
                    if resp.status_code == 200:
                        text = resp.text
                        ipv4s = re.findall(ipv4pattern, text)
                        ipv6s = re.findall(ipv6pattern, text)
                        for ip in ipv4s + ipv6s:
                            if not ip.startswith("0.") and not ip.startswith("255."):
                                foundips.add(ip)
                except Exception:
                    pass
        except Exception:
            pass
    try:
        pastebinurl = f"https://pastebin.com/search?q={phonenumber}"
        resp = requests.get(pastebinurl, timeout=10)
        if resp.status_code == 200:
            pasteips = re.findall(ipv4pattern, resp.text)
            for ip in pasteips:
                if not ip.startswith("0."):
                    foundips.add(ip)
    except Exception:
        pass
    ipresults = {}
    ipresults["ipv4andv6"] = list(foundips) if foundips else ["no ips found for this phone number"]
    ipresults["note"] = "ips are extracted from public web pages and pastebin where the phone number appears together with an ip address"
    return ipresults

def opencagegeocode(locationname):
    if not locationname or locationname == "unknown":
        return {"error": "no location name to geocode"}
    apikey = "d207133943c7cb5c41b11784e517095d"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={quote(locationname)}&key={apikey}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results"):
                first = data["results"][0]
                return {
                    "formatted": first.get("formatted", ""),
                    "latitude": first["geometry"]["lat"],
                    "longitude": first["geometry"]["lng"],
                    "components": first.get("components", {}),
                    "confidence": first.get("confidence", 0)
                }
            else:
                return {"error": "no results found"}
        else:
            return {"error": f"api returned status {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

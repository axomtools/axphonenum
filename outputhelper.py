def printall(baseinfo, osintdata, ipaddresses, geodata):
    print("=" * 60)
    print("phone number basic information")
    print("=" * 60)
    for key, value in baseinfo.items():
        print(f"{key}: {value}")
    print("\n" + "=" * 60)
    print("opencage geocoding (location detail)")
    print("=" * 60)
    if "error" in geodata:
        print(f"geocoding error: {geodata['error']}")
    else:
        print(f"formatted address: {geodata.get('formatted', 'n/a')}")
        print(f"latitude: {geodata.get('latitude', 'n/a')}")
        print(f"longitude: {geodata.get('longitude', 'n/a')}")
        print(f"confidence: {geodata.get('confidence', 'n/a')}")
        components = geodata.get("components", {})
        if components:
            print("components:")
            for k, v in components.items():
                print(f"  {k}: {v}")
    print("\n" + "=" * 60)
    print("osint data")
    print("=" * 60)
    print("\ngoogle search results (first 15 urls):")
    for idx, url in enumerate(osintdata["googleresults"], 1):
        print(f"{idx}. {url}")
    print("\nsocial media search links (click to search on each platform):")
    for platform, link in osintdata["sociallinks"].items():
        print(f"{platform}: {link}")
    print("\n" + "=" * 60)
    print("attempted extraction of ip addresses for this phone number")
    print("=" * 60)
    print("note: " + ipaddresses["note"])
    print("\nfound ip addresses:")
    for ip in ipaddresses["ipv4andv6"]:
        print(f" - {ip}")

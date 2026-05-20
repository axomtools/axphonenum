
import sys
import phoneparser
import osintengine
import outputhelper

def main():
    print("phone number osint tool")
    number = input("enter phone number with country code (example: +1234567890): ").strip()
    if not number:
        print("error: no phone number entered")
        sys.exit(1)
    baseinfo = phoneparser.parsefull(number)
    if "error" in baseinfo:
        print("error:", baseinfo["error"])
        sys.exit(1)
    osintdata = osintengine.gatherallinfo(number)
    geodata = osintengine.opencagegeocode(baseinfo.get("location", ""))
    ipaddresses = osintengine.findipsforphonenumber(number)
    outputhelper.printall(baseinfo, osintdata, ipaddresses, geodata)

if __name__ == "__main__":
    main()

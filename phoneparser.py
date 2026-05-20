import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from phonenumbers.phonenumberutil import PhoneNumberType

def parsefull(numberstr):
    result = {}
    try:
        parsed = phonenumbers.parse(numberstr, None)
        if not phonenumbers.is_valid_number(parsed):
            result["error"] = "invalid phone number"
            return result
        result["international"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        result["national"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        result["e164"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        result["countrycode"] = parsed.country_code
        result["nationalnumber"] = parsed.national_number
        region = geocoder.region_code_for_number(parsed)
        result["region"] = region if region else "unknown"
        result["location"] = geocoder.description_for_number(parsed, "en")
        result["carrier"] = carrier.name_for_number(parsed, "en")
        tzones = timezone.time_zones_for_number(parsed)
        result["timezones"] = ", ".join(tzones) if tzones else "none"
        typ = phonenumbers.number_type(parsed)
        typemap = {
            PhoneNumberType.FIXED_LINE: "fixed line",
            PhoneNumberType.MOBILE: "mobile",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "fixed line or mobile",
            PhoneNumberType.TOLL_FREE: "toll free",
            PhoneNumberType.PREMIUM_RATE: "premium rate",
            PhoneNumberType.SHARED_COST: "shared cost",
            PhoneNumberType.VOIP: "voip",
            PhoneNumberType.PERSONAL_NUMBER: "personal number",
            PhoneNumberType.PAGER: "pager",
            PhoneNumberType.UAN: "uan",
            PhoneNumberType.VOICEMAIL: "voicemail"
        }
        result["linetype"] = typemap.get(typ, "unknown")
        result["valid"] = True
    except Exception as e:
        result["error"] = str(e)
    return result

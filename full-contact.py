from modules.apis.fullcontact import API
from modules.utils import colored, pprint
import argparse, sys


__doc__ = "Perform contact info queries against email-addresses, twitter usernames, phone numbers and domain and company names ..."

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("full-contact", description=__doc__)
    parser.add_argument("query", type=str, help="Search query.")
    parser.add_argument("-t", "--type", type=str, default="email", help="Query type (email, twitter, phone, domain or company; Default: email).")
    parser.add_argument("-k", "--api-key", type=str, default="978e7c52735a8420", help="FullContact API key.")
    args = parser.parse_args(args)
    
    api = API(args.api_key)
    resp = api.search(args.type, args.query)
    print(colored(f"[i] Showing Contact Info For {args.type.title()} Query {repr(args.query)}:"))
    print(colored(" -  Request ID/SC: {0[requestId]}/{0[status]}".format(resp), dark=True))
    if "likelihood" in resp:
        print(colored(f" -  Likelihood: {resp['likelihood']:0.2%}", dark=True))
        print("")
    else:
        if "message" in resp:
            print(colored(f" -  Message: {resp['message']}", "yellow", True))
            sys.exit()
    
    if "contactInfo" in resp:
        print(colored(" -  Contact Info:"))
        pprint(resp["contactInfo"], 1)
        print("")
    
    if "digitalFootprint" in resp:
        print(colored(" -  Digital Footprint:"))
        pprint(resp["digitalFootprint"], 1)
        print("")
    
    if "socialProfiles" in resp:
        print(colored(" -  Social Profiles:"))
        for profile in resp["socialProfiles"]:
            print(colored(f"    - {profile['typeName']}:"))
            for i in ["type", "typeId", "typeName"]:
                del profile[i]
            #for key, value in profile.items():
            #    print(colored(f"      - {key.title()}: {value}", dark=True))
            pprint(profile, 2)
            print("")
    
    for key in ["socialProfiles", "digitalFootprint", "contactInfo", "likelihood", "requestId", "status", "photos"]:
        if key in resp:
            del resp[key]
    pprint(resp)


if __name__ == "__main__":
    parse_args()

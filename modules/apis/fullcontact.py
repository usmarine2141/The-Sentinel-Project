from modules.session import Session
import urllib.parse



class API(Session):
    def __init__(self, api_key: str):
        super(API, self).__init__("https://api.fullcontact.com/v2/")
        self.session.headers["X-FullContact-APIKey"] = api_key
    
    def search(self, method: str, query: str):
        method = method.lower()
        query = urllib.parse.quote(query)
        if method in ["twitter", "phone", "email"]:
            url = "person.json?{}={}".format(method, query)
        elif method == "domain":
            url = "company/lookup.json?domain={}&keyPeople=true".format(query)
        else:
            url = "company/search.json?companyName={}".format(query)
        response = self.request("GET", url).json()
        return response
    
    def gen_card(self, method: str, query: str, out_file: str = None):
        method = method.lower()
        query = urllib.parse.quote(query)
        if method in ["twitter", "phone", "email"]:
            url = "person.html?{}={}".format(method, query)
        else:
            raise ValueError("Invalid search method {} .".format(repr(method)))
        page = self.request("GET", url).content
        soup = self.parse_html(page)
        open(out_file or (soup.title.text + ".html"), "wb").write(page)

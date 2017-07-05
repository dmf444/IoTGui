import re, requests, warnings
from six.moves import urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from gtts import gTTS


class gHTTS(gTTS):

    def get_google_url(self):
        for idx, part in enumerate(self.text_parts):
            payload = { 'ie' : 'UTF-8',
                        'q' : part,
                        'tl' : self.lang,
                        'ttsspeed' : self.speed,
                        'total' : len(self.text_parts),
                        'idx' : idx,
                        'client' : 'tw-ob',
                        'textlen' : self._len(part),
                        'tk' : self.token.calculate_token(part)}
            headers = {
                "Referer" : "http://translate.google.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
            }
            if self.debug:
                print(payload)
            try:
                # Disable requests' ssl verify to accomodate certain proxies and firewalls
                # Filter out urllib3's insecure warnings. We can live without ssl verify here
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
                    r = requests.get(self.GOOGLE_TTS_URL,
                                     params=payload,
                                     headers=headers,
                                     proxies=urllib.request.getproxies(),
                                     verify=False)
                if self.debug:
                    print("Headers: {}".format(r.request.headers))
                    print("Request url: {}".format(r.request.url))
                    print("Response: {}, Redirects: {}".format(r.status_code, r.history))
                r.raise_for_status()
                return r.request.url
            except Exception as e:
                raise e
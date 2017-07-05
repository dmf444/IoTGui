import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep
from backend.google.gTTShelper import gHTTS
import pychromecast as Cast
import urllib.parse as Parser


class GoogleHome:
    def __init__(self, home_name: str):
        # Save the device name, set a default to the device
        self._device_name = home_name
        self._device = None
        # Scan for new devices, this *should* be a new instance
        self.scan_for_device()

    def scan_for_device(self):
        """
        Perform a scan for the specific device name. Save it if possible
        :return: None
        """
        casts = Cast.get_chromecasts()
        for cast in casts:
            if (cast.device.friendly_name == self._device_name):
                self._device = cast

    def send_message(self, speech: str) -> bool:
        """
        Sends a .mp3 file to the google home for speaking. Parsed from Google's
        Text to Speech API.
        :param speech: string of 100 chars or less
        :return: True if message sent, false otherwise
        """
        # Follow the gTTS charater limit
        if (len(speech) <= gHTTS.MAX_CHARS):
            # Get a url from google
            tts = gHTTS(text=speech)
            url = tts.get_google_url()
            # Assuming the device has been set
            if (self._device is not None):
                # Send the url to the Google Home, which should play it
                self._device.media_controller.play_media(url, 'audio/mp3')
                # This seems to be needed to actually work
                sleep(5)
                return True
        return False

    def _build_listening_post(self):
        server_add = ('', 8080)
        self._httpd = HTTPServer(server_add, HomeListeningSever)
        self._httpd.gHome = self
        self._httpd.serve_forever()

    def start_server(self):
        self._thread = threading.Thread(name='daemon', target=self._build_listening_post)
        self._thread.setDaemon(True)
        self._thread.start()


class HomeListeningSever(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.wfile.write(bytes("<p>This webserver does noting with a GET request, please send a POST to alert your Google Home</p>", "utf-8"))

        # POST is for submitting data.

    def do_POST(self):
        # print("incomming http: ", self.path)
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        post_info = post_data.decode("utf-8")
        post_info = post_info.split("=")
        text = Parser.unquote_plus(post_info[1])
        print(text)
        self.server.gHome.send_message(text)
        self.send_response(200)
        self.wfile.write(self._headers_buffer[0] + bytes("POST RECIEVED", "utf-8"))


if(__name__ == "__main__"):
    import urllib.request as RQ
    from urllib.parse import urlencode
    home = GoogleHome("Kitchen Home")
    home.start_server()

    url = 'http://127.0.0.1:8080/' # Set destination URL here
    post_fields = {'text': 'Hello World, this is a listening station'}
    request = RQ.Request(url, urlencode(post_fields).encode("utf-8"))
    RQ.urlopen(request)
    sleep(25)

import re
import urllib.parse

ignore_ip = ""
ignored_urls = ["example.com", "etherx.jabber.org", "clientapi.ipip.net", "xmlsoap.org", "facebook.com", "fbcdn.net", "ytimg.com", "192.168.", "github.com", "inspici.com", "opensource.org"]

def find_urls(text):

    if ignore_ip in text:
        return set()

    text = text.replace("\\", "")
    text = text.replace(";", " ")
    text = text.replace("|", " ")

    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url_pattern = re.compile(url_regex, re.IGNORECASE)
    urls = [match[0] for match in url_pattern.findall(text)]

    to_remove = set()
    urls = set(urls)

    for string in ignored_urls:
        for url in urls:
            if string in url:
                to_remove.add(url)

    for url in urls:
        if ignore_ip in urls:
            to_remove.add(url)

    urls.difference_update(to_remove)


    return set(urls)


def bytes_to_string(byte_data, remove_invalid=True):
    try:
        if remove_invalid:
            return byte_data.decode('utf-8', errors='ignore')
        else:
            return byte_data.decode('utf-8')
    except UnicodeDecodeError as e:
        #print(e)
        return None

def decode_url(encoded_url):
    decoded_url = urllib.parse.unquote(encoded_url)
    return decoded_url

def extract_urls(msg_bytes):
    urls = set()
    msg_string = bytes_to_string(msg_bytes)

    if msg_string is not None:
        urls.update(find_urls(msg_string))
        msg_url_encoded = decode_url(msg_string)
        urls.update(find_urls(msg_url_encoded))


    return urls



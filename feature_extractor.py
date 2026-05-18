import re
from urllib.parse import urlparse
import tldextract

def extract_features(url):

    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    features = {}

    # 1
    features['having_IPhaving_IP_Address'] = -1 if re.match(r'\\d+\\.\\d+\\.\\d+\\.\\d+', domain) else 1

    # 2
    features['URLURL_Length'] = -1 if len(url) > 75 else 1

    # 3
    features['Shortining_Service'] = -1 if any(s in url for s in [
        'bit.ly',
        'tinyurl',
        'goo.gl',
        't.co'
    ]) else 1

    # 4
    features['having_At_Symbol'] = -1 if '@' in url else 1

    # 5
    features['double_slash_redirecting'] = -1 if url.rfind('//') > 7 else 1

    # 6
    features['Prefix_Suffix'] = -1 if '-' in domain else 1

    # 7
    subdomains = tldextract.extract(url).subdomain.split('.')
    features['having_Sub_Domain'] = -1 if len(subdomains) > 1 else 1

    # 8
    features['SSLfinal_State'] = 1 if parsed.scheme == 'https' else -1

    # 9
    features['Domain_registeration_length'] = -1 if len(domain) < 7 else 1

    # 10
    features['HTTPS_token'] = -1 if 'https' in domain else 1

    # 11
    features['Request_URL'] = -1 if len(path) > 50 else 1

    # 12
    features['URL_of_Anchor'] = -1 if '#' in url else 1

    # 13
    features['Links_in_tags'] = -1 if '%' in url else 1

    # 14
    features['SFH'] = -1 if 'login' in url.lower() else 1

    # 15
    features['Submitting_to_email'] = -1 if 'mailto:' in url else 1

    # 16
    features['Redirect'] = -1 if url.count('//') > 1 else 1

    # 17
    features['Iframe'] = -1 if 'iframe' in url.lower() else 1

    return features

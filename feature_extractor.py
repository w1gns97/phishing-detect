import re
from urllib.parse import urlparse
import tldextract

def extract_features(url):

    parsed = urlparse(url)
    domain = parsed.netloc

    features = {}

    features['having_IPhaving_IP_Address'] = -1 if re.match(r'\\d+\\.\\d+\\.\\d+\\.\\d+', domain) else 1
    features['URLURL_Length'] = -1 if len(url) >= 75 else 1
    features['Shortining_Service'] = -1 if any(s in url for s in ['bit.ly', 'tinyurl']) else 1
    features['having_At_Symbol'] = -1 if '@' in url else 1
    features['double_slash_redirecting'] = -1 if url.rfind('//') > 7 else 1
    features['Prefix_Suffix'] = -1 if '-' in domain else 1
    features['having_Sub_Domain'] = -1 if len(tldextract.extract(url).subdomain.split('.')) > 1 else 1
    features['SSLfinal_State'] = 1 if parsed.scheme == 'https' else -1

    return features

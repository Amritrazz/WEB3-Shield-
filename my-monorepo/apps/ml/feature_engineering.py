import re
import pandas as pd
import tldextract

HIGH_RISK_KEYWORDS = ['metamask', 'wallet', 'claim', 'airdrop', 'free', 'eth', 'secur', 'login', 'verify']

def extract_lexical_features(url: str) -> dict:
    url_clean = str(url).lower().strip()
    ext = tldextract.extract(url_clean)
    
    return {
        'url_length': len(url_clean),
        'domain_length': len(ext.domain),
        'qty_dots': url_clean.count('.'),
        'qty_hyphens': url_clean.count('-'),
        'qty_slashes': url_clean.count('/'),
        'has_subdomain': 1 if len(ext.subdomain) > 0 else 0,
        'is_ip_address': 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url_clean) else 0,
        'keyword_match_count': sum(1 for word in HIGH_RISK_KEYWORDS if word in url_clean)
    }

def transform_dataframe(df: pd.DataFrame, url_col: str) -> pd.DataFrame:
    feature_list = df[url_col].apply(extract_lexical_features).tolist()
    return pd.DataFrame(feature_list)
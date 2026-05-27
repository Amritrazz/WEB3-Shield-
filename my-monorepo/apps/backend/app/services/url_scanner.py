import re
import math
import tldextract
import httpx
from urllib.parse import urlparse
from collections import Counter

CRYPTO_BRANDS = [
    "metamask","coinbase","binance","opensea","uniswap",
    "aave","compound","phantom","trustwallet","ledger"
]

def url_entropy(url: str) -> float:
    freq = Counter(url)
    total = len(url)
    return -sum((c/total) * math.log2(c/total) for c in freq.values())

def lexical_similarity(domain: str) -> dict:
    """Check if domain looks like a spoofed crypto brand"""
    suspicious = []
    for brand in CRYPTO_BRANDS:
        if brand in domain and not domain.endswith(f"{brand}.io")            and not domain.endswith(f"{brand}.com"):
            suspicious.append(brand)
    return suspicious

async def scan_url(url: str) -> dict:
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    domain = ext.domain + "." + ext.suffix

    flags = []
    risk = 0

    # Feature 1: URL entropy (high = suspicious)
    entropy = url_entropy(url)
    if entropy > 4.5:
        flags.append("high_url_entropy"); risk += 10

    # Feature 2: URL length
    if len(url) > 100:
        flags.append("long_url"); risk += 5

    # Feature 3: Brand spoofing
    spoofed_brands = lexical_similarity(domain)
    if spoofed_brands:
        flags.append(f"brand_spoofing:{spoofed_brands[0]}"); risk += 40

    # Feature 4: Suspicious TLDs
    bad_tlds = [".xyz",".tk",".ml",".ga",".cf",".gq",".pw"]
    if any(url.endswith(t) for t in bad_tlds):
        flags.append("suspicious_tld"); risk += 15

    # Feature 5: IP address as host
    if re.match(r"https?://d+.d+.d+.d+", url):
        flags.append("ip_host"); risk += 20

    # Feature 6: Too many subdomains
    subdomains = ext.subdomain.split(".") if ext.subdomain else []
    if len(subdomains) > 3:
        flags.append("excessive_subdomains"); risk += 10

    # Feature 7: HTTPS check
    if not url.startswith("https://"):
        flags.append("no_https"); risk += 15

    verdict = "SAFE" if risk < 30 else "SUSPICIOUS" if risk < 60 else "PHISHING"

    return {
        "url": url,
        "domain": domain,
        "risk_score": min(risk, 100),
        "verdict": verdict,
        "flags": flags,
        "entropy": round(entropy, 2),
        "explanation": _explain(flags)
    }

def _explain(flags):
    msgs = {
        "high_url_entropy": "URL has unusually random character patterns",
        "long_url": "Abnormally long URL to hide the real domain",
        "brand_spoofing:metamask": "Domain impersonates MetaMask",
        "no_https": "Site not using HTTPS encryption",
        "ip_host": "Domain is a raw IP address, not a real website",
        "suspicious_tld": "Uses a free TLD commonly used by phishers",
    }
    parts = [msgs[f] for f in flags if f in msgs]
    return ". ".join(parts) if parts else "No issues detected."

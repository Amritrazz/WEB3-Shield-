from web3 import Web3
import requests
from app.config import settings

w3_eth = Web3(Web3.HTTPProvider(
    f"https://eth-mainnet.g.alchemy.com/v2/{settings.alchemy_api_key}"
))

MAX_UINT256 = 2**256 - 1

DANGEROUS_SELECTORS = {
    "ff": "SELFDESTRUCT opcode",
    "f4": "DELEGATECALL opcode",
    "3d": "RETURNDATACOPY opcode",
}

async def analyze_contract(address: str) -> dict:
    flags = []
    risk = 0
    try:
        code = w3_eth.eth.get_code(
            Web3.to_checksum_address(address)
        ).hex()
    except Exception:
        return {"error": "Could not fetch contract bytecode"}

    if code == "0x":
        return {"error": "Not a contract — this is a wallet address"}

    # Scan bytecode for dangerous opcodes
    for opcode, name in DANGEROUS_SELECTORS.items():
        if opcode in code:
            flags.append(f"opcode_{opcode}"); risk += 20

    # Fetch verified ABI from Etherscan
    abi = await _fetch_abi(address)
    if abi:
        func_names = [f.get("name","") for f in abi if f.get("type")=="function"]
        if "approve" in func_names:
            flags.append("has_approve"); risk += 5
        if "setApprovalForAll" in func_names:
            flags.append("has_setApprovalForAll"); risk += 10
        if "transferOwnership" in func_names:
            flags.append("has_transferOwnership"); risk += 15
            # Check contract age via Etherscan
    age = await _get_age(address)
    if age is not None and age < 7:
        flags.append("new_contract_7d"); risk += 15

    verdict = "SAFE" if risk < 30 else "MEDIUM_RISK" if risk < 60 else "HIGH_RISK"

    return {
        "address": address,
        "risk_score": min(risk, 100),
        "verdict": verdict,
        "flags": flags,
        "explanation": _explain(flags)
    }

async def decode_approval(tx_data: str) -> dict:
    """Decode approve(address,uint256) calldata"""
    if len(tx_data) < 10: return None
    sig = tx_data[2:10]
    if sig != "095ea7b3": return None  # approve() selector
    from eth_abi import decode as abi_decode
    spender, amount = abi_decode(
        ["address","uint256"],
        bytes.fromhex(tx_data[10:])
    )
    return {
        "type": "ERC20 approve",
        "spender": spender,
        "amount": str(amount),
        "is_unlimited": amount >= MAX_UINT256,
        "risk": "UNLIMITED APPROVAL — dangerous!" if amount >= MAX_UINT256 else "Limited approval"
    }

async def _fetch_abi(address: str):
    url = (f"https://api.etherscan.io/api?module=contract"
           f"&action=getabi&address={address}"
           f"&apikey={settings.etherscan_api_key}")
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if data["status"] == "1":
            import json
            return json.loads(data["result"])
    except: pass
    return None

async def _get_age(address: str):
    url = (f"https://api.etherscan.io/api?module=account"
           f"&action=txlist&address={address}&sort=asc"
           f"&page=1&offset=1&apikey={settings.etherscan_api_key}")
    try:
        from datetime import datetime
        r = requests.get(url, timeout=5)
        txs = r.json().get("result", [])
        if txs:
            ts = int(txs[0]["timeStamp"])
            age = (datetime.utcnow() - datetime.utcfromtimestamp(ts)).days
            return age
    except: pass
    return None

def _explain(flags):
    msgs = {
        "opcode_ff": "Contract can self-destruct, destroying all funds",
        "opcode_f4": "Uses DELEGATECALL — arbitrary code injection possible",
        "has_setApprovalForAll": "Can request unlimited NFT approvals",
        "new_contract_7d": "Deployed less than 7 days ago",
        "has_transferOwnership": "Admin can change contract owner at any time",
    }
    parts = [msgs[f] for f in flags if f in msgs]
    return ". ".join(parts) if parts else "No critical issues found."
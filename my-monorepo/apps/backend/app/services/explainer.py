import anthropic

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

async def explain_threat(scan_result: dict) -> str:
    """Generate a plain-English risk explanation for non-technical users"""

    prompt = f"""You are a Web3 security assistant. A user is about to interact with:

URL/Address: {scan_result.get('url') or scan_result.get('address')}
Risk Score: {scan_result.get('risk_score')}/100
Verdict: {scan_result.get('verdict')}
Flags detected: {', '.join(scan_result.get('flags', []))}

Write a 2-3 sentence plain-English warning for a non-technical crypto user.
- Explain the specific danger in simple words
- Say what they should NOT do
- Say what they SHOULD do instead
Be direct, not alarmist. Max 60 words."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

async def explain_transaction(decoded_tx: dict) -> str:
    """Explain what a smart contract call actually does"""

    prompt = f"""Explain this Ethereum transaction in 1-2 sentences for a non-technical user:
Function: {decoded_tx.get('type')}
Spender: {decoded_tx.get('spender')}
Amount: {decoded_tx.get('amount_human')}
Risk: {decoded_tx.get('risk')}

Keep it under 40 words. Say what permission is being granted and why it's risky."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
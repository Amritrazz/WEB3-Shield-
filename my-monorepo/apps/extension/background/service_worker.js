const API = 'http://localhost:8000/api/v1/scan/url';

async function getToken() {
  return new Promise(resolve => {
    chrome.storage.local.get('token', d => resolve(d.token));
  });
}

chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
  if (info.status !== 'complete') return;
  if (!tab.url || !tab.url.startsWith('http')) return;

  const token = await getToken();
  if (!token) return;

  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify({ url: tab.url })
    });
    const data = await res.json();
    const score = data.risk_score || 0;

    // Badge color + number
    const color = score > 70 ? '#dc2626'
                : score > 40 ? '#d97706'
                : '#16a34a';
    chrome.action.setBadgeBackgroundColor({tabId, color});
    chrome.action.setBadgeText({tabId, text: String(Math.round(score))});

    // Desktop notification for high-risk sites
    if (score > 80) {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/shield128.png',
        title: 'Web3 Shield Alert',
        message: 'Phishing site! Risk: ' + score + '/100 — ' + data.verdict
      });
    }
  } catch(e) {
    console.error('Web3Shield scan failed:', e);
  }
});
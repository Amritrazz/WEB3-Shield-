(function() {
  const API = 'http://localhost:8000/api/v1/scan';
  const TOKEN = /* get from chrome.storage */ null;

  if (!window.ethereum) return;

  const original = window.ethereum;
  window.ethereum = new Proxy(original, {
    get(target, prop) {
      if (prop !== 'request') return Reflect.get(target, prop);
      return async function(args) {
        const method = args.method;

        // Block unsigned approvals
        if (method === 'eth_sendTransaction') {
          const tx = args.params[0];

          // Check approval calldata
          if (tx.data && tx.data.startsWith('0x095ea7b3')) {
            const res = await fetch(`${API}/transaction`, {
              method: 'POST',
              headers: {'Content-Type':'application/json'},
              body: JSON.stringify(tx)
            }).then(r => r.json()).catch(() => null);

            if (res && res.risk_score > 70) {
              const ok = confirm(
                "Web3 Shield Warning!\n" +
                "Risk: " + res.risk_score + "/100\n" +
                res.explanation + "\n\nProceed anyway?"
              );
              if (!ok) throw new Error('Blocked by Web3 Shield');
            }
          }
        }
        return target.request(args);
      };
    }
  });
})();
'use client'
import { useEffect, useState } from 'react'

interface Alert { type: string; data: any; ts: string }

export function LiveFeed() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const ws = new WebSocket(
      `ws://localhost:8000/ws/threats?token=${token}`
    )
    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onmessage = (e) => {
      const alert = JSON.parse(e.data)
      setAlerts(prev => [alert, ...prev].slice(0, 50))
    }
    return () => ws.close()
  }, [])

  return (
    <div>
      <div style={{
        display:'flex', alignItems:'center', gap:8, marginBottom:12
      }}>
        <div style={{
          width:8, height:8, borderRadius:'50%',
          background: connected ? '#16a34a' : '#dc2626'
        }}/>
        <span style={{fontSize:13, color:'var(--color-text-secondary)'}}>
          {connected ? 'Live feed connected' : 'Disconnected'}
        </span>
      </div>
      {alerts.map((a, i) => (
        <div key={i} style={{
          padding:'10px 14px', marginBottom:6,
          borderRadius:8, border:'0.5px solid var(--color-border-tertiary)',
          background:'var(--color-background-secondary)',
          fontSize:13
        }}>
          <strong>{a.data.verdict}</strong> — {a.data.url || a.data.address}
          <span style={{
            float:'right', color:'var(--color-text-tertiary)', fontSize:11
          }}>{new Date(a.ts).toLocaleTimeString()}</span>
        </div>
      ))}
    </div>
  )
}

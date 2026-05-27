'use client';

import React, { useState } from 'react';
import { Shield, AlertOctagon, Radio, ShieldCheck, TrendingUp, Globe, Link2 } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock Analytics Timeline Data
const threatTrends = [
  { name: '00:00', attacks: 12 },
  { name: '04:00', attacks: 26 },
  { name: '08:00', attacks: 45 },
  { name: '12:00', attacks: 89 },
  { name: '16:00', attacks: 64 },
  { name: '20:00', attacks: 102 },
];

export default function DashboardPage() {
  const [scanUrl, setScanUrl] = useState('');
  
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {/* Top Header Panel */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6 mb-8">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            <Radio className="w-6 h-6 text-cyan-400 animate-pulse" />
            Threat Monitoring Command Center
          </h1>
          <p className="text-slate-400 text-sm mt-1">Real-time Web3 security vectors and system intelligence</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-xl text-xs font-mono flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
          <span className="text-slate-300">NODE STATUS: ACTIVE</span>
        </div>
      </header>

      {/* Real-time URL Fast-Scan Engine Row */}
      <section className="mb-8 bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-md">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-cyan-400 mb-3 flex items-center gap-2">
          <Link2 className="w-4 h-4" /> On-Demand URL Integrity Validation
        </h2>
        <div className="flex gap-3">
          <input 
            type="text"
            value={scanUrl}
            onChange={(e) => setScanUrl(e.target.value)}
            placeholder="Paste suspicious target URL endpoint here (e.g., https://metamask-drainer.xyz)..."
            className="flex-1 bg-slate-950 border border-slate-800 focus:border-cyan-500/50 text-sm rounded-xl px-4 py-3 text-white outline-none transition-all placeholder:text-slate-600"
          />
          <button className="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-medium px-6 py-3 rounded-xl shadow-lg shadow-cyan-950/20 text-sm transition-all">
            Execute Scan Matrix
          </button>
        </div>
      </section>

      {/* High-Level Analytical Stat Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
        <div className="bg-slate-900 border border-slate-800/60 rounded-xl p-5 flex items-center gap-4">
          <div className="bg-red-500/10 p-3 rounded-xl border border-red-500/20 text-red-400"><AlertOctagon className="w-6 h-6" /></div>
          <div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Malicious Vectors</p><h3 className="text-2xl font-bold mt-0.5 text-white">1,429</h3></div>
        </div>
        <div className="bg-slate-900 border border-slate-800/60 rounded-xl p-5 flex items-center gap-4">
          <div className="bg-cyan-500/10 p-3 rounded-xl border border-cyan-500/20 text-cyan-400"><Globe className="w-6 h-6" /></div>
          <div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Domains Crawled</p><h3 className="text-2xl font-bold mt-0.5 text-white">43,120</h3></div>
        </div>
        <div className="bg-slate-900 border border-slate-800/60 rounded-xl p-5 flex items-center gap-4">
          <div className="bg-emerald-500/10 p-3 rounded-xl border border-emerald-500/20 text-emerald-400"><ShieldCheck className="w-6 h-6" /></div>
          <div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Contracts Cleared</p><h3 className="text-2xl font-bold mt-0.5 text-white">8,914</h3></div>
        </div>
        <div className="bg-slate-900 border border-slate-800/60 rounded-xl p-5 flex items-center gap-4">
          <div className="bg-amber-500/10 p-3 rounded-xl border border-amber-500/20 text-amber-400"><TrendingUp className="w-6 h-6" /></div>
          <div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Avg Risk Index</p><h3 className="text-2xl font-bold mt-0.5 text-white">14.2%</h3></div>
        </div>
      </div>

      {/* Main Grid Content Area: Attack Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-base font-semibold text-white mb-6 tracking-tight">Active Phishing Exploit Volume (24h)</h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={threatTrends}>
                <defs>
                  <linearGradient id="colorAttacks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.4} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Area type="monotone" dataKey="attacks" stroke="#06b6d4" strokeWidth={2} fillOpacity={1} fill="url(#colorAttacks)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Live Attack Feed Block */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col">
          <h3 className="text-base font-semibold text-white mb-4 tracking-tight">Intercept Streams</h3>
          <div className="space-y-4 flex-1 overflow-y-auto max-h-[17.5rem] pr-2 custom-scrollbar">
            <div className="bg-slate-950 border-l-2 border-red-500 p-3.5 rounded-r-xl text-xs">
              <div className="flex justify-between font-mono text-slate-400 mb-1"><span>04:02:11 PM</span><span className="text-red-400 font-bold">CRITICAL</span></div>
              <p className="text-slate-200 truncate">Flagged Wallet Drainer: metamask-wallet-connect.xyz</p>
            </div>
            <div className="bg-slate-950 border-l-2 border-amber-500 p-3.5 rounded-r-xl text-xs">
              <div className="flex justify-between font-mono text-slate-400 mb-1"><span>03:55:48 PM</span><span className="text-amber-400 font-bold">HIGH</span></div>
              <p className="text-slate-200 truncate">Suspicious Reward Airdrop Link: free-eth-rewards.net</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
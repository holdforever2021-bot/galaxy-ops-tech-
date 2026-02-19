"""
Galaxy Digital - Operations Technology Implementation Roadmap
Demo dashboard for VP/Director Tech Lead - Operations Technology role
Run: python app.py
View: http://localhost:5001
"""

from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# ── Data ──────────────────────────────────────────────────────────────────────

WORKSTREAMS = [
    {"id": "wb", "name": "Trade Booking Modernization", "epic": "EPIC-01", "status": "In Progress", "progress": 65, "risk": "Low", "owner": "NY Team", "sprint": "Sprint 14", "stories_done": 18, "stories_total": 28, "target": "Q2 2026"},
    {"id": "ws", "name": "Settlement Workflow Automation", "epic": "EPIC-02", "status": "At Risk", "progress": 40, "risk": "High", "owner": "NY / HK", "sprint": "Sprint 14", "stories_done": 10, "stories_total": 25, "target": "Q3 2026"},
    {"id": "wr", "name": "Reconciliation Engine Rebuild", "epic": "EPIC-03", "status": "In Progress", "progress": 55, "risk": "Medium", "owner": "HK Team", "sprint": "Sprint 13", "stories_done": 14, "stories_total": 26, "target": "Q2 2026"},
    {"id": "wpt", "name": "Post-Trade Regulatory Reporting", "epic": "EPIC-04", "status": "On Track", "progress": 78, "risk": "Low", "owner": "NY Team", "sprint": "Sprint 14", "stories_done": 22, "stories_total": 28, "target": "Q1 2026"},
    {"id": "wdf", "name": "DeFi / On-Chain Integration", "epic": "EPIC-05", "status": "Planning", "progress": 18, "risk": "Medium", "owner": "NY / HK", "sprint": "Sprint 12", "stories_done": 4, "stories_total": 22, "target": "Q4 2026"},
    {"id": "wai", "name": "AI-Driven Exception Management", "epic": "EPIC-06", "status": "In Progress", "progress": 50, "risk": "Low", "owner": "NY Team", "sprint": "Sprint 14", "stories_done": 9, "stories_total": 18, "target": "Q3 2026"},
]

STORIES = {
    "wb": [
        {"id": "WB-101", "title": "Migrate equity swap booking from legacy FIX to API-native architecture", "status": "Done", "points": 8},
        {"id": "WB-102", "title": "Implement real-time trade capture validation rules for crypto asset classes", "status": "Done", "points": 5},
        {"id": "WB-103", "title": "Build cross-asset booking engine supporting tokenized securities", "status": "In Progress", "points": 13},
        {"id": "WB-104", "title": "UTI/UPI auto-generation at point of trade capture", "status": "In Progress", "points": 8},
        {"id": "WB-105", "title": "Event-driven booking notification to downstream settlement systems", "status": "To Do", "points": 8},
        {"id": "WB-106", "title": "24/7 booking availability for crypto markets (no end-of-day batch)", "status": "To Do", "points": 13},
    ],
    "ws": [
        {"id": "WS-201", "title": "Design smart contract settlement layer for on-chain asset transfers", "status": "In Progress", "points": 13},
        {"id": "WS-202", "title": "Integrate BNY Mellon custody API for automated settlement instructions", "status": "Done", "points": 8},
        {"id": "WS-203", "title": "Build T+1 settlement framework for tokenized securities (SEC mandate)", "status": "In Progress", "points": 13},
        {"id": "WS-204", "title": "Fails management workflow — automated escalation and resolution", "status": "Blocked", "points": 8},
        {"id": "WS-205", "title": "Cross-border settlement netting across NY and HK entities", "status": "To Do", "points": 13},
    ],
    "wr": [
        {"id": "WR-301", "title": "Rebuild intraday P&L reconciliation engine (replace overnight batch)", "status": "Done", "points": 13},
        {"id": "WR-302", "title": "Three-way recon: internal books vs prime broker vs custodian", "status": "In Progress", "points": 8},
        {"id": "WR-303", "title": "Automated break identification with ML-assisted root cause classification", "status": "In Progress", "points": 13},
        {"id": "WR-304", "title": "Crypto position reconciliation against on-chain wallet balances", "status": "To Do", "points": 13},
        {"id": "WR-305", "title": "DTCC GTR trade state reconciliation for regulatory reporting", "status": "Done", "points": 5},
    ],
    "wpt": [
        {"id": "WPT-401", "title": "CFTC Part 45 Phase 2 — UPI implementation and UAT sign-off", "status": "Done", "points": 13},
        {"id": "WPT-402", "title": "HKMA OTCR rewrite — ISO 20022 XML schema migration", "status": "Done", "points": 13},
        {"id": "WPT-403", "title": "Automated regulatory change monitoring via LLM alert system", "status": "In Progress", "points": 8},
        {"id": "WPT-404", "title": "EMIR Refit — 203-field XML schema rebuild and DTCC GTR integration", "status": "Done", "points": 13},
        {"id": "WPT-405", "title": "Digital asset reporting framework for SEC SBSD mandates", "status": "In Progress", "points": 8},
    ],
    "wdf": [
        {"id": "WDF-501", "title": "Evaluate on-chain settlement protocols (Ethereum, Solana, Avalanche) for ops fit", "status": "Done", "points": 8},
        {"id": "WDF-502", "title": "Design hybrid TradFi/DeFi reconciliation model for tokenized assets", "status": "In Progress", "points": 13},
        {"id": "WDF-503", "title": "Smart contract audit framework for operations risk sign-off", "status": "To Do", "points": 13},
        {"id": "WDF-504", "title": "DeFi liquidity pool integration for Galaxy's institutional prime brokerage", "status": "To Do", "points": 13},
    ],
    "wai": [
        {"id": "WAI-601", "title": "Deploy LLM-based exception triage — auto-classify breaks by severity", "status": "Done", "points": 8},
        {"id": "WAI-602", "title": "API regression testing framework — automated on every deployment", "status": "In Progress", "points": 8},
        {"id": "WAI-603", "title": "Build data-driven SLA monitoring with predictive breach alerting", "status": "In Progress", "points": 5},
        {"id": "WAI-604", "title": "Automated settlement instruction generation from confirmed trade data", "status": "To Do", "points": 13},
        {"id": "WAI-605", "title": "Integration test harness for 24/7 crypto ops — no manual regression", "status": "To Do", "points": 8},
    ],
}

RISKS = [
    {"id": "R-01", "workstream": "Settlement Automation", "description": "T+1 SEC mandate deadline pressure — BNY API integration delayed by 3 weeks", "severity": "Critical", "mitigation": "Parallel track: manual fallback process while API integration completes"},
    {"id": "R-02", "workstream": "DeFi Integration", "description": "Smart contract audit timeline uncertain — no approved vendor selected", "severity": "High", "mitigation": "RFP issued to 3 audit firms; decision expected Sprint 15"},
    {"id": "R-03", "workstream": "Reconciliation Engine", "description": "Crypto wallet reconciliation requires real-time blockchain node access — infra not provisioned", "severity": "High", "mitigation": "Helios data center node deployment scoped as dependency"},
    {"id": "R-04", "workstream": "Post-Trade Reporting", "description": "HKMA OTCR Phase 2 go-live Sept 2025 — HK team bandwidth constraint", "severity": "Medium", "mitigation": "NY team cross-trained; 2 engineers redeployed from Trade Booking"},
    {"id": "R-05", "workstream": "AI Exception Mgmt", "description": "LLM model accuracy on exotic derivatives exceptions below 85% threshold", "severity": "Medium", "mitigation": "Fine-tuning on historical break data; target 92% accuracy before production"},
]

STRATEGIC_PILLARS = [
    {
        "name": "Helios Data Centers",
        "icon": "🏗️",
        "status": "Expanding",
        "description": "3.5 GW capacity under development. 800 MW CoreWeave agreement. First phase 133 MW Q1 2026.",
        "ops_impact": "Blockchain node infrastructure for on-chain reconciliation. Low-latency crypto trade booking. 24/7 uptime requirements for global ops.",
        "initiatives": ["Crypto node provisioning for wallet recon", "24/7 ops infrastructure design", "Low-latency settlement routing"],
        "color": "#f59e0b"
    },
    {
        "name": "Institutional Markets",
        "icon": "🏦",
        "status": "Growing",
        "description": "$1.8B loan book. 1,600+ institutional counterparties. Trading, lending, derivatives, prime brokerage.",
        "ops_impact": "SIMM initial margin, SBSD regulatory reporting, cross-asset reconciliation at scale. CFTC/SEC/HKMA compliance infrastructure.",
        "initiatives": ["CFTC Part 45 UPI compliance", "AcadiaSoft SIMM integration", "Prime brokerage settlement automation"],
        "color": "#6366f1"
    },
    {
        "name": "GalaxyOne Retail",
        "icon": "📱",
        "status": "Launched",
        "description": "2,000+ stocks/ETFs, crypto. 4% APY on cash. 8% yield notes for accredited investors. Robinhood competitor.",
        "ops_impact": "High-volume retail trade processing. Real-time settlement at scale. Exception management for millions of transactions.",
        "initiatives": ["Retail trade booking at scale", "Real-time exception management", "Automated retail settlement"],
        "color": "#10b981",
        "demo_link": "https://galaxyone-demo.onrender.com"
    },
    {
        "name": "Blockchain & DeFi",
        "icon": "⛓️",
        "status": "Building",
        "description": "Alluvial Finance acquisition. Liquid Collective staking protocol. On-chain credit and tokenization of traditional assets.",
        "ops_impact": "TradFi-to-DeFi workflow migration. Smart contract settlement. On-chain reconciliation. Hybrid custody models.",
        "initiatives": ["On-chain settlement framework", "Tokenized asset reconciliation", "DeFi liquidity integration"],
        "color": "#8b5cf6"
    },
]

LIFECYCLE_STAGES = [
    {
        "stage": "Order Execution",
        "icon": "⚡",
        "tradfi": "FIX protocol to broker/exchange. Manual pre-trade checks. Single-asset OMS.",
        "defi": "API-native order routing. Automated pre-trade risk. Multi-asset + crypto OMS.",
        "systems": ["FIX Engine", "OMS", "Risk Pre-Check"],
        "status": "Migrating",
        "automation": 70
    },
    {
        "stage": "Trade Confirmation",
        "icon": "✅",
        "tradfi": "SWIFT/Telex confirmations. 24-48hr matching. Manual exception handling.",
        "defi": "Real-time electronic confirmation. Automated matching. UTI/UPI generation at point of confirm.",
        "systems": ["MarkitWire", "DTCC Confirm", "UTI Generator"],
        "status": "Complete",
        "automation": 90
    },
    {
        "stage": "Clearing",
        "icon": "🔄",
        "tradfi": "CCP clearing via CME/ICE. Manual margin calls. SIMM bilateral for uncleared.",
        "defi": "Smart contract clearing. Automated margin via AcadiaSoft API. Real-time SIMM calculation.",
        "systems": ["CME", "ICE", "AcadiaSoft SIMM"],
        "status": "In Progress",
        "automation": 60
    },
    {
        "stage": "Settlement",
        "icon": "💸",
        "tradfi": "T+2 batch settlement. SWIFT messages. Manual fails management.",
        "defi": "T+0/T+1 atomic settlement. On-chain delivery-vs-payment. Automated fails escalation.",
        "systems": ["SWIFT", "BNY Mellon", "DTC/DTCC"],
        "status": "In Progress",
        "automation": 45
    },
    {
        "stage": "Reconciliation",
        "icon": "🔍",
        "tradfi": "Overnight batch recon. Excel-based break management. Manual root cause.",
        "defi": "Real-time intraday recon. ML break classification. Automated resolution workflows.",
        "systems": ["Internal Recon Engine", "DTCC GTR", "Prime Broker Feeds"],
        "status": "Rebuilding",
        "automation": 55
    },
    {
        "stage": "Book of Records",
        "icon": "📚",
        "tradfi": "End-of-day position updates. Single-source ledger. Static reporting.",
        "defi": "Real-time position ledger. Multi-entity golden source. Blockchain-anchored audit trail.",
        "systems": ["Portfolio Management", "Risk System", "GL Integration"],
        "status": "Planned",
        "automation": 30
    },
]

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    total_stories = sum(w['stories_total'] for w in WORKSTREAMS)
    done_stories = sum(w['stories_done'] for w in WORKSTREAMS)
    on_track = sum(1 for w in WORKSTREAMS if w['status'] in ['On Track', 'Done'])
    at_risk = sum(1 for w in WORKSTREAMS if w['risk'] == 'High')
    return render_template('index.html',
        workstreams=WORKSTREAMS,
        total_stories=total_stories,
        done_stories=done_stories,
        on_track=on_track,
        at_risk=at_risk,
        risks=RISKS[:3],
        pillars=STRATEGIC_PILLARS
    )

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html', workstreams=WORKSTREAMS, stories=STORIES, risks=RISKS)

@app.route('/lifecycle')
def lifecycle():
    return render_template('lifecycle.html', stages=LIFECYCLE_STAGES)

@app.route('/strategy')
def strategy():
    return render_template('strategy.html', pillars=STRATEGIC_PILLARS)

@app.route('/automation')
def automation():
    return render_template('automation.html')

@app.route('/steerco')
def steerco():
    return render_template('steerco.html')

@app.route('/api/workstreams')
def api_workstreams():
    return jsonify(WORKSTREAMS)

@app.route('/api/risks')
def api_risks():
    return jsonify(RISKS)

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

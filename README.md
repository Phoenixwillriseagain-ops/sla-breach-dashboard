# SLA Breach Analysis Dashboard

A self-contained, drag-and-drop **SLA Breach Analysis Dashboard** for `V2-breaches.xlsx` files.  
Upload your file — the dashboard parses all 4 SLA sheets and renders interactive charts instantly, with **zero backend required**.

---

## 📁 Repository Structure

```
sla-breach-dashboard/
├── breach-dashboard.html   ← Main dashboard (open in any browser)
├── analysis.py             ← Python CLI analysis script
└── README.md               ← This file
```

---

## 🚀 How to Use

### Option A — Browser Dashboard (Recommended)

1. Open `breach-dashboard.html` in any modern browser (Chrome, Edge, Firefox, Safari)
2. Drag & drop your `V2-breaches.xlsx` file onto the upload area
3. Explore the interactive charts across 6 tabs

> **No server, no install, no Python.** 100% client-side using [SheetJS](https://sheetjs.com/) + [Chart.js](https://www.chartjs.org/)

### Option B — Python CLI Analysis

```bash
pip install pandas openpyxl rich
python analysis.py path/to/V2-breaches.xlsx
```

Outputs a text summary and saves CSVs per sheet to `./output/`.

---

## 📊 What the Dashboard Analyzes

The file is expected to contain these sheets:

| Sheet | SLA Type | Typical Records |
|-------|----------|-----------------|
| KSL-4 | Related Incident SLA | ~678 |
| KM-1 | Reopen SLA | ~676 |
| KSL-5a | Process Compliance SLA | ~95 |
| KM-2 | Assign Back SLA | ~7 |

### Key Metrics per Sheet

- **Total vs. Valid vs. Excluded** breaches
- **Weekly trend** (breach volume by calendar week)
- **Breach Reason** breakdown (Agent / Software / Hardware / etc.)
- **Language distribution** (ISO_Language)
- **Top Topics/Systems** (#SW#AWP, #SW#ISTA, etc.)
- **Priority split** (Low vs. Moderate)
- **KM-1**: Action distribution (Not related / Remote Session / Callback)
- **KSL-5a**: Detailed breach description types

---

## 🗂 Expected Column Names

The dashboard auto-maps by column name. Ensure your export preserves these headers:

```
Incident Ticket, DATE_CLOSE, Status, Queue, Priority, ISO_Language,
Tool, TOPIC, SLA_Code, SLA_N, Breach_Description, DATE_TIME_Breach,
Reason, Excluded, Week, Agent, BMS ID, Comment, Jira
```

> Columns not found are silently skipped — partial files still work.

---

## 💡 Customization

- **Add a new sheet**: extend the `sheets` array in the JS `handleFile()` function and call `buildSheet('NEW_SHEET', 'newprefix')`
- **Change color palette**: edit `PALETTES.primary` and `PALETTES.categorical` arrays in the `<script>` block
- **Dark/Light mode**: the toggle in the header persists across chart re-renders

---

## 🔧 Stack

| Layer | Technology |
|-------|------------|
| File parsing | [SheetJS (xlsx)](https://sheetjs.com/) v0.18 |
| Charts | [Chart.js](https://www.chartjs.org/) v4.4 |
| Fonts | [Google Fonts – Inter](https://fonts.google.com/specimen/Inter) |
| Styling | Vanilla CSS with design tokens (no framework) |
| Python analysis | pandas + openpyxl + rich |

---

## 📌 Changelog

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-05-21 | Initial release — 4 sheets, 6 tabs, dark/light mode |

---

*Built for operational SLA breach reporting. Drop issues or PRs for improvements.*

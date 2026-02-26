# 🎨 Coloring Books Prompts

A static web app for children's coloring-book prompt generation, with **category filtering + quick copy + Gemini redirect**.

> This project uses **TOON (Token-Oriented Object Notation)** as the primary data format.

---

## ✨ Features

- 🔍 **Instant search** (keyword-based filtering)
- 🗂️ **Category filters** (Animals, Fantasy, Vehicles, etc.)
- 📋 **One-click prompt copy**
- ✨ **Gemini integration** (opens optimized prompt in a new tab)
- 📱 **Responsive UI**
- 🧱 **No backend required** (fully static)

---

## 🧩 Tech Stack

- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Data:** TOON (`js/prompts_data.toon`) + backward-compatible fallback (`js/prompts_data.js`)
- **Data processing:** Python (pandas, etc.)
- **Testing:** Playwright-based smoke test (`test_app.py`)

---

## 📁 Project Structure

```text
Coloring Books Prompts/
├─ index.html
├─ README.md
├─ TOON_SPEC.md
├─ prompts_full.toon / prompts_full.json
├─ process_all_sheets.py
├─ convert_to_js.py
├─ translate_prompts.py
├─ toon_prompts.py
├─ test_app.py
├─ assets/
│  └─ icon.svg
├─ css/
│  └─ style.css
└─ js/
   ├─ app_new.js
   ├─ gemini-redirect.js
   ├─ prompts_data.toon
   └─ prompts_data.js   (fallback)
```

---

## 🚀 Quick Start

### 1) Run the project

Start a simple HTTP server in the project folder:

```bash
python -m http.server 8000
```

Open in browser:

```text
http://localhost:8000
```

### 2) Use the app

1. Open the page
2. Type in the search bar
3. Narrow by category
4. Click **Copy** to copy a prompt
5. Click **Generate** to open Gemini

---

## 🧪 Testing

Run smoke test:

```bash
python test_app.py
```

Headless mode (recommended):

```bash
HEADLESS=1 python test_app.py
```

Windows PowerShell example:

`$env:HEADLESS='1'; python test_app.py`

---

## 🗃️ Data Flow (TOON-First)

### Excel → TOON

- Source: `Coloring Books Prompts.xlsx`
- Script: `process_all_sheets.py`
- Primary output: `prompts_full.toon`
- Compatibility output: `prompts_full.json`

### TOON → Web data file

- Script: `convert_to_js.py`
- Primary output: `js/prompts_data.toon`
- Fallback output: `js/prompts_data.js`

### Translation

- Script: `translate_prompts.py`
- Input: `prompts_full.toon`
- Output: `prompts_bilingual.toon`

---

## 📐 TOON Notes

- TOON parser/encoder utilities: `toon_prompts.py`
- Strict parse rules: `TOON_SPEC.md`
- Frontend loads TOON first, then falls back to JS data if needed.

---

## 🎯 App Icon

- Icon file: `assets/icon.svg`
- Favicon is wired in `index.html`:
  - `<link rel="icon" type="image/svg+xml" href="assets/icon.svg">`

If the icon does not update immediately, do a hard refresh (**Ctrl+F5**) because of browser favicon cache.

---

## 🛠️ Development Notes

- Main app logic: `js/app_new.js`
- `js/app.js` may be a legacy/alternate flow
- If data is not visible due to cache, hard refresh (**Ctrl+F5**)

---

## 🤝 Contributing

1. Create a branch
2. Make your changes
3. Run smoke test
4. Commit + open PR

Recommended PR template sections:

- Summary of changes
- Affected files
- Test results
- Screenshots (if UI changed)

---

## 🌐 Documentation Language

This repository keeps `README.md` and user-facing project documentation in **English** by default.

---

## 📄 License

A license file may not be added yet. Before publishing, add a proper `LICENSE` file (for example: MIT).

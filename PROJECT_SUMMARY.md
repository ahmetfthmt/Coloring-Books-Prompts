# 🎨 Coloring Books Prompts - Project Summary

## 📋 Project Overview
**Coloring Books Prompts** is a web-based library designed to help users find and generate creative prompts for children's coloring books. The application hosts a large collection of prompts across various categories and integrates with Google Gemini for AI image generation.

## ✨ Key Features

### 1. 🔍 Search & Discovery
- **Smart Search**: Filter prompts by keywords (e.g., "bear forest").
- **Category Filters**: visual buttons with icons for categories like Animals 🐾, Vehicles 🚗, Fantasy ✨, etc.
- **Instant Filtering**: Real-time filtering without page reloads.

### 2. 🚀 Image Generation (Gemini Integration)
- **External Redirect**: Clicking "Generate" opens Google Gemini in a new tab.
- **Deep Linking**: On mobile devices, attempts to open the generic Gemini App; falls back to the web interface.
- **Prompt Optimization**: Automatically optimizes the prompt for coloring book style (black and white, clean lines) before sending it to Gemini.

### 3. 📋 User Utilities
- **Copy to Clipboard**: One-click button to copy the optimized prompt.
- **Responsive Design**: Fully optimized for Desktop, Tablet, and Mobile.
- **Bidirectional Scroll**: Smooth UI experience where the welcome screen reappears when scrolling up.

## 🛠️ Technology Stack
- **Frontend**: Pure HTML5, CSS3, JavaScript (Vanilla).
- **Icons**: FontAwesome 6.
- **Fonts**: Google Fonts (Outfit).
- **Data Storage**: Local JSON object (`prompts_data.js`).
- **No Backend Required**: Runs entirely in the browser (Static Web App).

## 📂 File Structure
- `index.html`: Main application structure and layout.
- `js/app_new.js`: Core logic for sorting, filtering, and UI interactions.
- `js/gemini-redirect.js`: Handles the logic for opening Gemini and optimizing prompts.
- `js/prompts_data.js`: Database file containing the prompt collection.

## 🚀 How to Use
1. **Browse**: Scroll through the grid or use category buttons.
2. **Search**: Type keywords to find specific subjects.
3. **Generate**: Click the **Generate** button on any card.
   - It will open Gemini with a pre-filled, optimized prompt.
   - Simply click "Create" or "Send" in Gemini to get your coloring page.
4. **Copy**: Click **Copy** to save the prompt to your clipboard for use in other tools (Midjourney, DALL-E, etc.).

---
*Project Status: Completed & Polished (v1.0)*

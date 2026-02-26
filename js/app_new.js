let promptsData = [];
let filteredPrompts = [];
let selectedCategory = '';
let searchDebounceId = null;

// Category icons mapping
const categoryIcons = {
    'animals': 'fa-solid fa-paw',
    'vehicles': 'fa-solid fa-car',
    'nature & landscape': 'fa-solid fa-tree',
    'food & treats': 'fa-solid fa-cookie-bite',
    'fantasy & magic': 'fa-solid fa-wand-sparkles',
    'seasons & weather': 'fa-solid fa-cloud-sun',
    'sports & activities': 'fa-solid fa-football',
    'people & professions': 'fa-solid fa-user-group',
    'art & design': 'fa-solid fa-palette',
    'indoor & home': 'fa-solid fa-house',
    'space & science': 'fa-solid fa-rocket',
    'special occasions': 'fa-solid fa-gift',
    'other': 'fa-solid fa-star'
};

// Helper: show toast (global)
window.showToast = function (message = 'Prompt copied to clipboard!', duration = 2500) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    // Optionally show message inside toast
    const icon = toast.querySelector('i');
    if (message && toast) {
        // simple animation
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), duration);
    }
};

// Helper: copy to clipboard (global)
window.copyToClipboard = function (text) {
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
        window.showToast('✅ Prompt copied to clipboard!', 2500);
    }).catch(err => {
        console.error('Copy failed', err);
        alert('Prompt copied: ' + text);
    });
};

function parseToonPrompts(text) {
    const lines = text.split(/\r?\n/).filter(line => line.trim() !== '');
    if (lines.length === 0) return [];

    const header = lines[0].trim();
    const headerMatch = header.match(/^prompts\[(\d+)([|\t]?)\]\{(.+)\}:$/);
    if (!headerMatch) {
        throw new Error('TOON header formatı geçersiz');
    }

    const expectedCount = Number(headerMatch[1]);
    const delimiter = headerMatch[2] || ',';
    const fields = splitToonRow(headerMatch[3], delimiter).map(decodeToonCell);

    if (fields.join('|') !== 'text|category|sheet') {
        throw new Error('TOON field seti beklenen formatta değil');
    }

    const rows = lines.slice(1);
    if (rows.length !== expectedCount) {
        throw new Error(`TOON satır sayısı uyuşmuyor. Beklenen ${expectedCount}, gelen ${rows.length}`);
    }

    return rows.map((row) => {
        const indent = row.length - row.trimStart().length;
        if (indent !== 2) {
            throw new Error('Strict mode: her satır 2 boşluk ile başlamalı');
        }

        const values = splitToonRow(row.trimStart(), delimiter).map(decodeToonCell);
        if (values.length !== fields.length) {
            throw new Error('Strict mode: satır kolon sayısı field sayısıyla eşleşmiyor');
        }

        return {
            text: values[0],
            category: values[1],
            sheet: values[2]
        };
    });
}

function splitToonRow(rowText, delimiter) {
    const cells = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < rowText.length; i++) {
        const ch = rowText[i];

        if (ch === '"') {
            current += ch;
            inQuotes = !inQuotes;
            continue;
        }

        if (ch === '\\' && inQuotes) {
            if (i + 1 >= rowText.length) {
                throw new Error('Geçersiz TOON escape');
            }
            current += ch + rowText[i + 1];
            i++;
            continue;
        }

        if (ch === delimiter && !inQuotes) {
            cells.push(current.trim());
            current = '';
            continue;
        }

        current += ch;
    }

    if (inQuotes) {
        throw new Error('Kapanmayan TOON quoted değer');
    }

    cells.push(current.trim());
    return cells;
}

function decodeToonCell(token) {
    if (token.length >= 2 && token[0] === '"' && token[token.length - 1] === '"') {
        const raw = token.slice(1, -1);
        return raw
            .replace(/\\n/g, '\n')
            .replace(/\\r/g, '\r')
            .replace(/\\t/g, '\t')
            .replace(/\\"/g, '"')
            .replace(/\\\\/g, '\\');
    }

    return token;
}

async function loadPromptsData() {
    try {
        const response = await fetch('js/prompts_data.toon?v=20260226', { cache: 'no-store' });
        if (!response.ok) {
            throw new Error(`TOON data yüklenemedi: ${response.status}`);
        }

        const text = await response.text();
        const parsed = parseToonPrompts(text);
        promptsData = parsed;
        filteredPrompts = [...promptsData];
        console.log(`✅ ${promptsData.length} prompts loaded from TOON`);
        return;
    } catch (error) {
        console.warn('⚠️ TOON yükleme başarısız, legacy fallback kullanılacak:', error);
    }

    const legacy = Array.isArray(window.promptsData) ? window.promptsData : [];
    if (legacy.length > 0) {
        promptsData = legacy;
        filteredPrompts = [...promptsData];
        console.log(`✅ ${promptsData.length} prompts loaded from legacy JS fallback`);
        return;
    }

    throw new Error('Ne TOON ne de legacy data kaynağı yüklenebildi');
}

// Filter prompts by category + query
function filterPrompts(searchInputEl, promptsGridEl, countEl) {
    const query = (searchInputEl.value || '').toLowerCase().trim();

    filteredPrompts = promptsData.filter(prompt => {
        const matchesCategory = !selectedCategory || prompt.category === selectedCategory;
        const matchesSearch = query === '' || prompt.text.toLowerCase().includes(query);
        return matchesCategory && matchesSearch;
    });

    renderPrompts(filteredPrompts, query, promptsGridEl, countEl);
}

// Render prompts into grid
function renderPrompts(items, query, promptsGridEl, countEl) {
    if (countEl) countEl.textContent = items.length;

    if (items.length === 0) {
        promptsGridEl.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 4rem 2rem;">
                <i class="fa-solid fa-search" style="font-size: 3rem; color: var(--text-muted); margin-bottom: 1rem;"></i>
                <h3>No prompts found</h3>
                <p style="color: var(--text-muted);">Try different keywords or category</p>
            </div>
        `;
        return;
    }

    promptsGridEl.innerHTML = '';
    const fragment = document.createDocumentFragment();

    for (const prompt of items) {
        fragment.appendChild(createPromptCard(prompt, query));
    }

    promptsGridEl.appendChild(fragment);
}

function createPromptCard(prompt, query) {
    const card = document.createElement('div');
    card.className = 'prompt-card';

    const category = document.createElement('div');
    category.className = 'card-category';
    category.textContent = prompt.category;

    const text = document.createElement('p');
    text.className = 'card-text';
    appendHighlightedText(text, prompt.text, query);

    const footer = document.createElement('div');
    footer.className = 'card-footer';

    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.innerHTML = '<i class="fa-solid fa-copy"></i> Copy';
    copyBtn.addEventListener('click', () => window.copyToClipboard(prompt.text));

    const generateBtn = document.createElement('button');
    generateBtn.className = 'generate-btn';
    generateBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate';
    generateBtn.addEventListener('click', () => window.generateWithPrompt(prompt.text));

    footer.appendChild(copyBtn);
    footer.appendChild(generateBtn);

    card.appendChild(category);
    card.appendChild(text);
    card.appendChild(footer);

    return card;
}

function appendHighlightedText(container, text, query) {
    if (!query) {
        container.textContent = text;
        return;
    }

    const q = query.toLowerCase();
    const source = text;
    const lower = source.toLowerCase();
    let start = 0;

    while (start < source.length) {
        const index = lower.indexOf(q, start);
        if (index === -1) {
            container.appendChild(document.createTextNode(source.slice(start)));
            break;
        }

        if (index > start) {
            container.appendChild(document.createTextNode(source.slice(start, index)));
        }

        const match = document.createElement('span');
        match.className = 'match';
        match.textContent = source.slice(index, index + q.length);
        container.appendChild(match);
        start = index + q.length;
    }
}

// Initialize app once DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    // DOM elements
    const welcomeScreen = document.getElementById('welcomeScreen');
    const mainApp = document.getElementById('mainApp');
    const searchInput = document.getElementById('searchInput');
    const promptsGrid = document.getElementById('promptsGrid');
    const categoryBtns = document.getElementById('categoryFilters');
    const countEl = document.getElementById('count');
    const resultsInfo = document.getElementById('resultsInfo');
    const appHeader = document.getElementById('appHeader');
    const appNameEl = document.getElementById('appName');

    // Safety: ensure elements exist
    if (!searchInput || !promptsGrid || !categoryBtns) {
        console.warn('Essential DOM elements missing - aborting init');
        return;
    }

    try {
        await loadPromptsData();
    } catch (error) {
        console.error(error);
        promptsGrid.classList.remove('hidden');
        promptsGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 4rem 2rem;">
                <i class="fa-solid fa-triangle-exclamation" style="font-size: 3rem; color: #ef4444; margin-bottom: 1rem;"></i>
                <h3>Data loading failed</h3>
                <p style="color: var(--text-muted);">TOON source could not be parsed.</p>
            </div>
        `;
        return;
    }

    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length >= 2) {
        const categoryCount = new Set(promptsData.map(p => p.category)).size;
        statNumbers[0].textContent = promptsData.length.toLocaleString('en-US');
        statNumbers[1].textContent = categoryCount.toString();
    }

    // Initialize categories
    function initializeCategories() {
        const categories = [...new Set(promptsData.map(p => p.category))];
        categoryBtns.innerHTML = '';
        categories.forEach((category, idx) => {
            const btn = document.createElement('button');
            btn.className = 'pill';
            btn.setAttribute('data-category', category);

            const iconClass = categoryIcons[category.toLowerCase()] || 'fa-solid fa-star';
            btn.innerHTML = `<i class="${iconClass}"></i> <span>${category.charAt(0).toUpperCase() + category.slice(1)}</span>`;

            // don't auto-select any category by default (no 'all' pill)
            if (selectedCategory && selectedCategory === category) {
                btn.classList.add('active');
            }

            btn.addEventListener('click', () => {
                document.querySelectorAll('.pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedCategory = category;
                filterPrompts(searchInput, promptsGrid, countEl);
            });

            categoryBtns.appendChild(btn);
        });
    }

    // Hide prompts/results initially
    promptsGrid.classList.add('hidden');
    if (resultsInfo) resultsInfo.classList.add('hidden');

    // Wire search input
    searchInput.addEventListener('input', (e) => {
        const q = e.target.value.trim();
        if (!q) {
            promptsGrid.classList.add('hidden');
            if (resultsInfo) resultsInfo.classList.add('hidden');
            if (countEl) countEl.textContent = '0';
            promptsGrid.innerHTML = '';
            return;
        }
        promptsGrid.classList.remove('hidden');
        if (resultsInfo) resultsInfo.classList.remove('hidden');

        if (searchDebounceId) {
            clearTimeout(searchDebounceId);
        }
        searchDebounceId = setTimeout(() => {
            filterPrompts(searchInput, promptsGrid, countEl);
        }, 200);
    });

    // Scroll effect: fade welcome screen slowly based on scroll and reveal main app
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // header scaling (subtle)
        const maxScroll = 500;
        const scrollPercent = Math.min(scrollTop / maxScroll, 1);
        if (appHeader) appHeader.style.transform = `scale(${1 - (scrollPercent * 0.03)})`;

        // welcome screen fade & translate
        if (welcomeScreen) {
            const fadeRange = Math.max(200, welcomeScreen.offsetHeight * 0.6);
            const p = Math.min(scrollTop / fadeRange, 1);
            welcomeScreen.style.opacity = String(Math.max(0, 1 - p));
            welcomeScreen.style.transform = `translateY(${p * -8}px)`;
            welcomeScreen.style.pointerEvents = p > 0.98 ? 'none' : 'auto';

            // reveal main app when faded away
            if (p > 0.95) {
                if (mainApp) {
                    mainApp.classList.add('active');
                    mainApp.style.pointerEvents = 'all';
                    mainApp.style.opacity = '1';
                }
            } else {
                if (mainApp) {
                    mainApp.classList.remove('active');
                    mainApp.style.pointerEvents = 'none';
                    mainApp.style.opacity = '';
                }
            }
        }

        // optional: if a visible appName exists (legacy), fade it a bit
        if (appNameEl) {
            const titleOpacity = 1 - (scrollPercent * 0.75);
            appNameEl.style.opacity = String(Math.max(0.15, titleOpacity));
            appNameEl.style.transform = `translateY(${scrollPercent * -8}px)`;
        }
    });

    // Pull-down (mobile) fade for app name
    let touchStartY = 0;
    let isPulling = false;
    const maxPull = 220;

    window.addEventListener('touchstart', (e) => {
        if ((window.pageYOffset || document.documentElement.scrollTop) <= 0) {
            touchStartY = e.touches[0].clientY;
            isPulling = true;
        }
    });

    window.addEventListener('touchmove', (e) => {
        if (!isPulling) return;
        const currentY = e.touches[0].clientY;
        const pull = Math.max(0, currentY - touchStartY);
        const pullPercent = Math.min(pull / maxPull, 1);
        if (welcomeScreen) {
            welcomeScreen.style.opacity = String(1 - pullPercent);
            welcomeScreen.style.transform = `translateY(${pullPercent * 8}px)`;
        } else if (appNameEl) {
            appNameEl.style.opacity = String(1 - pullPercent);
            appNameEl.style.transform = `translateY(${pullPercent * 8}px)`;
        }
    });

    window.addEventListener('touchend', () => {
        isPulling = false;
        if (welcomeScreen) {
            welcomeScreen.style.transition = 'opacity 300ms ease, transform 300ms ease';
            welcomeScreen.style.opacity = '';
            welcomeScreen.style.transform = '';
            setTimeout(() => { welcomeScreen.style.transition = ''; }, 350);
        } else if (appNameEl) {
            appNameEl.style.transition = 'opacity 300ms ease, transform 300ms ease';
            appNameEl.style.opacity = '';
            appNameEl.style.transform = '';
            setTimeout(() => { appNameEl.style.transition = ''; }, 350);
        }
    });

    // Initialize categories
    initializeCategories();

    console.log('✅ App initialized (DOM ready)');
});

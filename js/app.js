console.log("=== APP.JS BAŞLATILIYOR ===");

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM yüklendi!");

    // DOM Elements
    const grid = document.getElementById('promptsGrid');
    const searchInput = document.getElementById('searchInput');
    const categoryContainer = document.getElementById('categoryFilters');
    const countLabel = document.getElementById('count');
    const toast = document.getElementById('toast');

    console.log("DOM elementleri:", {
        grid: grid ? "✓" : "✗",
        searchInput: searchInput ? "✓" : "✗",
        categoryContainer: categoryContainer ? "✓" : "✗",
        countLabel: countLabel ? "✓" : "✗",
        toast: toast ? "✓" : "✗"
    });

    // Data from global scope (loaded via data.js)
    const allPrompts = window.promptsData || [];
    console.log("Yüklenen prompt sayısı:", allPrompts.length);

    if (allPrompts.length === 0) {
        console.error("❌ HATA: Hiç prompt yüklenemedi!");
        grid.innerHTML = '<p style="color: red;">HATA: Veri yüklenemedi!</p>';
        return;
    }

    // State
    let currentFilter = 'all';
    let searchQuery = '';

    // Initialize
    init();

    function init() {
        console.log("init() çalışıyor...");
        generateCategoryButtons();
        renderPrompts();
        setupEventListeners();
        console.log("init() tamamlandı!");
    }

    // --- Core Functions ---

    function generateCategoryButtons() {
        console.log("Kategoriler oluşturuluyor...");

        // Extract unique categories
        const categories = new Set();
        allPrompts.forEach(p => {
            if (p.category) categories.add(p.category);
        });

        console.log("Bulunan kategoriler:", Array.from(categories));

        // Create buttons
        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = 'pill';
            btn.dataset.category = cat;
            btn.textContent = cat;
            categoryContainer.appendChild(btn);
        });

        console.log("Kategori butonları eklendi:", categories.size + " adet");
    }

    function renderPrompts() {
        console.log("renderPrompts() çalışıyor...", { currentFilter, searchQuery });

        // Filter data
        const filtered = allPrompts.filter(item => {
            // 1. Category Filter
            const matchCategory = currentFilter === 'all' || item.category === currentFilter;

            // 2. Search Filter
            const matchSearch = !searchQuery ||
                item.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
                item.category.toLowerCase().includes(searchQuery.toLowerCase());

            return matchCategory && matchSearch;
        });

        console.log("Filtrelenmiş prompt sayısı:", filtered.length);

        // Update count
        countLabel.textContent = filtered.length;

        // Clear grid
        grid.innerHTML = '';

        // Generate Cards
        if (filtered.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">
                    <i class="fa-regular fa-folder-open" style="font-size: 3rem; margin-bottom: 16px; opacity: 0.5;"></i>
                    <p>No prompts found matching your criteria.</p>
                </div>
            `;
            return;
        }

        filtered.forEach(item => {
            const card = document.createElement('div');
            card.className = 'prompt-card';
            card.onclick = () => copyToClipboard(item.text);

            const categoryHTML = item.category ? `<div class="card-category">${escapeHtml(item.category)}</div>` : '';

            card.innerHTML = `
                <div>
                    ${categoryHTML}
                    <div class="card-text">${highlightMatch(escapeHtml(item.text), searchQuery)}</div>
                </div>
                <div class="card-footer">
                    <span class="copy-btn"><i class="fa-regular fa-copy"></i> Click to Copy</span>
                </div>
            `;

            grid.appendChild(card);
        });

        console.log("Kartlar oluşturuldu!");
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function highlightMatch(text, query) {
        if (!query) return text;
        const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`(${escapedQuery})`, 'gi');
        return text.replace(regex, '<span style="background: rgba(255, 255, 0, 0.3); font-weight: bold;">$1</span>');
    }

    function copyToClipboard(text) {
        console.log("Kopyalanıyor:", text.substring(0, 50) + "...");
        navigator.clipboard.writeText(text).then(() => {
            console.log("Kopyalama başarılı!");
            showToast();
        }).catch(err => {
            console.error('Kopyalama başarısız:', err);
        });
    }

    function showToast() {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);
    }

    function setupEventListeners() {
        console.log("Event listener'lar ekleniyor...");

        // Search Input
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.trim();
            console.log("Arama yapılıyor:", searchQuery);
            renderPrompts();
        });

        // Category Buttons delegation
        categoryContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('pill')) {
                console.log("Kategori tıklandı:", e.target.dataset.category);

                // Remove active class from all
                document.querySelectorAll('.pill').forEach(btn => btn.classList.remove('active'));

                // Add active to clicked
                e.target.classList.add('active');

                // Update state
                currentFilter = e.target.dataset.category;
                renderPrompts();
            }
        });

        console.log("Event listener'lar eklendi!");
    }
});

console.log("=== APP.JS YÜKLEME TAMAMLANDI ===");

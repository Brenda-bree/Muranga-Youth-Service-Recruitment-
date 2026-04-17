    (function() {
        // ============================================================
        // 1. SHARD OVERLAY ANIMATION (remove after load)
        // ============================================================
        window.addEventListener('load', () => {
            const overlay = document.querySelector('.shard-overlay');
            if (overlay) {
                setTimeout(() => {
                    overlay.style.opacity = '0';
                    setTimeout(() => {
                        overlay.style.display = 'none';
                    }, 600);
                }, 800);
            }
        });

        // ============================================================
        // 2. SCROLL SHRINK HEADER
        // ============================================================
        const header = document.querySelector('.sleek-header');
        if (header) {
            window.addEventListener('scroll', () => {
                if (window.scrollY > 50) {
                    header.classList.add('shrink');
                } else {
                    header.classList.remove('shrink');
                }
            });
        }

        // ============================================================
        // 3. USER DROPDOWN (profile menu)
        // ============================================================
        const profile = document.getElementById('userProfile');
        const dropdown = document.getElementById('dropdownMenu');
        if (profile && dropdown) {
            profile.addEventListener('click', (e) => {
                e.stopPropagation();
                dropdown.classList.toggle('show');
            });
            window.addEventListener('click', () => {
                dropdown.classList.remove('show');
            });
        }

        // ============================================================
        // 4. SIDEBAR TOGGLE (FIXED - no hiding of button)
        // ============================================================
        const openBtn = document.querySelector('.sleek-header .open-sidebar'); // only header button
        const sidebar = document.getElementById('adminSidebar');
        const closeBtn = document.getElementById('closeSidebar');
        const overlaySidebar = document.getElementById('sidebarOverlay');
        const mainContent = document.getElementById('mainContent');

        if (openBtn && sidebar && closeBtn && overlaySidebar) {
            function openSidebar() {
                sidebar.classList.add('open');
                overlaySidebar.classList.add('active');
                if (mainContent) mainContent.classList.add('shifted');
            }
            function closeSidebar() {
                sidebar.classList.remove('open');
                overlaySidebar.classList.remove('active');
                if (mainContent) mainContent.classList.remove('shifted');
            }
            openBtn.addEventListener('click', (e) => {
                e.preventDefault();
                openSidebar();
            });
            closeBtn.addEventListener('click', closeSidebar);
            overlaySidebar.addEventListener('click', closeSidebar);
        }

        // ============================================================
        // 5. NAME SEARCH WITH AJAX + KEYBOARD NAVIGATION
        // ============================================================
        const searchInput = document.getElementById('searchInput');
        const suggestionsDiv = document.getElementById('nameSuggestions');
        let currentSearchType = 'id';
        let debounceTimer;
        let selectedIndex = -1;
        let currentSuggestions = [];

        // Update when toggle changes
        document.querySelectorAll('input[name="search_type"]').forEach(radio => {
            radio.addEventListener('change', function() {
                currentSearchType = this.value;
                suggestionsDiv.innerHTML = '';
                selectedIndex = -1;
                currentSuggestions = [];
                const spinner = document.getElementById('searchSpinner');
                if (spinner) spinner.style.display = 'none';
                
                if (currentSearchType === 'name') {
                    searchInput.placeholder = 'Enter name (min 2 chars)';
                    searchInput.maxLength = 100;
                    searchInput.removeAttribute('pattern');
                } else {
                    searchInput.placeholder = 'Enter ID Number (9 digits)';
                    searchInput.maxLength = 9;
                    searchInput.pattern = '\\d{9}';
                }
            });
        });

        // Keyboard navigation for suggestions
        searchInput.addEventListener('keydown', function(e) {
            if (currentSearchType !== 'name') return;
            const items = document.querySelectorAll('.suggestion-item:not(.no-results)');
            if (items.length === 0) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
                updateHighlight(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                updateHighlight(items);
            } else if (e.key === 'Enter' && selectedIndex >= 0) {
                e.preventDefault();
                const selected = items[selectedIndex];
                if (selected) {
                    const details = {
                        name: selected.dataset.name,
                        gender: selected.dataset.gender,
                        size: selected.dataset.size,
                        phone: selected.dataset.phone,
                        cohort: selected.dataset.cohort
                    };
                    showRejectionCard(details);
                    searchInput.value = '';
                    suggestionsDiv.innerHTML = '';
                    selectedIndex = -1;
                    currentSuggestions = [];
                    const spinner = document.getElementById('searchSpinner');
                    if (spinner) spinner.style.display = 'none';
                }
            } else if (e.key === 'Escape') {
                suggestionsDiv.innerHTML = '';
                selectedIndex = -1;
                currentSuggestions = [];
            }
        });

        function updateHighlight(items) {
            items.forEach((item, idx) => {
                if (idx === selectedIndex) {
                    item.style.background = 'rgba(78, 205, 196, 0.4)';
                    item.scrollIntoView({ block: 'nearest' });
                } else {
                    item.style.background = '';
                }
            });
        }

        // Input handler with debounce
        searchInput.addEventListener('input', function() {
            if (currentSearchType !== 'name') {
                suggestionsDiv.innerHTML = '';
                selectedIndex = -1;
                currentSuggestions = [];
                const spinner = document.getElementById('searchSpinner');
                if (spinner) spinner.style.display = 'none';
                return;
            }
            
            const query = this.value.trim();
            if (query.length < 2) {
                suggestionsDiv.innerHTML = '';
                selectedIndex = -1;
                currentSuggestions = [];
                const spinner = document.getElementById('searchSpinner');
                if (spinner) spinner.style.display = 'none';
                return;
            }
            
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const spinner = document.getElementById('searchSpinner');
                if (spinner) spinner.style.display = 'flex';
                suggestionsDiv.innerHTML = '';
                selectedIndex = -1;
                currentSuggestions = [];
                
                fetch(`/search/names?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (spinner) spinner.style.display = 'none';
                        if (data.length === 0) {
                            suggestionsDiv.innerHTML = '<div class="suggestion-item no-results">No matches found</div>';
                            return;
                        }
                        currentSuggestions = data;
                        let html = '';
                        data.forEach(person => {
                            html += `<div class="suggestion-item" data-id="${person.id_number}" data-name="${person.name}" data-gender="${person.gender}" data-size="${person.size}" data-phone="${person.phone_number}" data-cohort="${person.cohort_number}">
                                        <strong>${escapeHtml(person.name)}</strong> (ID: ${person.id_number}) - Cohort ${person.cohort_number}
                                    </div>`;
                        });
                        suggestionsDiv.innerHTML = html;
                        
                        // Add click handlers to suggestions
                        document.querySelectorAll('.suggestion-item').forEach(item => {
                            item.addEventListener('click', function() {
                                const details = {
                                    name: this.dataset.name,
                                    gender: this.dataset.gender,
                                    size: this.dataset.size,
                                    phone: this.dataset.phone,
                                    cohort: this.dataset.cohort
                                };
                                showRejectionCard(details);
                                searchInput.value = '';
                                suggestionsDiv.innerHTML = '';
                                selectedIndex = -1;
                                currentSuggestions = [];
                                const spinner = document.getElementById('searchSpinner');
                                if (spinner) spinner.style.display = 'none';
                            });
                        });
                    })
                    .catch(error => {
                        if (spinner) spinner.style.display = 'none';
                        suggestionsDiv.innerHTML = '<div class="suggestion-item no-results">Error loading suggestions</div>';
                        console.error('Search error:', error);
                    });
            }, 300);
        });

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }

        function showRejectionCard(details) {
            const container = document.querySelector('.container');
            let resultDiv = container.querySelector('.result');
            if (!resultDiv) {
                resultDiv = document.createElement('div');
                container.appendChild(resultDiv);
            }
            resultDiv.className = 'result REJECTED';
            resultDiv.innerHTML = `
                <h2>REJECTED</h2>
                <p>${escapeHtml(details.name)} is already in Cohort ${escapeHtml(details.cohort)}.</p>
                <div class="details-card">
                    <h3>Registered Applicant Details</h3>
                    <div class="details-grid">
                        <div class="detail-item"><span class="detail-label">Full Name:</span><span class="detail-value">${escapeHtml(details.name)}</span></div>
                        <div class="detail-item"><span class="detail-label">Gender:</span><span class="detail-value">${escapeHtml(details.gender)}</span></div>
                        <div class="detail-item"><span class="detail-label">Size:</span><span class="detail-value">${escapeHtml(details.size)}</span></div>
                        <div class="detail-item"><span class="detail-label">Phone Number:</span><span class="detail-value">${escapeHtml(details.phone)}</span></div>
                        <div class="detail-item"><span class="detail-label">Cohort:</span><span class="detail-value">Cohort ${escapeHtml(details.cohort)}</span></div>
                    </div>
                </div>
            `;
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    })();

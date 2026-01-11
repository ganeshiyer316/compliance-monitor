// MCC Labels for human-readable industry names
const MCC_LABELS = {
    "6051": "Crypto - Digital Currency",
    "6211": "Securities Brokers/Dealers",
    "7995": "Gambling - Betting/Casino",
    "7994": "Video Game Arcades",
    "6012": "Financial Institutions",
    "6540": "POI Funding (BNPL)",
    "5999": "Miscellaneous Retail"
};

// Global state
let allItems = [];
let filteredItems = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    setupEventListeners();
});

// Load data from JSON
async function loadData() {
    try {
        const response = await fetch('data.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        allItems = data.items || [];
        filteredItems = [...allItems];

        // Update last updated timestamp
        updateLastUpdated(data.last_updated);

        // Populate MCC filter
        populateMCCFilter();

        // Render initial view
        renderItems();
        updateSummaryStats();

        // Hide loading
        document.getElementById('loading').style.display = 'none';

    } catch (error) {
        console.error('Error loading data:', error);
        showError(`Failed to load data: ${error.message}`);
    }
}

// Update last updated timestamp
function updateLastUpdated(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    let timeAgo;
    if (diffMins < 60) {
        timeAgo = `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffMins < 1440) {
        const hours = Math.floor(diffMins / 60);
        timeAgo = `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    } else {
        const days = Math.floor(diffMins / 1440);
        timeAgo = `${days} day${days !== 1 ? 's' : ''} ago`;
    }

    document.getElementById('lastUpdated').textContent = `Last updated: ${timeAgo}`;
}

// Populate MCC filter dropdown
function populateMCCFilter() {
    const mccFilter = document.getElementById('mccFilter');
    const mccs = new Set();

    allItems.forEach(item => {
        const itemMccs = parseJSON(item.mccs);
        if (Array.isArray(itemMccs)) {
            itemMccs.forEach(mcc => mccs.add(mcc.toString()));
        }
    });

    // Sort and create options
    Array.from(mccs).sort().forEach(mcc => {
        const label = MCC_LABELS[mcc] || `MCC ${mcc}`;
        const option = document.createElement('option');
        option.value = mcc;
        option.textContent = `${label} (${mcc})`;
        mccFilter.appendChild(option);
    });
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('mccFilter').addEventListener('change', applyFilters);
    document.getElementById('regionFilter').addEventListener('change', applyFilters);
    document.getElementById('impactFilter').addEventListener('change', applyFilters);
    document.getElementById('searchInput').addEventListener('input', applyFilters);
}

// Apply all filters
function applyFilters() {
    const mccFilter = document.getElementById('mccFilter').value;
    const regionFilter = document.getElementById('regionFilter').value;
    const impactFilter = document.getElementById('impactFilter').value;
    const searchQuery = document.getElementById('searchInput').value.toLowerCase();

    filteredItems = allItems.filter(item => {
        // MCC filter
        if (mccFilter) {
            const itemMccs = parseJSON(item.mccs);
            if (!itemMccs || !itemMccs.includes(mccFilter)) {
                return false;
            }
        }

        // Region filter
        if (regionFilter) {
            const regions = parseJSON(item.regions);
            if (!regions || !regions.includes(regionFilter)) {
                return false;
            }
        }

        // Impact filter
        if (impactFilter && item.impact_level !== impactFilter) {
            return false;
        }

        // Search filter
        if (searchQuery) {
            const searchableText = `${item.title} ${item.summary}`.toLowerCase();
            if (!searchableText.includes(searchQuery)) {
                return false;
            }
        }

        return true;
    });

    renderItems();
    updateSummaryStats();
}

// Render compliance items
function renderItems() {
    const container = document.getElementById('itemsContainer');
    const emptyState = document.getElementById('emptyState');

    if (filteredItems.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';

    container.innerHTML = filteredItems.map(item => createItemCard(item)).join('');

    // Attach toggle listeners
    document.querySelectorAll('.requirements-toggle').forEach(toggle => {
        toggle.addEventListener('click', toggleRequirements);
    });
}

// Create item card HTML
function createItemCard(item) {
    const impactLevel = item.impact_level || 'low';
    const title = item.title || 'Untitled';
    const summary = item.summary || 'No summary available';
    const deadline = item.deadline || '';

    // Format deadline
    const deadlineText = deadline ? formatDeadline(deadline) : 'No deadline';

    // Format MCCs
    const mccs = parseJSON(item.mccs);
    const mccsText = formatMCCs(mccs);

    // Format regions
    const regions = parseJSON(item.regions);
    const regionsText = regions && regions.length ? regions.join(', ') : 'N/A';

    // Format transaction types
    const transactionTypes = parseJSON(item.transaction_types);
    const transactionTypesText = transactionTypes && transactionTypes.length ? transactionTypes.join(', ') : 'N/A';

    // Technical requirements
    const techReqs = parseJSON(item.technical_requirements);
    const techReqsHTML = techReqs && techReqs.length ? `
        <div class="requirements-toggle" data-item-id="${item.id || Math.random()}">
            <h4>📋 Technical Requirements (${techReqs.length})</h4>
            <span class="icon">▼</span>
        </div>
        <div class="requirements-content">
            <ul>
                ${techReqs.map(req => `<li>${req}</li>`).join('')}
            </ul>
        </div>
    ` : '';

    // Relevance score
    const relevance = item.relevance_score || 'N/A';

    // Source
    const sourceName = item.source_name || 'Unknown';
    const url = item.source_url || '#';

    return `
        <div class="item ${impactLevel}">
            <div class="item-header">
                <h2 class="item-title">${title}</h2>
                <span class="priority-badge ${impactLevel}">${impactLevel.toUpperCase()}</span>
            </div>

            <div class="item-meta">
                <div class="meta-item">
                    <span class="meta-label">Deadline:</span>
                    <span class="deadline">${deadlineText}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">MCCs:</span> ${mccsText}
                </div>
                <div class="meta-item">
                    <span class="meta-label">Regions:</span> ${regionsText}
                </div>
                <div class="meta-item">
                    <span class="meta-label">Transaction Types:</span> ${transactionTypesText}
                </div>
            </div>

            <div class="summary-text">
                ${summary}
            </div>

            ${techReqsHTML}

            <div>
                <span class="relevance-score">Relevance: ${relevance}/10</span>
            </div>

            <div style="margin-top: 1rem;">
                <span class="meta-label">Source:</span>
                <a href="${url}" class="source-link" target="_blank" rel="noopener noreferrer">${sourceName}</a>
            </div>
        </div>
    `;
}

// Format deadline with ordinal suffix
function formatDeadline(dateString) {
    try {
        const date = new Date(dateString);
        const day = date.getDate();
        const month = date.toLocaleString('en-GB', { month: 'long' });
        const year = date.getFullYear();

        const suffix = getDaySuffix(day);

        // Calculate days remaining
        const now = new Date();
        const diffTime = date - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        const daysText = diffDays > 0 ? ` (${diffDays} days)` : ' (Past due)';

        return `${day}${suffix} ${month} ${year}${daysText}`;
    } catch (e) {
        return dateString;
    }
}

// Get day suffix (1st, 2nd, 3rd, etc.)
function getDaySuffix(day) {
    if (day > 3 && day < 21) return 'th';
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}

// Format MCCs with labels
function formatMCCs(mccs) {
    if (!mccs || !Array.isArray(mccs) || mccs.length === 0) {
        return 'N/A';
    }

    return mccs.map(mcc => {
        const label = MCC_LABELS[mcc] || `MCC ${mcc}`;
        return `${label} (${mcc})`;
    }).join(', ');
}

// Toggle requirements visibility
function toggleRequirements(event) {
    const toggle = event.currentTarget;
    const content = toggle.nextElementSibling;

    toggle.classList.toggle('expanded');
    content.classList.toggle('expanded');
}

// Update summary statistics
function updateSummaryStats() {
    const total = filteredItems.length;
    const high = filteredItems.filter(i => i.impact_level === 'high').length;
    const medium = filteredItems.filter(i => i.impact_level === 'medium').length;
    const low = filteredItems.filter(i => i.impact_level === 'low').length;

    document.getElementById('totalCount').textContent = total;
    document.getElementById('highCount').textContent = high;
    document.getElementById('mediumCount').textContent = medium;
    document.getElementById('lowCount').textContent = low;
}

// Show error state
function showError(message) {
    document.getElementById('loading').style.display = 'none';
    const errorDiv = document.getElementById('error');
    errorDiv.style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

// Parse JSON fields (handle both string and already-parsed objects)
function parseJSON(value) {
    if (!value) return null;
    if (Array.isArray(value)) return value;
    if (typeof value === 'string') {
        try {
            return JSON.parse(value);
        } catch (e) {
            return null;
        }
    }
    return null;
}

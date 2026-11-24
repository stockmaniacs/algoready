/**
 * AlgoReady Overlay Utilities
 * Provides overlay, toast, and modal functionality
 */

/**
 * Create and show an overlay/modal
 * @param {string} title - Overlay title
 * @param {string} content - HTML content
 * @param {object} options - Configuration options
 * @returns {Promise<string|boolean>} - Resolves with button result or true
 */
function showOverlay(title, content, options = {}) {
    return new Promise((resolve) => {
        // Remove existing overlay
        hideOverlay();
        
        const overlayContainer = document.createElement('div');
        overlayContainer.className = 'overlay-container';
        overlayContainer.id = 'algoready-overlay';
        
        const overlayPanel = document.createElement('div');
        overlayPanel.className = 'overlay-panel';
        
        const header = document.createElement('header');
        header.className = 'overlay-header';
        header.innerHTML = `
            <h2>${title}</h2>
            <button class="overlay-close" id="overlay-close">&times;</button>
        `;
        
        const body = document.createElement('div');
        body.className = 'overlay-body';
        body.innerHTML = content;
        
        const actions = document.createElement('div');
        actions.className = 'overlay-actions';
        
        // Add buttons
        if (options.showCancel !== false) {
            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'btn-secondary';
            cancelBtn.textContent = 'Cancel';
            cancelBtn.addEventListener('click', () => {
                cleanup();
                resolve(false);
            });
            actions.appendChild(cancelBtn);
        }
        
        if (options.showConfirm !== false) {
            const confirmBtn = document.createElement('button');
            confirmBtn.className = 'btn-primary';
            confirmBtn.textContent = options.confirmText || 'Confirm';
            if (options.confirmCallback) {
                confirmBtn.addEventListener('click', () => {
                    cleanup();
                    resolve(options.confirmCallback());
                });
            } else {
                confirmBtn.addEventListener('click', () => {
                    cleanup();
                    resolve(true);
                });
            }
            actions.appendChild(confirmBtn);
        }
        
        overlayPanel.appendChild(header);
        overlayPanel.appendChild(body);
        overlayPanel.appendChild(actions);
        overlayContainer.appendChild(overlayPanel);
        document.body.appendChild(overlayContainer);
        
        // Close button handler
        document.getElementById('overlay-close').addEventListener('click', () => {
            cleanup();
            resolve(false);
        });
        
        // Escape key handler
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                cleanup();
                resolve(false);
            }
        };
        document.addEventListener('keydown', handleEscape);
        
        function cleanup() {
            if (overlayContainer) {
                overlayContainer.remove();
            }
            document.removeEventListener('keydown', handleEscape);
        }
    });
}

/**
 * Hide and remove the current overlay
 */
function hideOverlay() {
    const existing = document.getElementById('algoready-overlay');
    if (existing) {
        existing.remove();
    }
}

/**
 * Show a toast notification
 * @param {string} message - Toast message
 * @param {string} type - 'success', 'error', 'info', 'warning'
 * @param {number} duration - Duration in milliseconds
 */
function showToast(message, type = 'info', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Auto-remove
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s';
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
    
    // Manual close on click
    toast.addEventListener('click', () => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s';
        setTimeout(() => toast.remove(), 300);
    });
}

/**
 * Show a confirm alert
 * @param {string} message - Alert message
 * @param {string} title - Alert title
 * @param {string} type - 'success', 'error', 'info'
 * @returns {Promise<boolean>}
 */
function showConfirm(message, title = 'Confirm', type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert-overlay ${type}`;
    alertContainer.id = 'algoready-alert';
    
    alertContainer.innerHTML = `
        <h3>${title}</h3>
        <p>${message}</p>
        <button onclick="closeConfirm()">OK</button>
    `;
    
    document.body.appendChild(alertContainer);
    
    return new Promise((resolve) => {
        window.closeConfirm = () => {
            alertContainer.style.opacity = '0';
            alertContainer.style.transition = 'opacity 0.3s';
            setTimeout(() => alertContainer.remove(), 300);
            resolve(true);
        };
    });
}

/**
 * Show an alert and wait for acknowledgment
 * @param {string} message - Alert message
 * @param {string} title - Alert title
 * @param {string} type - 'success', 'error', 'info'
 */
function showAlert(message, title = 'Alert', type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert-overlay ${type}`;
    alertContainer.id = 'algoready-alert';
    
    alertContainer.innerHTML = `
        <h3>${title}</h3>
        <p>${message}</p>
        <button onclick="closeAlert()">OK</button>
    `;
    
    document.body.appendChild(alertContainer);
    
    window.closeAlert = () => {
        alertContainer.style.opacity = '0';
        alertContainer.style.transition = 'opacity 0.3s';
        setTimeout(() => alertContainer.remove(), 300);
    };
}

/**
 * Show loading spinner
 * @param {string} message - Loading message
 * @returns {string} - Container element
 */
function showLoading(message = 'Loading...') {
    const container = document.createElement('div');
    container.className = 'overlay-container';
    container.id = 'algoready-loading';
    container.style.zIndex = '9998';
    
    container.innerHTML = `
        <div class="overlay-panel" style="max-width: 300px; text-align: center;">
            <div class="spinner"></div>
            <p style="margin-top: 16px; color: var(--text-secondary);">${message}</p>
        </div>
    `;
    
    document.body.appendChild(container);
    return container;
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const existing = document.getElementById('algoready-loading');
    if (existing) {
        existing.remove();
    }
}

/**
 * Format currency
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code
 * @returns {string}
 */
function formatCurrency(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

/**
 * Format percentage
 * @param {number} value - Value to format
 * @param {number} decimals - Decimal places
 * @returns {string}
 */
function formatPercent(value, decimals = 2) {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(decimals)}%`;
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function}
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Deep copy object
 * @param {any} obj - Object to copy
 * @returns {any}
 */
function deepCopy(obj) {
    return JSON.parse(JSON.stringify(obj));
}

/**
 * Generate unique ID
 * @returns {string}
 */
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showOverlay,
        hideOverlay,
        showToast,
        showConfirm,
        showAlert,
        showLoading,
        hideLoading,
        formatCurrency,
        formatPercent,
        debounce,
        deepCopy,
        generateId
    };
}
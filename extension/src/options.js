/**
 * AlgoReady Chrome Extension Options Page
 * Settings and configuration
 */

// Default settings
const DEFAULT_SETTINGS = {
    theme: 'dark',
    notifications: true,
    alerts: true,
    autoSync: true,
    syncInterval: 30,
    defaultExchange: 'NSE',
    dataProvider: 'kite',
    hotkeys: true,
    compactMode: false,
    showPaperTrading: true
};

/**
 * Render settings form
 */
function renderSettings(settings) {
    const content = document.getElementById('options-content');
    
    content.innerHTML = `
        <div class="options-page">
            <section class="settings-section">
                <h2>Appearance</h2>
                <div class="option-group">
                    <label>Theme</label>
                    <select id="theme-select">
                        <option value="dark" ${settings.theme === 'dark' ? 'selected' : ''}>Dark</option>
                        <option value="light" ${settings.theme === 'light' ? 'selected' : ''}>Light</option>
                    </select>
                </div>
                
                <div class="option-group">
                    <label>
                        <input type="checkbox" id="compact-mode" ${settings.compactMode ? 'checked' : ''}>
                        Compact Mode
                    </label>
                </div>
            </section>
            
            <section class="settings-section">
                <h2>Notifications</h2>
                <div class="option-group">
                    <label>
                        <input type="checkbox" id="notifications" ${settings.notifications ? 'checked' : ''}>
                        Enable Notifications
                    </label>
                </div>
                
                <div class="option-group">
                    <label>
                        <input type="checkbox" id="alerts" ${settings.alerts ? 'checked' : ''}>
                        Trading Alerts
                    </label>
                </div>
            </section>
            
            <section class="settings-section">
                <h2>Data & Sync</h2>
                <div class="option-group">
                    <label>
                        <input type="checkbox" id="auto-sync" ${settings.autoSync ? 'checked' : ''}>
                        Auto Sync
                    </label>
                </div>
                
                <div class="option-group">
                    <label for="sync-interval">Sync Interval (minutes)</label>
                    <input type="number" id="sync-interval" min="1" max="60" value="${settings.syncInterval || 30}">
                </div>
                
                <div class="option-group">
                    <label for="default-exchange">Default Exchange</label>
                    <select id="default-exchange">
                        <option value="NSE" ${settings.defaultExchange === 'NSE' ? 'selected' : ''}>NSE</option>
                        <option value="BSE" ${settings.defaultExchange === 'BSE' ? 'selected' : ''}>BSE</option>
                        <option value="NFO" ${settings.defaultExchange === 'NFO' ? 'selected' : ''}>NFO</option>
                    </select>
                </div>
            </section>
            
            <section class="settings-section">
                <h2>Advanced</h2>
                <div class="option-group">
                    <label for="data-provider">Data Provider</label>
                    <select id="data-provider">
                        <option value="kite" ${settings.dataProvider === 'kite' ? 'selected' : ''}>Kite (Zerodha)</option>
                        <option value="upstox" ${settings.dataProvider === 'upstox' ? 'selected' : ''}>Upstox</option>
                        <option value="fyers" ${settings.dataProvider === 'fyers' ? 'selected' : ''}>FYERS</option>
                    </select>
                </div>
                
                <div class="option-group">
                    <label>
                        <input type="checkbox" id="hotkeys" ${settings.hotkeys ? 'checked' : ''}>
                        Enable Keyboard Shortcuts
                    </label>
                </div>
                
                <div class="option-group">
                    <label>
                        <input type="checkbox" id="show-paper-trading" ${settings.showPaperTrading ? 'checked' : ''}>
                        Show Paper Trading Mode
                    </label>
                </div>
            </section>
            
            <section class="settings-section">
                <h2>Broker Connections</h2>
                <div id="broker-connections">
                    <p class="content-placeholder">Connect your broker accounts from the popup panel.</p>
                </div>
            </section>
        </div>
    `;
    
    // Attach event listeners
    attachEventListeners(settings);
}

/**
 * Attach event listeners to settings form
 */
function attachEventListeners(settings) {
    document.getElementById('save-settings').addEventListener('click', saveSettings);
    
    // Add change listeners to all form elements
    const themeSelect = document.getElementById('theme-select');
    const compactMode = document.getElementById('compact-mode');
    const notifications = document.getElementById('notifications');
    const alerts = document.getElementById('alerts');
    const autoSync = document.getElementById('auto-sync');
    const syncInterval = document.getElementById('sync-interval');
    const defaultExchange = document.getElementById('default-exchange');
    const dataProvider = document.getElementById('data-provider');
    const hotkeys = document.getElementById('hotkeys');
    const showPaperTrading = document.getElementById('show-paper-trading');
    
    if (themeSelect) themeSelect.addEventListener('change', previewChanges);
    if (compactMode) compactMode.addEventListener('change', previewChanges);
    if (notifications) notifications.addEventListener('change', previewChanges);
    if (alerts) alerts.addEventListener('change', previewChanges);
    if (autoSync) autoSync.addEventListener('change', previewChanges);
    if (syncInterval) syncInterval.addEventListener('change', previewChanges);
    if (defaultExchange) defaultExchange.addEventListener('change', previewChanges);
    if (dataProvider) dataProvider.addEventListener('change', previewChanges);
    if (hotkeys) hotkeys.addEventListener('change', previewChanges);
    if (showPaperTrading) showPaperTrading.addEventListener('change', previewChanges);
}

/**
 * Preview changes (apply without saving)
 */
function previewChanges() {
    const settings = loadSettings();
    
    const themeSelect = document.getElementById('theme-select');
    const compactMode = document.getElementById('compact-mode');
    const notifications = document.getElementById('notifications');
    const alerts = document.getElementById('alerts');
    const autoSync = document.getElementById('auto-sync');
    const syncInterval = document.getElementById('sync-interval');
    const defaultExchange = document.getElementById('default-exchange');
    const dataProvider = document.getElementById('data-provider');
    const hotkeys = document.getElementById('hotkeys');
    const showPaperTrading = document.getElementById('show-paper-trading');
    
    if (themeSelect) settings.theme = themeSelect.value;
    if (compactMode) settings.compactMode = compactMode.checked;
    if (notifications) settings.notifications = notifications.checked;
    if (alerts) settings.alerts = alerts.checked;
    if (autoSync) settings.autoSync = autoSync.checked;
    if (syncInterval) settings.syncInterval = parseInt(syncInterval.value) || 30;
    if (defaultExchange) settings.defaultExchange = defaultExchange.value;
    if (dataProvider) settings.dataProvider = dataProvider.value;
    if (hotkeys) settings.hotkeys = hotkeys.checked;
    if (showPaperTrading) settings.showPaperTrading = showPaperTrading.checked;
    
    applySettings(settings);
}

/**
 * Save settings to storage
 */
async function saveSettings() {
    const settings = loadSettings();
    
    try {
        await chrome.storage.sync.set({ algoreadySettings: settings });
        
        const saveBtn = document.getElementById('save-settings');
        saveBtn.textContent = 'Saved!';
        saveBtn.classList.add('saved');
        
        setTimeout(() => {
            saveBtn.textContent = 'Save Settings';
            saveBtn.classList.remove('saved');
        }, 2000);
        
    } catch (error) {
        console.error('Error saving settings:', error);
        alert('Failed to save settings. Please try again.');
    }
}

/**
 * Load settings from storage
 */
function loadSettings() {
    const settings = { ...DEFAULT_SETTINGS };
    
    // Load broker connections count
    const brokers = JSON.parse(localStorage.getItem('brokerConnections') || '[]');
    settings.connectedBrokers = brokers.length;
    
    return settings;
}

/**
 * Apply settings to UI
 */
function applySettings(settings) {
    const root = document.documentElement;
    
    if (settings.theme === 'dark') {
        root.style.setProperty('--bg-primary', '#0f172a');
        root.style.setProperty('--text-primary', '#f8fafc');
    } else {
        root.style.setProperty('--bg-primary', '#ffffff');
        root.style.setProperty('--text-primary', '#0f172a');
    }
}

/**
 * Initialize options page
 */
async function init() {
    try {
        const result = await chrome.storage.sync.get(['algoreadySettings']);
        const settings = result.algoreadySettings || DEFAULT_SETTINGS;
        
        renderSettings(settings);
        applySettings(settings);
        
    } catch (error) {
        console.error('Error initializing options:', error);
        renderSettings(DEFAULT_SETTINGS);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
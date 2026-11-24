/**
 * AlgoReady Chrome Extension Side Panel
 * Advanced trading interface
 */

const API_URL = 'https://api.algoready.dev';

// Current tab state
let currentTab = 'dashboard';

/**
 * Render dashboard tab
 */
function renderDashboard(positions, signals) {
    const content = document.getElementById('sidepanel-content');
    
    const totalPnl = positions.reduce((sum, p) => sum + (p.unrealized_pnl || 0), 0);
    const activeSignals = signals?.filter(s => s.status === 'pending') || [];
    
    content.innerHTML = `
        <div class="dashboard-grid">
            <div class="dashboard-card">
                <h3>Total P&L</h3>
                <div class="metric ${totalPnl >= 0 ? 'profit' : 'loss'}">
                    ${totalPnl >= 0 ? '+' : ''}${totalPnl.toFixed(2)}
                </div>
            </div>
            
            <div class="dashboard-card">
                <h3>Active Signals</h3>
                <div class="metric">${activeSignals.length}</div>
            </div>
            
            <div class="dashboard-card">
                <h3>Open Positions</h3>
                <div class="metric">${positions.length}</div>
            </div>
        </div>
        
        ${positions.length > 0 ? `
            <div class="positions-list">
                <h3>Positions</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Instrument</th>
                            <th>Qty</th>
                            <th>Entry</th>
                            <th>Current</th>
                            <th>P&L</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${positions.map(p => `
                            <tr class="${p.unrealized_pnl >= 0 ? 'profit' : 'loss'}">
                                <td>${p.instrument}</td>
                                <td>${p.quantity}</td>
                                <td>${p.avg_entry_price.toFixed(2)}</td>
                                <td>${p.current_price?.toFixed(2) || '-'}</td>
                                <td>${(p.unrealized_pnl || 0).toFixed(2)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        ` : ''}
        
        ${activeSignals.length > 0 ? `
            <div class="signals-list">
                <h3>Active Signals</h3>
                ${activeSignals.map(s => `
                    <div class="signal-card">
                        <div class="signal-header">
                            <span class="instrument">${s.instrument}</span>
                            <span class="direction ${s.direction.toLowerCase()}">${s.direction}</span>
                        </div>
                        <div class="signal-details">
                            <span>Entry: ${s.entry_price || s.detected_at.toLocaleTimeString()}</span>
                            <span>Target: ${s.target_price}</span>
                            <span>SL: ${s.stop_loss_price}</span>
                        </div>
                        <button class="btn-primary" onclick="executeSignal('${s.id}')">Execute</button>
                    </div>
                `).join('')}
            </div>
        ` : ''}
    `;
}

/**
 * Render positions tab
 */
function renderPositions(positions) {
    const content = document.getElementById('sidepanel-content');
    
    content.innerHTML = `
        <div class="positions-page">
            <h2>Positions</h2>
            ${positions.length > 0 ? `
                <table class="positions-table">
                    <thead>
                        <tr>
                            <th>Instrument</th>
                            <th>Exchange</th>
                            <th>Direction</th>
                            <th>Quantity</th>
                            <th>Entry</th>
                            <th>Current</th>
                            <th>P&L</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${positions.map(p => `
                            <tr>
                                <td>${p.instrument}</td>
                                <td>${p.exchange}</td>
                                <td class="${p.direction.toLowerCase()}">${p.direction}</td>
                                <td>${p.quantity}</td>
                                <td>${p.avg_entry_price.toFixed(2)}</td>
                                <td>${(p.current_price || 0).toFixed(2)}</td>
                                <td class="${p.unrealized_pnl >= 0 ? 'profit' : 'loss'}">
                                    ${(p.unrealized_pnl || 0).toFixed(2)}
                                </td>
                                <td>
                                    <button class="btn-secondary" onclick="closePosition('${p.id}')">Close</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            ` : '<p>No open positions</p>'}
        </div>
    `;
}

/**
 * Render orders tab
 */
function renderOrders(orders) {
    const content = document.getElementById('sidepanel-content');
    
    content.innerHTML = `
        <div class="orders-page">
            <h2>Orders</h2>
            ${orders.length > 0 ? `
                <table class="orders-table">
                    <thead>
                        <tr>
                            <th>Instrument</th>
                            <th>Type</th>
                            <th>Status</th>
                            <th>Qty</th>
                            <th>Price</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${orders.map(o => `
                            <tr>
                                <td>${o.instrument}</td>
                                <td>${o.order_type || 'Market'}</td>
                                <td class="status-${o.status?.toLowerCase()}">${o.status}</td>
                                <td>${o.quantity}</td>
                                <td>${o.price || '-'}</td>
                                <td>${o.placed_at.toLocaleTimeString()}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            ` : '<p>No orders</p>'}
        </div>
    `;
}

/**
 * Render strategies tab
 */
function renderStrategies(strategies) {
    const content = document.getElementById('sidepanel-content');
    
    content.innerHTML = `
        <div class="strategies-page">
            <h2>Strategies</h2>
            <div class="strategies-grid">
                ${strategies.map(s => `
                    <div class="strategy-card">
                        <h3>${s.name}</h3>
                        <p class="category">${s.category}</p>
                        <div class="strategy-meta">
                            <span class="target">TP: ${s.target_percent}%</span>
                            <span class="sl">SL: ${s.stop_loss_percent}%</span>
                        </div>
                        <button class="btn-secondary" onclick="applyStrategy('${s.id}')">Apply</button>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

/**
 * Switch tabs
 */
function switchTab(tabName) {
    currentTab = tabName;
    
    // Update nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.dataset.tab === tabName);
    });
    
    // Load content based on tab
    loadTabContent(tabName);
}

/**
 * Load content for specific tab
 */
async function loadTabContent(tabName) {
    const token = await getAuthToken();
    
    if (!token) {
        alert('Please sign in first');
        return;
    }
    
    try {
        switch (tabName) {
            case 'dashboard':
                const [positionsRes, signalsRes] = await Promise.all([
                    fetch(`${API_URL}/v1/positions`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    })
                ]);
                const positions = await positionsRes.json();
                const signals = await signalsRes.json();
                renderDashboard(positions, signals);
                break;
                
            case 'positions':
                const posRes = await fetch(`${API_URL}/v1/positions`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const posData = await posRes.json();
                renderPositions(posData);
                break;
                
            case 'orders':
                const ordersRes = await fetch(`${API_URL}/v1/orders`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const orders = await ordersRes.json();
                renderOrders(orders);
                break;
                
            case 'strategies':
                const stratRes = await fetch(`${API_URL}/v1/strategies`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const strategies = await stratRes.json();
                renderStrategies(strategies);
                break;
        }
    } catch (error) {
        console.error('Error loading tab:', error);
    }
}

/**
 * Get auth token
 */
async function getAuthToken() {
    return new Promise((resolve) => {
        chrome.storage.sync.get(['authState'], (result) => {
            resolve(result.authState?.token);
        });
    });
}

/**
 * Initialize side panel
 */
async function init() {
    // Set up tab switching
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            switchTab(e.target.dataset.tab);
        });
    });
    
    // Load initial content
    await loadTabContent(currentTab);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Expose functions for HTML
window.executeSignal = async (signalId) => {};
window.closePosition = async (positionId) => {};
window.applyStrategy = async (strategyId) => {};
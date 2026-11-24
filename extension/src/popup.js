/**
 * AlgoReady Chrome Extension Popup
 */

const API_URL = 'https://api.algoready.dev';

/**
 * Render authenticated view
 */
function renderAuthenticatedView(brokers, strategies) {
    const content = document.getElementById('content');
    
    const brokerCount = brokers?.length || 0;
    const activeStrategies = strategies?.activeCount || 0;
    const strategyName = strategies?.active?.[0]?.name || 'None';
    
    content.innerHTML = `
        <div class="status-card">
            <h3>Connected Accounts</h3>
            <div class="broker-count">${brokerCount} connected</div>
        </div>
        
        <div class="status-card">
            <h3>Active Strategies</h3>
            <div class="strategy-info">
                <span class="strategy-count">${activeStrategies}</span>
                <span class="strategy-name">${strategyName}</span>
            </div>
        </div>
        
        <div class="actions">
            <button id="connect-btn" class="btn-primary">
                Connect New Broker
            </button>
            <button id="open-app-btn" class="btn-secondary">
                Open AlgoReady
            </button>
        </div>
    `;
    
    // Add event listeners
    document.getElementById('connect-btn').addEventListener('click', () => {
        chrome.runtime.sendMessage({ type: 'OPEN_BROKER_CONNECTOR' });
        window.close();
    });
    
    document.getElementById('open-app-btn').addEventListener('click', () => {
        chrome.tabs.create({ url: 'https://algoready.pages.dev' });
        window.close();
    });
}

/**
 * Render login view
 */
function renderLoginView() {
    const content = document.getElementById('content');
    
    content.innerHTML = `
        <div class="login-form">
            <h2>Welcome to AlgoReady</h2>
            <p>Your trading workspace</p>
            
            <form id="login-form">
                <div class="input-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" required placeholder="Enter your email">
                </div>
                
                <div class="input-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" required placeholder="Enter your password">
                </div>
                
                <button type="submit" class="btn-primary">Sign In</button>
            </form>
            
            <div class="auth-links">
                <a href="#" id="signup-link">Don't have an account? Sign up</a>
            </div>
        </div>
    `;
    
    // Add event listener
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await chrome.runtime.sendMessage({
                type: 'LOGIN',
                credentials: { email, password }
            });
            
            if (response.success) {
                await fetchBrokersAndStrategies();
            } else {
                alert(response.error || 'Login failed');
            }
        } catch (error) {
            alert('Login failed: ' + error.message);
        }
    });
}

/**
 * Fetch brokers and strategies
 */
async function fetchBrokersAndStrategies() {
    try {
        const brokersResult = await chrome.runtime.sendMessage({ type: 'BROKERS_LIST' });
        const strategiesResult = await chrome.runtime.sendMessage({ type: 'STRATEGIES_LIST' });
        
        renderAuthenticatedView(brokersResult.brokers || [], strategiesResult.strategies || []);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

/**
 * Initialize popup
 */
async function init() {
    try {
        const authResult = await chrome.runtime.sendMessage({ type: 'AUTH_CHECK' });
        
        if (authResult.authenticated) {
            await fetchBrokersAndStrategies();
        } else {
            renderLoginView();
        }
    } catch (error) {
        console.error('Initialization error:', error);
        renderLoginView();
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
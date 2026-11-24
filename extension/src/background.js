/**
 * AlgoReady Chrome Extension Background Service Worker
 * Handles authentication, broker connections, and message passing
 */

// Extension state
const state = {
  isAuthenticated: false,
  user: null,
  connectedBrokers: [],
  activeStrategies: [],
};

// API base URL
const API_URL = 'https://api.algoready.dev';

/**
 * Initialize extension on startup
 */
chrome.runtime.onInstalled.addListener(() => {
  console.log('AlgoReady extension installed');
  
  // Restore state from storage
  chrome.storage.sync.get(['authState', 'brokers', 'strategies'], (result) => {
    if (result.authState) {
      state.isAuthenticated = result.authState.isAuthenticated;
      state.user = result.authState.user;
    }
    if (result.brokers) {
      state.connectedBrokers = result.brokers;
    }
    if (result.strategies) {
      state.activeStrategies = result.strategies;
    }
  });
});

/**
 * Handle messages from content scripts and popup
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.type) {
    case 'AUTH_CHECK':
      sendResponse({ authenticated: state.isAuthenticated, user: state.user });
      break;
    
    case 'BROKERS_LIST':
      sendResponse({ brokers: state.connectedBrokers });
      break;
    
    case 'STRATEGIES_LIST':
      sendResponse({ strategies: state.activeStrategies });
      break;
    
    case 'LOGIN':
      handleLogin(message.credentials)
        .then(result => sendResponse({ success: true, data: result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true; // Keep message channel open
    
    case 'LOGOUT':
      handleLogout()
        .then(() => sendResponse({ success: true }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
    
    case 'CONNECT_BROKER':
      connectBroker(message.brokerType)
        .then(result => sendResponse({ success: true, data: result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
    
    default:
      console.warn('Unknown message type:', message.type);
      sendResponse({ error: 'Unknown message type' });
  }
  
  return true;
});

/**
 * Handle login flow
 */
async function handleLogin(credentials) {
  try {
    const response = await fetch(`${API_URL}/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    
    const data = await response.json();
    
    // Store authentication state
    state.isAuthenticated = true;
    state.user = data.user;
    
    // Save to storage
    await chrome.storage.sync.set({
      authState: {
        isAuthenticated: true,
        user: data.user,
        token: data.access_token,
      },
    });
    
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

/**
 * Handle logout
 */
async function handleLogout() {
  state.isAuthenticated = false;
  state.user = null;
  
  await chrome.storage.sync.remove(['authState', 'brokers', 'strategies']);
}

/**
 * Connect to a broker
 */
async function connectBroker(brokerType) {
  if (!state.isAuthenticated || !state.user) {
    throw new Error('User not authenticated');
  }
  
  const authState = await chrome.storage.sync.get(['authState']);
  const token = authState.authState?.token;
  
  if (!token) {
    throw new Error('No authentication token');
  }
  
  try {
    // Generate OAuth state
    const state = crypto.getRandomValues(new Uint8Array(32)).join('');
    
    // Store state for verification
    const connectionInfo = {
      brokerType,
      oauthState: state,
      initiatedAt: Date.now(),
    };
    
    // Open OAuth window
    const redirectUri = chrome.identity.getRedirectURL();
    const authUrl = await getBrokerAuthUrl(brokerType, redirectUri, state);
    
    const redirectUrl = await chrome.identity.launchWebAuthFlow({
      url: authUrl,
      interactive: true,
    });
    
    // Handle callback
    const params = new URLSearchParams(new URL(redirectUrl).search);
    const code = params.get('code');
    const returnedState = params.get('state');
    
    if (returnedState !== state) {
      throw new Error('Invalid OAuth state');
    }
    
    // Exchange code for token
    const response = await fetch(`${API_URL}/v1/brokers/${brokerType}/callback`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      throw new Error('Failed to connect broker');
    }
    
    const data = await response.json();
    
    // Update state
    state.connectedBrokers.push(data);
    await chrome.storage.sync.set({ brokers: state.connectedBrokers });
    
    return data;
  } catch (error) {
    console.error('Broker connection error:', error);
    throw error;
  }
}

/**
 * Get broker authorization URL
 */
async function getBrokerAuthUrl(brokerType, redirectUri, state) {
  const config = await fetchBrokerConfig(brokerType);
  return `${config.authUrl}?client_id=${config.clientId}&redirect_uri=${redirectUri}&response_type=code&state=${state}&scope=${config.scopes.join(' ')}`;
}

/**
 * Fetch broker configuration
 */
async function fetchBrokerConfig(brokerType) {
  // This would typically come from your backend
  const configs = {
    zerodha: {
      authUrl: 'https://kite.trade/connect/login',
      clientId: process.env.ZERODHA_API_KEY,
      scopes: ['login', 'portfolio', 'orders', 'positions', 'quote', 'historical_data', 'websocket'],
    },
    upstox: {
      authUrl: 'https://api.upstox.org/v2/login/authorization',
      clientId: process.env.UPSTOX_API_KEY,
      scopes: ['read', 'trade', 'positions'],
    },
    fyers: {
      authUrl: 'https://api.fyers.in/api/v2/authorize',
      clientId: process.env.FYERS_CLIENT_ID,
      scopes: ['profile', 'trading', 'market_data'],
    },
  };
  
  return configs[brokerType] || null;
}

/**
 * Sync positions from broker
 */
async function syncPositions() {
  if (!state.isAuthenticated) return;
  
  const authState = await chrome.storage.sync.get(['authState']);
  const token = authState.authState?.token;
  
  if (!token) return;
  
  try {
    const response = await fetch(`${API_URL}/v1/positions`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    
    if (response.ok) {
      const positions = await response.json();
      return positions;
    }
  } catch (error) {
    console.error('Failed to sync positions:', error);
  }
  
  return [];
}

/**
 * Create notification for signal
 */
async function createSignalNotification(signal) {
  const options = {
    type: 'basic',
    iconUrl: 'public/icons/icon-16.png',
    title: `AlgoReady Signal: ${signal.instrument}`,
    message: `${signal.direction} @ ${signal.entry_price}\nTarget: ${signal.target_price}\nSL: ${signal.stop_loss_price}`,
    priority: 2,
  };
  
  await chrome.notifications.create(`signal_${signal.id}`, options);
}

/**
 * Schedule position sync
 */
chrome.alarms.create('syncPositions', { periodInMinutes: 1 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'syncPositions') {
    syncPositions();
  }
});
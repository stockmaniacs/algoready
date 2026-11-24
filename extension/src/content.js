/**
 * AlgoReady Chrome Extension Content Script
 * Injects chart overlays and detects trading platforms
 */

(() => {
    'use strict';

    // Content script state
    let state = {
        platform: null,
        instrument: null,
        exchange: null,
        timeframe: null,
        charts: [],
        overlayElements: [],
    };

    // Platform detection patterns
    const platforms = {
        zerodha: {
            urlPattern: /kite\.trade/,
            chartSelectors: ['.chart-container', '#chart', '[data-role="chart"]'],
            instrumentSelector: '.instrument-name, [data-symbol]',
            timeframeSelectors: '.timeframe-selector, [data-timeframe]',
        },
        upstox: {
            urlPattern: /upstox\.com/,
            chartSelectors: ['.tradingview-chart', '#chart'],
            instrumentSelector: '.instrument-symbol, [data-symbol]',
            timeframeSelectors: '.timeframe-wrapper, [data-timeframe]',
        },
        fyers: {
            urlPattern: /fyers\.in/,
            chartSelectors: ['.chart-container', '#chart-container'],
            instrumentSelector: '.symbol-name, [data-symbol]',
            timeframeSelectors: '.timeframe-selector, [data-interval]',
        },
    };

    /**
     * Detect current platform
     */
    function detectPlatform() {
        const url = window.location.href;
        
        for (const [name, config] of Object.entries(platforms)) {
            if (config.urlPattern.test(url)) {
                return name;
            }
        }
        
        return null;
    }

    /**
     * Detect instrument on chart
     */
    function detectInstrument() {
        if (!state.platform) return null;
        
        const config = platforms[state.platform];
        if (!config) return null;
        
        try {
            // Try to find instrument element
            const element = document.querySelector(config.instrumentSelector);
            if (element) {
                return element.textContent.trim() || element.dataset.symbol;
            }
            
            // Fallback: parse from URL
            const pathMatch = window.location.pathname.match(/\/([^/]+)\/?$/);
            if (pathMatch) {
                return pathMatch[1].toUpperCase();
            }
            
        } catch (error) {
            console.error('Error detecting instrument:', error);
        }
        
        return null;
    }

    /**
     * Detect exchange
     */
    function detectExchange() {
        if (!state.platform) return null;
        
        // Infer from platform and instrument
        const instrument = state.instrument?.toUpperCase() || '';
        
        if (instrument.includes('NIFTY') || instrument.includes('BANKNIFTY')) {
            return 'NSE';
        }
        if (instrument.includes('-') && instrument.split('-')[1]) {
            const suffix = instrument.split('-')[1];
            if (suffix.includes('CE') || suffix.includes('PE')) {
                return 'NFO';
            }
        }
        
        return 'NSE';
    }

    /**
     * Detect timeframe
     */
    function detectTimeframe() {
        if (!state.platform) return null;
        
        const config = platforms[state.platform];
        if (!config) return null;
        
        try {
            const element = document.querySelector(config.timeframeSelectors?.[0]);
            if (element) {
                const timeframe = element.textContent.trim() || element.dataset.timeframe;
                return normalizeTimeframe(timeframe);
            }
        } catch (error) {
            console.error('Error detecting timeframe:', error);
        }
        
        return '15m'; // Default
    }

    /**
     * Normalize timeframe format
     */
    function normalizeTimeframe(tf) {
        const tfLower = tf?.toLowerCase() || '15m';
        
        // Common conversions
        const conversions = {
            '1': '1m', '5': '5m', '15': '15m', '30': '30m',
            '60': '60m', '1h': '60m', '90': '90m', '120': '120m',
            '1d': '1d', '1w': '1w', '1mo': '1mo'
        };
        
        return conversions[tfLower] || tfLower;
    }

    /**
     * Initialize chart overlay
     */
    function initOverlay() {
        if (!state.instrument) return;
        
        // Create overlay container
        const overlayContainer = document.createElement('div');
        overlayContainer.className = 'algoready-overlay';
        overlayContainer.id = 'algoready-overlay';
        
        // Add CSS
        addOverlayStyles();
        
        // Find chart container
        const chartContainer = document.querySelector('.tradingview-widget-container, .chart-container, #chart');
        if (chartContainer) {
            chartContainer.style.position = 'relative';
            chartContainer.appendChild(overlayContainer);
            
            state.overlayElements.push(overlayContainer);
        }
    }

    /**
     * Add overlay styles
     */
    function addOverlayStyles() {
        if (document.getElementById('algoready-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'algoready-styles';
        style.textContent = `
            .algoready-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 9999;
            }
            
            .algoready-signal {
                position: absolute;
                background: rgba(0, 165, 233, 0.9);
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-family: Arial, sans-serif;
                pointer-events: auto;
            }
            
            .algoready-entry-line {
                position: absolute;
                height: 100%;
                border-left: 2px dashed #0EA5E9;
                z-index: 9998;
            }
            
            .algoready-target-line {
                position: absolute;
                height: 100%;
                border-left: 2px solid #22C55E;
                z-index: 9998;
            }
            
            .algoready-sl-line {
                position: absolute;
                height: 100%;
                border-left: 2px solid #EF4444;
                z-index: 9998;
            }
            
            .algoready-marker {
                position: absolute;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                z-index: 9999;
                pointer-events: auto;
            }
            
            .algoready-marker.entry {
                background: #0EA5E9;
                border: 2px solid white;
            }
            
            .algoready-marker.target {
                background: #22C55E;
                border: 2px solid white;
            }
            
            .algoready-marker.sl {
                background: #EF4444;
                border: 2px solid white;
            }
        `;
        
        document.head.appendChild(style);
    }

    /**
     * Update overlay with signal data
     */
    function updateOverlay(signal) {
        if (!state.overlayElements.length) return;
        
        const overlay = state.overlayElements[0];
        if (!overlay) return;
        
        // Remove existing overlays
        overlay.innerHTML = '';
        
        // Add signal label
        const label = document.createElement('div');
        label.className = 'algoready-signal';
        label.innerHTML = `
            <div><strong>${signal.instrument}</strong></div>
            <div>Direction: ${signal.direction}</div>
            <div>Entry: ${signal.entry_price}</div>
            <div>Target: ${signal.target_price}</div>
            <div>SL: ${signal.stop_loss_price}</div>
        `;
        overlay.appendChild(label);
    }

    /**
     * Handle platform changes
     */
    function handlePlatformChange() {
        const platform = detectPlatform();
        
        if (platform && platform !== state.platform) {
            state.platform = platform;
            console.log(`Detected platform: ${platform}`);
            
            // Request instruments from background
            chrome.runtime.sendMessage({
                type: 'PLATFORM_DETECTED',
                platform: platform
            });
            
            // Initialize overlay
            initOverlay();
        }
    }

    /**
     * Main initialization
     */
    function init() {
        // Initial detection
        handlePlatformChange();
        
        // Set up mutation observer for dynamic content
        const observer = new MutationObserver((mutations) => {
            // Check for instrument/timeframe changes
            const newInstrument = detectInstrument();
            const newTimeframe = detectTimeframe();
            
            if (newInstrument !== state.instrument) {
                state.instrument = newInstrument;
                console.log('Instrument changed:', newInstrument);
            }
            
            if (newTimeframe !== state.timeframe) {
                state.timeframe = newTimeframe;
                console.log('Timeframe changed:', newTimeframe);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Check for page changes
        window.addEventListener('popstate', handlePlatformChange);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose methods for other scripts
    window.AlgoReady = {
        getState: () => state,
        updateOverlay: updateOverlay,
        initOverlay: initOverlay,
    };

})();
/**
 * Frontend Configuration
 * 
 * This file contains environment-specific configuration for the MedAdhere frontend.
 * It automatically detects if running locally or in production and uses the appropriate API URL.
 */

const API_CONFIG = {
    // Automatically detect environment
    baseURL: window.location.hostname === 'localhost' 
        ? 'http://localhost:8010'  // Local development
        : 'https://medadhere-backend-azc7a8eyd8ggbadx.centralindia-01.azurewebsites.net',  // Production (Azure)
    
    timeout: 30000,  // 30 seconds timeout
    
    // Retry configuration
    retryAttempts: 3,
    retryDelay: 1000,  // 1 second
};

// Make config available globally
window.API_CONFIG = API_CONFIG;

// Log current configuration (for debugging)
console.log('🔧 API Configuration:', {
    environment: window.location.hostname === 'localhost' ? 'Development' : 'Production',
    baseURL: API_CONFIG.baseURL
});

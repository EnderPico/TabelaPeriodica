/**
 * Periodic Table Interactive Script - Overlay Duplicate Card System
 * 
 * This script handles:
 * - Element card click events
 * - Creating duplicate overlay cards in the center
 * - CSS 3D flip animations for overlay cards
 * - API calls to fetch element details
 * - Backdrop click to close overlay
 * 
 * Animation Flow:
 * 1. Click element → show backdrop + duplicate card (front face)
 * 2. Fetch data → flip card to show back face with details
 * 3. Click backdrop → flip back to front → hide overlay
 * 
 * Author: High School IT Project
 * Purpose: Educational periodic table with overlay duplicate cards
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL
const FLIP_DURATION = 600; // Duration of flip animation in milliseconds

// DOM elements
let overlayBackdrop = null;
let overlayCard = null;
let overlayCardFront = null;
let overlayCardBack = null;

// State management
let isOverlayOpen = false;
let currentElementData = null;

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🧪 Periodic Table Overlay Duplicate Card System Initialized');
    
    // Get DOM elements
    overlayBackdrop = document.getElementById('overlay-backdrop');
    overlayCard = document.getElementById('overlay-card');
    overlayCardFront = overlayCard.querySelector('.overlay-card-front');
    overlayCardBack = overlayCard.querySelector('.overlay-card-back');
    
    // Add event listeners
    setupElementClickListeners();
    setupBackdropClickListener();
    
    console.log('✅ Event listeners attached successfully');
});

/**
 * Add click event listeners to all element cards
 */
function setupElementClickListeners() {
    const elements = document.querySelectorAll('.element[data-symbol]');
    
    elements.forEach(element => {
        element.addEventListener('click', function(event) {
            event.stopPropagation();
            const symbol = this.getAttribute('data-symbol');
            
            if (symbol) {
                console.log(`🔬 Element clicked: ${symbol}`);
                handleElementClick(this, symbol);
            }
        });
    });
    
    console.log(`📋 Attached click listeners to ${elements.length} elements`);
}

/**
 * Handle element card click - create overlay duplicate and fetch data
 */
async function handleElementClick(elementCard, symbol) {
    if (isOverlayOpen) return;
    
    try {
        // Extract element data from the clicked card
        const atomicNumber = elementCard.querySelector('.atomic-number').textContent;
        const symbolText = elementCard.querySelector('.symbol').textContent;
        const name = elementCard.querySelector('.name').textContent;
        const atomicMass = elementCard.querySelector('.atomic-mass').textContent;
        
        // Get the element's category class for styling
        const categoryClasses = Array.from(elementCard.classList).filter(cls => 
            cls !== 'element' && cls !== 'flipped'
        );
        
        // Create duplicate card with front face data
        createOverlayCard(atomicNumber, symbolText, name, atomicMass, categoryClasses);
        
        // Show overlay backdrop
        showOverlayBackdrop();
        
        // Fetch detailed data from backend
        const elementData = await fetchElementData(symbol);
        
        if (elementData) {
            // Update card back with detailed information
            updateOverlayCardBack(elementData);
            
            // Flip to show back face after a short delay
            setTimeout(() => {
                flipOverlayCardToBack();
            }, 300);
            
            currentElementData = elementData;
        } else {
            // Handle error case
            showOverlayError('Erro ao carregar dados');
        }
        
    } catch (error) {
        console.error('❌ Error handling element click:', error);
        showOverlayError('Erro de conexão');
    }
}

/**
 * Fetch element data from the backend API
 */
async function fetchElementData(symbol) {
    try {
        console.log(`🌐 Fetching data for element: ${symbol}`);
        
        const response = await fetch(`${API_BASE_URL}/elements/${symbol}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(`✅ Data received for ${symbol}:`, data);
        
        return data;
        
    } catch (error) {
        console.error(`❌ Failed to fetch data for ${symbol}:`, error);
        return null;
    }
}

/**
 * Create overlay card with front face data
 */
function createOverlayCard(atomicNumber, symbol, name, atomicMass, categoryClasses) {
    // Update front face content
    overlayCardFront.querySelector('.overlay-atomic-number').textContent = atomicNumber;
    overlayCardFront.querySelector('.overlay-symbol').textContent = symbol;
    overlayCardFront.querySelector('.overlay-name').textContent = name;
    overlayCardFront.querySelector('.overlay-atomic-mass').textContent = atomicMass;
    
    // Apply the same category styling as the original element
    overlayCardFront.className = 'overlay-card-front';
    categoryClasses.forEach(cls => {
        overlayCardFront.classList.add(cls);
    });
    
    // Reset back face
    overlayCardBack.innerHTML = '<div class="overlay-loading">Carregando...</div>';
    overlayCardBack.className = 'overlay-card-back';
    
    console.log(`📋 Overlay card created for ${symbol}`);
}

/**
 * Show overlay backdrop
 */
function showOverlayBackdrop() {
    overlayBackdrop.classList.add('active');
    isOverlayOpen = true;
    console.log('🌫️ Overlay backdrop shown');
}

/**
 * Update overlay card back with detailed element data
 */
function updateOverlayCardBack(elementData) {
    overlayCardBack.innerHTML = `
        <div class="overlay-atomic-number">${elementData.number}</div>
        <div class="overlay-symbol">${elementData.symbol}</div>
        <div class="overlay-name">${elementData.name}</div>
        <div class="overlay-atomic-mass">${elementData.atomic_mass || 'N/A'}</div>
        <div class="overlay-description">${elementData.info || 'Informações detalhadas não disponíveis.'}</div>
    `;
    
    console.log(`📖 Overlay card back updated with details for ${elementData.symbol}`);
}

/**
 * Flip overlay card to show back face
 */
function flipOverlayCardToBack() {
    overlayBackdrop.classList.add('flipped');
    console.log('🔄 Overlay card flipped to back');
}

/**
 * Show error state in overlay card back
 */
function showOverlayError(errorMessage) {
    overlayCardBack.innerHTML = `<div class="overlay-loading" style="color: #e74c3c;">${errorMessage}</div>`;
    
    // Still flip to show error
    setTimeout(() => {
        flipOverlayCardToBack();
    }, 300);
}

/**
 * Setup backdrop click listener for closing overlay
 */
function setupBackdropClickListener() {
    if (overlayBackdrop) {
        overlayBackdrop.addEventListener('click', function(event) {
            if (event.target === overlayBackdrop && isOverlayOpen) {
                console.log('🔒 Backdrop clicked - closing overlay');
                closeOverlay();
            }
        });
    }
}

/**
 * Close overlay with reverse animation
 */
function closeOverlay() {
    if (!isOverlayOpen) return;
    
    // First flip back to front
    overlayBackdrop.classList.remove('flipped');
    
    // Wait for flip animation to complete, then hide backdrop
    setTimeout(() => {
        overlayBackdrop.classList.remove('active');
        isOverlayOpen = false;
        currentElementData = null;
        console.log('✅ Overlay closed');
    }, FLIP_DURATION);
}

/**
 * Handle keyboard events (ESC to close)
 */
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && isOverlayOpen) {
        closeOverlay();
    }
});

/**
 * Utility function to check if backend is available
 */
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/elements`);
        return response.ok;
    } catch (error) {
        console.warn('⚠️ Backend not available:', error.message);
        return false;
    }
}

// Check backend connection on load
document.addEventListener('DOMContentLoaded', async function() {
    const isBackendAvailable = await checkBackendConnection();
    
    if (!isBackendAvailable) {
        console.warn('⚠️ Backend API not available. Some features may not work.');
        
        // Show a subtle notification to the user
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f39c12;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 12px;
            z-index: 1001;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;
        notification.textContent = '⚠️ Backend não disponível - dados limitados';
        document.body.appendChild(notification);
        
        // Remove notification after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    } else {
        console.log('✅ Backend API connection successful');
    }
});

console.log('🚀 Periodic Table Overlay Duplicate Card Script loaded successfully');

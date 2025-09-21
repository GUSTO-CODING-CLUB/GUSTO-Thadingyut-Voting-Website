/**
 * Simple Professional Navigation Script for Kings Queens Voting Website
 * Clean, fast, and professional navigation effects
 */

// Navigation configuration mapping Flask routes to display names
const NAV_ROUTES = {
    '/': 'home',
    '/candidates': 'candidates', 
    '/lantern': 'lantern',
    '/results': 'results',
    '/about': 'about',
    '/final': 'final',
    '/winner': 'winner',
    '/viewmore': 'viewmore'
};

// Initialize navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
});

function initializeNavigation() {
    const navLinks = Array.from(document.querySelectorAll('.nav-a'));
    const indicator = document.getElementById('nav-indicator');
    
    if (!navLinks.length || !indicator) return;

    // Set initial active state based on current page
    setActivePage();
    
    // Handle navigation clicks
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavClick);
    });
    
    // Handle window resize
    window.addEventListener('resize', handleResize);
}

function getCurrentPage() {
    const path = window.location.pathname;
    
    // Handle root path
    if (path === '/' || path === '') {
        return 'home';
    }
    
    // Handle Flask routes
    for (const [route, page] of Object.entries(NAV_ROUTES)) {
        if (path === route) {
            return page;
        }
    }
    
    // Fallback to first nav item
    return 'home';
}

function setActivePage() {
    const currentPage = getCurrentPage();
    const navLinks = Array.from(document.querySelectorAll('.nav-a'));
    const indicator = document.getElementById('nav-indicator');
    
    // Remove active state from all links
    navLinks.forEach(link => {
        link.classList.remove('is-active', 'text-white');
        link.classList.add('text-gray-700');
    });
    
    // Find and activate current page link
    const activeLink = navLinks.find(link => {
        const href = link.getAttribute('href');
        if (!href) return false;
        
        // Check if this link corresponds to current page
        return (currentPage === 'home' && href.includes('/')) ||
               (currentPage !== 'home' && href.includes(`/${currentPage}`));
    });
    
    if (activeLink) {
        activeLink.classList.add('is-active', 'text-white');
        activeLink.classList.remove('text-gray-700');
        
        // Move indicator on desktop with simple animation
        if (window.innerWidth >= 768) {
            moveIndicatorTo(activeLink);
        }
    }
}

function moveIndicatorTo(element) {
    const indicator = document.getElementById('nav-indicator');
    const wrapper = element.closest('.relative');
    
    if (!indicator || !wrapper) return;
    
    const wrapperRect = wrapper.getBoundingClientRect();
    const elementRect = element.getBoundingClientRect();
    const paddingX = 8;
    const paddingY = 2;
    
    // Calculate position and size
    const width = elementRect.width + paddingX * 2;
    const height = elementRect.height + paddingY * 2;
    const x = elementRect.left - wrapperRect.left - paddingX;
    const y = elementRect.top - wrapperRect.top - paddingY;
    
    // Apply simple, fast transition
    indicator.style.width = `${width}px`;
    indicator.style.height = `${height}px`;
    indicator.style.transform = `translate(${x}px, ${y}px)`;
    indicator.style.opacity = '1';
}

function handleNavClick(event) {
    const link = event.currentTarget;
    const href = link.getAttribute('href');
    
    // Skip if no href or internal anchor
    if (!href || href.startsWith('#')) return;
    
    // Prevent default to handle navigation manually
    event.preventDefault();
    
    // Set active state immediately
    const navLinks = Array.from(document.querySelectorAll('.nav-a'));
    navLinks.forEach(l => {
        l.classList.remove('is-active', 'text-white');
        l.classList.add('text-gray-700');
    });
    
    link.classList.add('is-active', 'text-white');
    link.classList.remove('text-gray-700');
    
    // Move indicator on desktop
    if (window.innerWidth >= 768) {
        moveIndicatorTo(link);
    }
    
    // Navigate immediately for fast response
    window.location.href = href;
}

function handleResize() {
    const activeLink = document.querySelector('.nav-a.is-active');
    if (activeLink && window.innerWidth >= 768) {
        moveIndicatorTo(activeLink);
    }
}

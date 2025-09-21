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
        
        // Add smooth hover effects
        link.addEventListener('mouseenter', handleNavHover);
        link.addEventListener('mouseleave', handleNavLeave);
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
        link.classList.remove('is-active', 'text-black');
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
        activeLink.classList.add('is-active', 'text-black');
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
    const paddingX = 12;
    const paddingY = 4;
    
    // Calculate position and size
    const width = elementRect.width + paddingX * 2;
    const height = elementRect.height + paddingY * 2;
    const x = elementRect.left - wrapperRect.left - paddingX;
    const y = elementRect.top - wrapperRect.top - paddingY;
    
    // Apply smooth, professional transition with easing
    indicator.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
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
        l.classList.remove('is-active', 'text-black');
        l.classList.add('text-gray-700');
    });
    
    link.classList.add('is-active', 'text-black');
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

function handleNavHover(event) {
    const link = event.currentTarget;
    
    // Only show hover effect on desktop and if not already active
    if (window.innerWidth >= 768 && !link.classList.contains('is-active')) {
        const indicator = document.getElementById('nav-indicator');
        if (indicator) {
            // Create a subtle hover effect with reduced opacity
            indicator.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            moveIndicatorTo(link);
            indicator.style.opacity = '0.6';
        }
    }
}

function handleNavLeave(event) {
    const link = event.currentTarget;
    
    // Only handle leave on desktop and if not active
    if (window.innerWidth >= 768 && !link.classList.contains('is-active')) {
        const indicator = document.getElementById('nav-indicator');
        const activeLink = document.querySelector('.nav-a.is-active');
        
        if (indicator && activeLink) {
            // Return to active link position
            indicator.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            moveIndicatorTo(activeLink);
            indicator.style.opacity = '1';
        }
    }
}

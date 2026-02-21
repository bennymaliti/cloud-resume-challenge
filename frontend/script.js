// Visitor Counter Script
// This script fetches the visitor count from the API Gateway endpoint
// and updates the DOM with the current count

(function() {
    'use strict';

    // Configuration
    const config = {
        apiEndpoint: 'https://c1op5k68ii.execute-api.eu-west-2.amazonaws.com/Prod/visitor-count',
        retryAttempts: 3,
        retryDelay: 1000, // milliseconds
        timeout: 5000 // milliseconds
    };

    // Utility function to create a timeout promise
    function timeout(ms) {
        return new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Request timeout')), ms)
        );
    }

    // Fetch visitor count with retry logic
    async function fetchVisitorCount(attempt = 1) {
        const counterElement = document.getElementById('visitor-count');
        
        try {
            console.log(`Fetching visitor count (attempt ${attempt}/${config.retryAttempts})...`);
            
            // Create fetch request with timeout
            const fetchPromise = fetch(config.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors'
            });

            // Race between fetch and timeout
            const response = await Promise.race([
                fetchPromise,
                timeout(config.timeout)
            ]);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Visitor count data received:', data);

            // Extract count from response
            const count = data.count || data.visitor_count || data.visitorCount;
            
            if (typeof count === 'number') {
                updateCounter(count);
                console.log(`Successfully updated visitor count to: ${count}`);
            } else {
                throw new Error('Invalid count format in response');
            }

        } catch (error) {
            console.error(`Error fetching visitor count (attempt ${attempt}):`, error);

            // Retry logic
            if (attempt < config.retryAttempts) {
                console.log(`Retrying in ${config.retryDelay}ms...`);
                await new Promise(resolve => setTimeout(resolve, config.retryDelay));
                return fetchVisitorCount(attempt + 1);
            } else {
                // All attempts failed
                console.error('All retry attempts failed');
                counterElement.textContent = 'Error';
                counterElement.style.color = '#ef4444';
            }
        }
    }

    // Update the counter in the DOM with animation
    function updateCounter(count) {
        const counterElement = document.getElementById('visitor-count');
        
        // Animate the counter
        animateValue(counterElement, 0, count, 1000);
    }

    // Animate counter from start to end value
    function animateValue(element, start, end, duration) {
        const startTime = performance.now();
        const range = end - start;

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out cubic)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (range * easeOut));

            element.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = end.toLocaleString();
            }
        }

        requestAnimationFrame(update);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fetchVisitorCount);
    } else {
        fetchVisitorCount();
    }

    // Optional: Add analytics tracking
    function trackPageView() {
        // You can add Google Analytics or other tracking here
        console.log('Page view tracked');
    }

    // Track page view on load
    window.addEventListener('load', trackPageView);

})();

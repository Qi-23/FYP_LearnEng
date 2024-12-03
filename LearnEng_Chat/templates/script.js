// Initialize Lucide icons
lucide.createIcons();

// Scenario data
const scenarios = [
    {
        number: 1,
        title: "Hotel Booking",
        description: "Master the art of hotel reservations, from inquiring about room availability to handling special requests and checking in.",
        difficulty: "Easy",
        icon: "building-2",
        image: "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&q=80&w=1000"
    },
    {
        number: 2,
        title: "Taking a Ride",
        description: "Learn essential phrases for ride-hailing services, giving directions, and handling transportation situations confidently.",
        difficulty: "Medium",
        icon: "car",
        image: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=1000"
    },
    {
        number: 3,
        title: "Restaurant Orders",
        description: "Perfect your dining vocabulary and etiquette, from making reservations to ordering meals and handling special dietary requirements.",
        difficulty: "Hard",
        icon: "utensils",
        image: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&q=80&w=1000"
    }
];

// Create difficulty badge with appropriate number of stars
function createDifficultyBadge(difficulty) {
    const stars = {
        'Easy': 1,
        'Medium': 2,
        'Hard': 3
    };
    
    const badge = document.createElement('div');
    badge.className = 'difficulty-badge';
    
    for (let i = 0; i < stars[difficulty]; i++) {
        const star = document.createElement('i');
        star.setAttribute('data-lucide', 'star');
        badge.appendChild(star);
    }
    
    const text = document.createElement('span');
    text.textContent = difficulty;
    badge.appendChild(text);
    
    return badge;
}

// Create scenario card
function createScenarioCard(scenario) {
    const card = document.createElement('div');
    card.className = 'scenario-card';
    
    card.innerHTML = `
        <div class="card-image-container">
            <img src="${scenario.image}" alt="${scenario.title}" class="card-image">
            <div class="image-overlay"></div>
            <div class="card-title-section">
                <h3 class="card-title">${scenario.title}</h3>
                <div class="scenario-number">
                    <i data-lucide="${scenario.icon}"></i>
                    <span>Scenario ${scenario.number}</span>
                </div>
            </div>
        </div>
        <div class="card-content">
            <p class="card-description">${scenario.description}</p>
            <button class="start-button">Start Scenario</button>
        </div>
    `;
    
    // Insert difficulty badge
    const imageContainer = card.querySelector('.card-image-container');
    imageContainer.appendChild(createDifficultyBadge(scenario.difficulty));
    
    // Add click handler
    const startButton = card.querySelector('.start-button');
    startButton.addEventListener('click', () => {
        console.log(`Starting scenario ${scenario.number}`);
    });
    
    return card;
}

// Render scenarios
function renderScenarios() {
    const container = document.getElementById('scenariosContainer');
    scenarios.forEach(scenario => {
        container.appendChild(createScenarioCard(scenario));
    });
    // Reinitialize icons for dynamically added content
    lucide.createIcons();
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    renderScenarios();
    
    // Add click handlers for header buttons
    document.querySelectorAll('.icon-button').forEach(button => {
        button.addEventListener('click', () => {
            console.log('Button clicked:', button.getAttribute('aria-label'));
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation de la carte de la pharmacie
    initPharmacyMap();

    // Éléments interactifs
    setupDraggableElements();
    setupElementClicks();
    setupToolbar();
});

function initPharmacyMap() {
    const pharmacyMap = document.getElementById('pharmacy-map');
    if (!pharmacyMap) return;

    // Récupération des données de la pharmacie
    const pharmacyId = pharmacyMap.dataset.pharmacyId;
    const pharmacyWidth = parseInt(pharmacyMap.dataset.width);
    const pharmacyHeight = parseInt(pharmacyMap.dataset.height);

    // Configuration de la taille de la carte
    pharmacyMap.style.width = `${pharmacyWidth}px`;
    pharmacyMap.style.height = `${pharmacyHeight}px`;

    // Chargement des éléments de la pharmacie
    loadPharmacyElements(pharmacyId);
}

function loadPharmacyElements(pharmacyId) {
    fetch(`/api/pharmacy/${pharmacyId}/elements/`)
        .then(response => response.json())
        .then(data => {
            renderElements(data.elements);
        })
        .catch(error => {
            console.error('Erreur lors du chargement des éléments:', error);
        });
}

function renderElements(elements) {
    const pharmacyMap = document.getElementById('pharmacy-map');
    
    elements.forEach(element => {
        const elementDiv = document.createElement('div');
        elementDiv.id = `element-${element.id}`;
        elementDiv.className = `pharmacy-element ${element.element_type.toLowerCase()}`;
        elementDiv.dataset.elementId = element.id;
        elementDiv.dataset.elementType = element.element_type;
        
        // Positionnement et dimensions
        elementDiv.style.left = `${element.x}px`;
        elementDiv.style.top = `${element.y}px`;
        elementDiv.style.width = `${element.width}px`;
        elementDiv.style.height = `${element.height}px`;
        
        // Contenu de l'élément
        const elementName = document.createElement('div');
        elementName.className = 'element-name';
        elementName.textContent = element.name;
        
        const elementLab = document.createElement('div');
        elementLab.className = 'element-lab';
        elementLab.textContent = element.laboratory || '';
        
        elementDiv.appendChild(elementName);
        elementDiv.appendChild(elementLab);
        
        pharmacyMap.appendChild(elementDiv);
    });
}

function setupDraggableElements() {
    // Configuration des éléments glissables avec interact.js
    interact('.pharmacy-element').draggable({
        inertia: true,
        modifiers: [
            interact.modifiers.restrictRect({
                restriction: 'parent',
                endOnly: true
            })
        ],
        autoScroll: true,
        
        listeners: {
            move: dragMoveListener,
            end: function (event) {
                // Mise à jour de la position dans la base de données
                const elementId = event.target.dataset.elementId;
                const x = parseInt(event.target.style.left);
                const y = parseInt(event.target.style.top);
                
                updateElementPosition(elementId, x, y);
            }
        }
    });
}

function dragMoveListener(event) {
    const target = event.target;
    
    // Récupération de la position actuelle
    const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
    const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;
    
    // Mise à jour de la position CSS
    target.style.transform = `translate(${x}px, ${y}px)`;
    
    // Stockage de la position
    target.setAttribute('data-x', x);
    target.setAttribute('data-y', y);
}

function updateElementPosition(elementId, x, y) {
    fetch(`/api/element/${elementId}/update/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            x: x,
            y: y
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Erreur:', data.error);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

function setupElementClicks() {
    document.addEventListener('click', function(event) {
        // Vérification si l'élément cliqué est un élément de la pharmacie
        const element = event.target.closest('.pharmacy-element');
        if (!element) return;
        
        // Récupération de l'ID de l'élément
        const elementId = element.dataset.elementId;
        
        // Affichage des détails de l'élément
        showElementDetails(elementId);
        
        // Mise en évidence de l'élément sélectionné
        document.querySelectorAll('.pharmacy-element').forEach(el => {
            el.classList.remove('selected');
        });
        element.classList.add('selected');
    });
}

function showElementDetails(elementId) {
    fetch(`/api/element/${elementId}/`)
        .then(response => response.json())
        .then(data => {
            // Mise à jour du panneau de détails
            const detailsPanel = document.getElementById('element-details-panel');
            populateDetailsPanel(detailsPanel, data);
            
            // Affichage du panneau s'il est caché
            detailsPanel.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Erreur lors du chargement des détails:', error);
        });
}

function populateDetailsPanel(panel, elementData) {
    // Mise à jour du titre
    panel.querySelector('.element-title').textContent = elementData.name;
    
    // Mise à jour du type
    panel.querySelector('.element-type').textContent = getElementTypeLabel(elementData.type);
    
    // Mise à jour du laboratoire
    const labSelect = panel.querySelector('#laboratory-select');
    if (elementData.laboratory) {
        [...labSelect.options].forEach(option => {
            if (option.textContent === elementData.laboratory) {
                option.selected = true;
            }
        });
    } else {
        labSelect.value = '';
    }
    
    // Mise à jour des données de vente
    panel.querySelector('.revenue-value').textContent = `${elementData.revenue.toFixed(2)} €`;
    panel.querySelector('.profit-value').textContent = `${elementData.profit.toFixed(2)} €`;
    panel.querySelector('.margin-value').textContent = `${elementData.margin_percentage.toFixed(2)}%`;
    panel.querySelector('.units-value').textContent = elementData.units_sold;
    
    // Mise à jour de la liste des produits
    const productsList = panel.querySelector('.products-list');
    productsList.innerHTML = '';
    
    elementData.products.forEach(product => {
        const li = document.createElement('li');
        li.textContent = product.name;
        productsList.appendChild(li);
    });
}

function getElementTypeLabel(type) {
    const types = {
        'SHELF': 'Rayon',
        'TG': 'Tête de Gondole',
        'BAC': 'Bac Soldeur',
        'ENTRANCE': 'Entrée',
        'EXIT': 'Sortie',
        'COUNTER': 'Comptoir'
    };
    
    return types[type] || type;
}

function setupToolbar() {
    // Bouton d'ajout d'élément
    const addButton = document.getElementById('add-element-btn');
    if (addButton) {
        addButton.addEventListener('click', function() {
            showAddElementForm();
        });
    }
    
    // Bouton d'export du plan
    const exportButton = document.getElementById('export-plan-btn');
    if (exportButton) {
        exportButton.addEventListener('click', function() {
            exportPharmacyPlan();
        });
    }
}

function showAddElementForm() {
    const modal = document.getElementById('add-element-modal');
    modal.classList.remove('hidden');
}

function exportPharmacyPlan() {
    const pharmacyMap = document.getElementById('pharmacy-map');
    const pharmacyId = pharmacyMap.dataset.pharmacyId;
    
    window.location.href = `/pharmacy/${pharmacyId}/export/`;
}

// Utilitaire pour récupérer le token CSRF
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
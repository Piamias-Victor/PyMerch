document.addEventListener('DOMContentLoaded', function() {
    // Initialisation de la vue spéciale
    initSpecialView();
});

function initSpecialView() {
    const pharmacyMap = document.getElementById('pharmacy-map');
    if (!pharmacyMap) return;

    // Récupération des données de la pharmacie
    const pharmacyId = pharmacyMap.dataset.pharmacyId;
    const viewType = pharmacyMap.dataset.viewType;

    // Configuration de la taille de la carte
    pharmacyMap.style.width = `${pharmacyMap.dataset.width}px`;
    pharmacyMap.style.height = `${pharmacyMap.dataset.height}px`;

    // Chargement des éléments de la pharmacie
    loadPharmacyElements(pharmacyId, viewType);
}

function loadPharmacyElements(pharmacyId, viewType) {
    fetch(`/api/pharmacy/${pharmacyId}/elements/`)
        .then(response => response.json())
        .then(data => {
            renderElements(data.elements, viewType);
        })
        .catch(error => {
            console.error('Erreur lors du chargement des éléments:', error);
        });
}

function renderElements(elements, viewType) {
    const pharmacyMap = document.getElementById('pharmacy-map');
    
    // Si c'est une vue par laboratoire, créer une palette de couleurs pour les laboratoires
    let labColors = {};
    if (viewType === 'lab') {
        // Extraire les laboratoires uniques
        const labs = [...new Set(elements.filter(e => e.laboratory).map(e => e.laboratory))];
        
        // Assigner une couleur à chaque laboratoire
        const colors = [
            '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796',
            '#5a5c69', '#2e59d9', '#17a673', '#2c9faf', '#6610f2', '#e83e8c'
        ];
        
        labs.forEach((lab, index) => {
            labColors[lab] = colors[index % colors.length];
        });
        
        // Mettre à jour la légende des laboratoires
        updateLabLegend(labColors);
    }
    
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
        
        // Appliquer la couleur en fonction du type de vue
        if (viewType === 'revenue') {
            elementDiv.style.backgroundColor = getRevenueColor(element.sales_data?.revenue || 0);
            elementDiv.style.color = getContrastColor(element.sales_data?.revenue || 0);
        } else if (viewType === 'margin') {
            const marginPct = element.sales_data?.revenue > 0 
                ? (element.sales_data?.profit / element.sales_data?.revenue) * 100 
                : 0;
            elementDiv.style.backgroundColor = getMarginColor(marginPct);
            elementDiv.style.color = getContrastColor(marginPct);
        } else if (viewType === 'lab' && element.laboratory) {
            elementDiv.style.backgroundColor = labColors[element.laboratory] || '#ffffff';
            elementDiv.style.color = '#000000';
        }
        
        // Contenu de l'élément
        const elementName = document.createElement('div');
        elementName.className = 'element-name';
        elementName.textContent = element.name;
        
        const elementData = document.createElement('div');
        elementData.className = 'element-data';
        
        if (viewType === 'revenue') {
            elementData.textContent = `${(element.sales_data?.revenue || 0).toFixed(0)} €`;
        } else if (viewType === 'margin') {
            const marginPct = element.sales_data?.revenue > 0 
                ? (element.sales_data?.profit / element.sales_data?.revenue) * 100 
                : 0;
            elementData.textContent = `${marginPct.toFixed(1)}%`;
        } else if (viewType === 'lab') {
            elementData.textContent = element.laboratory || '-';
        }
        
        elementDiv.appendChild(elementName);
        elementDiv.appendChild(elementData);
        
        pharmacyMap.appendChild(elementDiv);
    });
}

function updateLabLegend(labColors) {
    const legendContainer = document.getElementById('lab-legend');
    if (!legendContainer) return;
    
    legendContainer.innerHTML = '';
    
    // Créer un élément de légende pour chaque laboratoire
    Object.entries(labColors).forEach(([lab, color]) => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        
        const colorBox = document.createElement('div');
        colorBox.className = 'legend-color';
        colorBox.style.backgroundColor = color;
        
        const labName = document.createElement('span');
        labName.textContent = lab;
        
        legendItem.appendChild(colorBox);
        legendItem.appendChild(labName);
        
        legendContainer.appendChild(legendItem);
    });
}

function getRevenueColor(revenue) {
    if (revenue > 1000) return '#63be7b';  // Vert foncé
    if (revenue > 500) return '#a6d96a';   // Vert clair
    if (revenue > 100) return '#ffeb84';   // Jaune
    return '#f8696b';                      // Rouge
}

function getMarginColor(marginPct) {
    if (marginPct > 30) return '#63be7b';  // Vert foncé
    if (marginPct > 20) return '#a6d96a';  // Vert clair
    if (marginPct > 10) return '#ffeb84';  // Jaune
    return '#f8696b';                      // Rouge
}

function getContrastColor(value) {
    // Retourne une couleur de texte qui contraste avec la couleur de fond
    return value > 500 ? 'white' : 'black';
}
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des graphiques
    initRevenueByTypeChart();
    initProfitByTypeChart();
    initRevenueByLabChart();
    initProfitByLabChart();
    initMarginHeatmap();
    
    // Bouton d'export
    const exportBtn = document.getElementById('export-data-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportData);
    }
});

function initRevenueByTypeChart() {
    const canvas = document.getElementById('revenue-by-type-chart');
    if (!canvas) return;
    
    // Récupération des données via l'API
    fetch(`/api/pharmacy/${canvas.closest('.container-fluid').dataset.pharmacyId}/stats/by-type/`)
        .then(response => response.json())
        .then(data => {
            // Extraction des données
            const labels = data.map(item => getElementTypeLabel(item.element_type));
            const values = data.map(item => item.total_revenue);
            
            // Création du graphique
            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Chiffre d\'affaires (€)',
                        data: values,
                        backgroundColor: [
                            '#4e73df',
                            '#1cc88a',
                            '#36b9cc',
                            '#f6c23e',
                            '#e74a3b',
                            '#858796'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value + ' €';
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.parsed.y.toFixed(2) + ' €';
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement des données:', error);
        });
}

function initProfitByTypeChart() {
    const canvas = document.getElementById('profit-by-type-chart');
    if (!canvas) return;
    
    // Récupération des données via l'API
    fetch(`/api/pharmacy/${canvas.closest('.container-fluid').dataset.pharmacyId}/stats/by-type/`)
        .then(response => response.json())
        .then(data => {
            // Extraction des données
            const labels = data.map(item => getElementTypeLabel(item.element_type));
            const values = data.map(item => item.total_profit);
            
            // Création du graphique
            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Marge (€)',
                        data: values,
                        backgroundColor: [
                            '#4e73df',
                            '#1cc88a',
                            '#36b9cc',
                            '#f6c23e',
                            '#e74a3b',
                            '#858796'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value + ' €';
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.parsed.y.toFixed(2) + ' €';
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement des données:', error);
        });
}

function initRevenueByLabChart() {
    const canvas = document.getElementById('revenue-by-lab-chart');
    if (!canvas) return;
    
    // Récupération des données via l'API
    fetch(`/api/pharmacy/${canvas.closest('.container-fluid').dataset.pharmacyId}/stats/by-lab/`)
        .then(response => response.json())
        .then(data => {
            // Extraction des données
            const labels = data.map(item => item.laboratory__name);
            const values = data.map(item => item.total_revenue);
            
            // Création du graphique
            new Chart(canvas, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            '#4e73df',
                            '#1cc88a',
                            '#36b9cc',
                            '#f6c23e',
                            '#e74a3b',
                            '#858796',
                            '#5a5c69',
                            '#2e59d9',
                            '#17a673',
                            '#2c9faf'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw.toFixed(2) + ' €';
                                    const percentage = (context.raw / values.reduce((a, b) => a + b, 0) * 100).toFixed(2) + '%';
                                    return context.label + ': ' + value + ' (' + percentage + ')';
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement des données:', error);
        });
}

function initProfitByLabChart() {
    const canvas = document.getElementById('profit-by-lab-chart');
    if (!canvas) return;
    
    // Récupération des données via l'API
    fetch(`/api/pharmacy/${canvas.closest('.container-fluid').dataset.pharmacyId}/stats/by-lab/`)
        .then(response => response.json())
        .then(data => {
            // Extraction des données
            const labels = data.map(item => item.laboratory__name);
            const values = data.map(item => item.total_profit);
            
            // Création du graphique
            new Chart(canvas, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            '#4e73df',
                            '#1cc88a',
                            '#36b9cc',
                            '#f6c23e',
                            '#e74a3b',
                            '#858796',
                            '#5a5c69',
                            '#2e59d9',
                            '#17a673',
                            '#2c9faf'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw.toFixed(2) + ' €';
                                    const percentage = (context.raw / values.reduce((a, b) => a + b, 0) * 100).toFixed(2) + '%';
                                    return context.label + ': ' + value + ' (' + percentage + ')';
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement des données:', error);
        });
}

function initMarginHeatmap() {
    const heatmapContainer = document.getElementById('margin-heatmap');
    if (!heatmapContainer) return;
    
    // Récupération des données des éléments pour la carte de chaleur
    fetch(`/api/pharmacy/${heatmapContainer.dataset.pharmacyId}/elements/`)
        .then(response => response.json())
        .then(data => {
            // Création de la carte de chaleur
            renderHeatmap(heatmapContainer, data.elements);
        })
        .catch(error => {
            console.error('Erreur lors du chargement des données:', error);
        });
}

function renderHeatmap(container, elements) {
    // Dimensions du conteneur
    container.style.width = `${container.dataset.width}px`;
    container.style.height = `${container.dataset.height}px`;
    container.style.position = 'relative';
    container.style.border = '1px solid #ddd';
    container.style.backgroundColor = '#f5f5f5';
    
    // Rendu des éléments avec coloration selon leur taux de marge
    elements.forEach(element => {
        // Calcul du taux de marge
        let marginPct = 0;
        if (element.sales_data && element.sales_data.revenue > 0) {
            marginPct = (element.sales_data.profit / element.sales_data.revenue) * 100;
        }
        
        // Création de l'élément de la carte de chaleur
        const div = document.createElement('div');
        div.style.position = 'absolute';
        div.style.left = `${element.x}px`;
        div.style.top = `${element.y}px`;
        div.style.width = `${element.width}px`;
        div.style.height = `${element.height}px`;
        div.style.backgroundColor = getHeatmapColor(marginPct);
        div.style.border = '1px solid #333';
        div.style.borderRadius = '3px';
        div.style.display = 'flex';
        div.style.flexDirection = 'column';
        div.style.justifyContent = 'center';
        div.style.alignItems = 'center';
        div.style.padding = '2px';
        div.style.boxSizing = 'border-box';
        div.style.fontSize = '10px';
        div.style.color = marginPct > 30 ? 'white' : 'black';
        
        // Nom de l'élément
        const nameSpan = document.createElement('span');
        nameSpan.textContent = element.name;
        nameSpan.style.fontWeight = 'bold';
        nameSpan.style.whiteSpace = 'nowrap';
        nameSpan.style.overflow = 'hidden';
        nameSpan.style.textOverflow = 'ellipsis';
        nameSpan.style.width = '100%';
        nameSpan.style.textAlign = 'center';
        
        // Taux de marge
        const marginSpan = document.createElement('span');
        marginSpan.textContent = `${marginPct.toFixed(1)}%`;
        
        div.appendChild(nameSpan);
        div.appendChild(marginSpan);
        
        container.appendChild(div);
    });
}

function getHeatmapColor(value) {
    // Couleur de la carte de chaleur basée sur le taux de marge
    if (value <= 0) return '#f8696b';  // Rouge pour les marges négatives
    if (value < 15) return '#ffeb84';  // Jaune pour les marges faibles
    if (value < 30) return '#a6d96a';  // Vert clair pour les marges moyennes
    return '#63be7b';  // Vert foncé pour les bonnes marges
}

function exportData() {
    const pharmacyId = document.querySelector('.container-fluid').dataset.pharmacyId;
    window.location.href = `/pharmacy/${pharmacyId}/export-data/`;
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
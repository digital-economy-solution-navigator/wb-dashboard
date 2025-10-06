// Global state
let allIndicatorsData = [];
let filteredData = [];

// Initialize dashboard
async function initDashboard() {
    try {
        const response = await fetch('data/standardized_data/consolidated_dataset.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        allIndicatorsData = data.data_points || [];
        
        console.log('Loaded data:', allIndicatorsData.length, 'data points');
        
        populateFilters();
        applyFilters();
        
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('summary').innerHTML = 
            `<div class="error">Error loading data: ${error.message}</div>`;
    }
}

// Populate filter dropdowns
function populateFilters() {
    // Get unique countries and sort them
    const countries = [...new Set(allIndicatorsData.map(d => d.country))].sort();
    const countrySelect = document.getElementById('countryFilter');
    countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country;
        option.textContent = country;
        countrySelect.appendChild(option);
    });
    
    // Get unique indicators and sort them
    const indicators = [...new Set(allIndicatorsData.map(d => d.indicator))].sort();
    const indicatorSelect = document.getElementById('indicatorFilter');
    indicators.forEach(indicator => {
        const option = document.createElement('option');
        option.value = indicator;
        option.textContent = indicator;
        indicatorSelect.appendChild(option);
    });
    
    // Populate year range (2015-2022)
    const years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022];
    const yearFromSelect = document.getElementById('yearFromFilter');
    const yearToSelect = document.getElementById('yearToFilter');
    
    years.forEach(year => {
        const fromOption = document.createElement('option');
        fromOption.value = year;
        fromOption.textContent = year;
        yearFromSelect.appendChild(fromOption);
        
        const toOption = document.createElement('option');
        toOption.value = year;
        toOption.textContent = year;
        yearToSelect.appendChild(toOption);
    });
    
    // Set default year range
    yearFromSelect.value = '2015';
    yearToSelect.value = '2022';
}

// Get current filter values
function getFilters() {
    return {
        country: document.getElementById('countryFilter').value,
        indicator: document.getElementById('indicatorFilter').value,
        yearFrom: document.getElementById('yearFromFilter').value,
        yearTo: document.getElementById('yearToFilter').value,
        layer: document.getElementById('layerFilter').value
    };
}

// Apply filters to data
function applyFilters(data = allIndicatorsData, filters = getFilters()) {
    console.log('applyFilters called with:', { dataLength: data?.length, filters });
    
    // Ensure data is available and is an array
    if (!data || !Array.isArray(data) || data.length === 0) {
        console.error('No data available for filtering');
        document.getElementById('summary').textContent = 'No data available';
        document.getElementById('preview-container').innerHTML = '<div class="no-data">No data available</div>';
        return;
    }
    
    let filtered = [...data];
    console.log('Starting with', filtered.length, 'data points');
    
    // Filter by country
    if (filters.country) {
        const beforeCount = filtered.length;
        filtered = filtered.filter(d => d.country === filters.country);
        console.log(`Country filter (${filters.country}): ${beforeCount} -> ${filtered.length}`);
    }
    
    // Filter by indicator
    if (filters.indicator) {
        const beforeCount = filtered.length;
        filtered = filtered.filter(d => d.indicator === filters.indicator);
        console.log(`Indicator filter (${filters.indicator}): ${beforeCount} -> ${filtered.length}`);
    }
    
    // Filter by year range
    if (filters.yearFrom) {
        const yearFrom = parseInt(filters.yearFrom);
        const beforeCount = filtered.length;
        filtered = filtered.filter(d => d.year >= yearFrom);
        console.log(`Year from filter (${yearFrom}): ${beforeCount} -> ${filtered.length}`);
    }
    
    if (filters.yearTo) {
        const yearTo = parseInt(filters.yearTo);
        const beforeCount = filtered.length;
        filtered = filtered.filter(d => d.year <= yearTo);
        console.log(`Year to filter (${yearTo}): ${beforeCount} -> ${filtered.length}`);
    }
    
    // Validate year range
    if (filters.yearFrom && filters.yearTo) {
        const yearFrom = parseInt(filters.yearFrom);
        const yearTo = parseInt(filters.yearTo);
        if (yearFrom > yearTo) {
            alert('From year must be less than or equal to To year');
            return;
        }
    }
    
    // Filter out rows with missing values
    const beforeCount = filtered.length;
    filtered = filtered.filter(d => 
        d.value !== null && 
        d.value !== undefined && 
        !isNaN(d.value)
    );
    console.log(`Value filter (removing null/NaN): ${beforeCount} -> ${filtered.length}`);
    
    // Layer filter (placeholder for future)
    if (filters.layer && filters.layer !== 'All') {
        // Future: implement layer filtering
    }
    
    filteredData = filtered;
    console.log('Final filtered data:', filteredData.length, 'points');
    renderResults();
}

// Render results
function renderResults() {
    renderSummary(filteredData.length);
    renderPreview(filteredData.slice(0, 10));
}

// Render summary
function renderSummary(count) {
    document.getElementById('summary').textContent = 
        `${count} points after filter`;
}

// Render preview table
function renderPreview(rows) {
    const container = document.getElementById('preview-container');
    
    if (rows.length === 0) {
        container.innerHTML = '<div class="no-data">No data matches the current filters</div>';
        return;
    }
    
    let tableHtml = `
        <table class="preview-table">
            <thead>
                <tr>
                    <th>Indicator</th>
                    <th>Country</th>
                    <th>Year</th>
                    <th>Value</th>
                    <th>Category</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    rows.forEach(row => {
        tableHtml += `
            <tr>
                <td>${row.indicator}</td>
                <td>${row.country}</td>
                <td>${row.year}</td>
                <td>${row.value.toLocaleString()}</td>
                <td>${row.category}</td>
            </tr>
        `;
    });
    
    tableHtml += '</tbody></table>';
    
    container.innerHTML = tableHtml;
}

// Regional average helper (placeholder)
function computeRegionalAverage(filteredData) {
    // Future: average by {indicator, year} across all countries in region
    console.log('Regional average computation (placeholder):', {
        dataPoints: filteredData.length,
        indicators: [...new Set(filteredData.map(d => d.indicator))],
        years: [...new Set(filteredData.map(d => d.year))].sort()
    });
    return null; // return shape { [year]: avgValue }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initDashboard();
    
    // Filter change events - removed automatic filtering
    // Now filtering only happens when "Apply Filters" button is clicked
    
    // Button events
    document.getElementById('applyFilters').addEventListener('click', function() {
        applyFilters();
    });
    document.getElementById('clearFilters').addEventListener('click', function() {
        document.getElementById('countryFilter').value = '';
        document.getElementById('indicatorFilter').value = '';
        document.getElementById('yearFromFilter').value = '2015';
        document.getElementById('yearToFilter').value = '2022';
        document.getElementById('layerFilter').value = '';
        applyFilters();
    });
});

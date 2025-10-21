// Global state
let allIndicatorsData = [];
let filteredData = [];
let metadata = null;

// Initialize dashboard
async function initDashboard() {
    try {
                const response = await fetch('data/transformed_data_v2/consolidated_dataset.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        allIndicatorsData = data.data_points || [];
        metadata = data.metadata || {};
        
    console.log('Loaded data:', allIndicatorsData.length, 'data points');
    console.log('Sample data point:', allIndicatorsData[0]);
    console.log('Available indicators in metadata:', metadata.indicators);
    console.log('Metadata:', metadata);
    
    // Debug: Check what indicators are actually in the data
    const actualIndicators = [...new Set(allIndicatorsData.map(d => d.indicator))];
    console.log('Actual indicators in data:', actualIndicators);
    console.log('Count of data points per indicator:');
    actualIndicators.forEach(indicator => {
        const count = allIndicatorsData.filter(d => d.indicator === indicator).length;
        console.log(`  ${indicator}: ${count} data points`);
    });
        
        // Ensure DOM is ready before populating filters
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                populateFilters();
                applyFilters();
            });
        } else {
            populateFilters();
            applyFilters();
        }
        
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('summary').innerHTML = 
            `<div class="error">
                <h3>⚠️ Data Loading Error</h3>
                <p><strong>Error:</strong> ${error.message}</p>
                <p><strong>Possible solutions:</strong></p>
                <ul>
                    <li>Run the data transformation script: <code>cd data && python transform_data_v2.py</code></li>
                    <li>Or use the simple version: <code>cd data && python simple_transform.py</code></li>
                    <li>Check that data.xlsx exists in the data/ directory</li>
                    <li>Verify the transformation completed successfully</li>
                </ul>
                <p><em>Check the browser console for more details.</em></p>
            </div>`;
        
        // Show empty filters
        populateEmptyFilters();
    }
}

// Populate filter dropdowns
function populateFilters() {
    console.log('populateFilters called with data length:', allIndicatorsData.length);
    console.log('Metadata available:', metadata);
    
    // Get unique countries and sort them
    const countries = [...new Set(allIndicatorsData.map(d => d.country))].sort();
    console.log('Found countries:', countries);
    const countrySelect = document.getElementById('countryFilter');
    countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country;
        option.textContent = country;
        countrySelect.appendChild(option);
    });
    
    // Use metadata indicators if available, otherwise extract from data
    let indicators = [];
    if (metadata && metadata.indicators && metadata.indicators.length > 0) {
        indicators = [...metadata.indicators].sort();
        console.log('Using metadata indicators:', indicators);
    } else {
        indicators = [...new Set(allIndicatorsData.map(d => d.indicator))].sort();
        console.log('Extracted indicators from data:', indicators);
    }
    
    const indicatorSelect = document.getElementById('indicatorFilter');
    console.log('Indicator select element:', indicatorSelect);
    console.log('Current indicator select innerHTML:', indicatorSelect.innerHTML);
    
    // Clear existing options first
    indicatorSelect.innerHTML = '<option value="">All Indicators</option>';
    
    indicators.forEach(indicator => {
        const option = document.createElement('option');
        option.value = indicator;
        option.textContent = indicator;
        indicatorSelect.appendChild(option);
        console.log('Added indicator option:', indicator);
    });
    
    console.log('Final indicator select innerHTML:', indicatorSelect.innerHTML);
    console.log('Number of options in indicator select:', indicatorSelect.options.length);
    
    // Test: Try to manually add a test option to verify the dropdown works
    const testOption = document.createElement('option');
    testOption.value = 'TEST_INDICATOR';
    testOption.textContent = 'TEST INDICATOR';
    indicatorSelect.appendChild(testOption);
    console.log('Added test option, total options now:', indicatorSelect.options.length);
    
    // Populate year filter dynamically from data
    const years = [...new Set(allIndicatorsData.map(d => d.year))].filter(y => y).sort();
    console.log('Found years:', years);
    const yearSelect = document.getElementById('yearFilter');
    
    years.forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    });
}

// Populate empty filters when data is not available
function populateEmptyFilters() {
    // Clear existing options
    document.getElementById('countryFilter').innerHTML = '<option value="">All Countries</option>';
    document.getElementById('indicatorFilter').innerHTML = '<option value="">All Indicators</option>';
    document.getElementById('yearFilter').innerHTML = '<option value="">All Years</option>';
    
    // Show message in preview
    document.getElementById('preview-container').innerHTML = 
        '<div class="no-data">No data available. Please run the data transformation script first.</div>';
}

// Get current filter values
function getFilters() {
    return {
        country: document.getElementById('countryFilter').value,
        indicator: document.getElementById('indicatorFilter').value,
        year: document.getElementById('yearFilter').value
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
        console.log('Before indicator filter - sample data points:', filtered.slice(0, 3).map(d => ({ indicator: d.indicator, country: d.country, year: d.year })));
        filtered = filtered.filter(d => d.indicator === filters.indicator);
        console.log(`Indicator filter (${filters.indicator}): ${beforeCount} -> ${filtered.length}`);
        console.log('After indicator filter - sample results:', filtered.slice(0, 3).map(d => ({ indicator: d.indicator, country: d.country, year: d.year })));
    }
    
    // Filter by year
    if (filters.year) {
        const year = parseInt(filters.year);
        const beforeCount = filtered.length;
        filtered = filtered.filter(d => d.year === year);
        console.log(`Year filter (${year}): ${beforeCount} -> ${filtered.length}`);
    }
    
    // Filter out rows with missing values
    const beforeCount = filtered.length;
    filtered = filtered.filter(d => 
        d.value !== null && 
        d.value !== undefined && 
        !isNaN(d.value)
    );
    console.log(`Value filter (removing null/NaN): ${beforeCount} -> ${filtered.length}`);
    
    
    filteredData = filtered;
    console.log('Final filtered data:', filteredData.length, 'points');
    renderResults();
}

// Render results
function renderResults() {
    renderSummary(filteredData.length);
    renderPreview(filteredData);
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
    
    // Smart optimization: Limit preview to 255 rows for better performance
    const maxPreviewRows = 255;
    const displayRows = rows.slice(0, maxPreviewRows);
    const hasMoreData = rows.length > maxPreviewRows;
    
    let tableHtml = `
        <table class="preview-table">
            <thead>
                <tr>
                    <th>Indicator</th>
                    <th>Country</th>
                    <th>Year</th>
                    <th>Value</th>
                    <th>Category</th>
                    <th>Layer</th>
                    <th>Unit</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    displayRows.forEach(row => {
        tableHtml += `
            <tr>
                <td>${row.indicator}</td>
                <td>${row.country}</td>
                <td>${row.year}</td>
                <td>${row.value.toLocaleString()}</td>
                <td>${row.category}</td>
                <td>${row.layer || 'Unknown'}</td>
                <td>${row.unit || 'Unknown'}</td>
            </tr>
        `;
    });
    
    tableHtml += '</tbody></table>';
    
    // Add note if data is truncated
    if (hasMoreData) {
        tableHtml += `<div class="data-truncated">📊 Showing first ${maxPreviewRows} of ${rows.length} results. Use filters to narrow down your search.</div>`;
    }
    
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
    
    // Automatic filtering on filter change
    document.getElementById('countryFilter').addEventListener('change', function() {
        applyFilters();
    });
    document.getElementById('indicatorFilter').addEventListener('change', function() {
        applyFilters();
    });
    document.getElementById('yearFilter').addEventListener('change', function() {
        applyFilters();
    });
    
    // Clear filters button
    document.getElementById('clearFilters').addEventListener('click', function() {
        document.getElementById('countryFilter').value = '';
        document.getElementById('indicatorFilter').value = '';
        document.getElementById('yearFilter').value = '';
        applyFilters();
    });
});

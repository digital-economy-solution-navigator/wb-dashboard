# Western Balkans Dashboard

A comprehensive dashboard for analyzing Western Balkans development indicators based on the new 17-indicator framework.

## Framework Overview

The dashboard is built around a comprehensive framework covering:

### 🧩 Foundational Capabilities (14 indicators)

#### A. Enabling Infrastructure
- **Energy**
  1. Energy availability — Electricity consumption per capita
  2. Energy reliability — Percentage of firms experiencing electrical outages

- **Digital**
  3. Access to digital connectivity — Fixed broadband subscriptions per 100 people
  4. Quality of connectivity — Mean download speed (Mbps)

#### B. Production Capabilities
- **Basic**
  5. Productive investments — Gross Fixed Capital Formation (GFCF, % of GDP)
  6. Productive skills — Mean years of schooling

- **Intermediate**
  7. Operational efficiency — ISO 9001 certificates
  8. Technology absorption — Intellectual Property Right payments (royalties, % of GDP)

#### C. Innovation Capabilities
- **Basic (Effort)**
  9. Advanced skills — Gross enrolment ratio in tertiary education
  10. Specialized skills — Percentage of graduates from STEM programmes in tertiary education
  11. Research effort — Gross Expenditure in R&D (% of GDP)

- **Intermediate (Output)**
  12. Research output — Scientific and technical journal articles per million people
  13. Innovation output (patents) — Total patents in force per 100 billion USD GDP
  14. Innovation output (royalties) — Intellectual Property Right receipts (royalties, % of GDP)

### 💻 Digital Capabilities (3 indicators)

#### A. Absorption & Exposure
15. Absorption and exposure to production technologies with digital potential → Imports of production technologies (% of GDP)

#### B. Deployment & Adaptation
16. Deployment and adaptation of digital production technologies → Imports of digital products (% of GDP)
17. Industrial competitiveness in digital technologies → Exports of digital products (% of GDP)

## Data Structure

The dashboard expects data in the following format:

```json
{
  "metadata": {
    "title": "Western Balkans Dashboard Data",
    "transformation_date": "2024-01-01T00:00:00",
    "total_points": 1000,
    "countries": ["Albania", "Bosnia and Herzegovina", ...],
    "years": [2015, 2016, 2017, ...],
    "indicators": ["Energy availability", "Energy reliability", ...],
    "categories": ["Foundational Capabilities", "Digital Capabilities"]
  },
  "data_points": [
    {
      "indicator": "Energy availability",
      "country": "Albania",
      "year": 2020,
      "value": 1500.5,
      "category": "Foundational Capabilities",
      "subcategory": "Enabling Infrastructure - Energy",
      "layer": "Basic",
      "unit": "kWh per capita",
      "sheet_source": "Energy_Data"
    }
  ]
}
```

## Setup Instructions

### 1. Data Transformation

Run the data transformation script to convert your Excel data:

```bash
cd data
python transform_data_v2.py
```

This will create:
- `transformed_data_v2/consolidated_dataset.json` - Main dataset
- `transformed_data_v2/transformation_summary.json` - Processing summary
- `transformed_data_v2/indicator_framework.json` - Framework definition
- `transformed_data_v2/indicator_mapping.json` - Flattened mapping

### 2. Alternative Simple Transformation

For a simpler approach:

```bash
cd data
python simple_transform.py
```

This creates:
- `transformed_data/consolidated_dataset.json` - Simplified dataset

### 3. Update Dashboard

The dashboard is already configured to load from `data/transformed_data_v2/consolidated_dataset.json`. If you use the simple transformation, update `script.js` line 8:

```javascript
const response = await fetch('data/transformed_data/consolidated_dataset.json');
```

## Features

### Filtering
- **Country**: Filter by specific countries
- **Indicator**: Filter by specific indicators
- **Year Range**: Filter by year range (dynamically populated from data)
- **Layer**: Filter by capability layer (Basic, Intermediate, Advanced)

### Data Display
- **Summary**: Shows count of filtered data points
- **Preview Table**: Displays filtered data with columns:
  - Indicator
  - Country
  - Year
  - Value
  - Category
  - Layer
  - Unit

### Controls
- **Apply Filters**: Apply current filter settings
- **Clear Filters**: Reset all filters to default values

## File Structure

```
wb-dashboard/
├── data/
│   ├── data.xlsx                    # Source Excel file
│   ├── transform_data_v2.py         # Comprehensive transformation script
│   ├── simple_transform.py          # Simple transformation script
│   └── transformed_data_v2/         # Output directory
│       ├── consolidated_dataset.json
│       ├── transformation_summary.json
│       ├── indicator_framework.json
│       └── indicator_mapping.json
├── index.html                       # Main dashboard page
├── script.js                        # Dashboard JavaScript
├── styles.css                       # Dashboard styling
└── README.md                        # This file
```

## Requirements

- Python 3.7+
- pandas
- openpyxl (for Excel file reading)

Install requirements:
```bash
pip install pandas openpyxl
```

## Usage

1. Place your Excel data file as `data/data.xlsx`
2. Run the transformation script
3. Open `index.html` in a web browser
4. Use the filters to explore the data

## Data Format Requirements

The Excel file should contain sheets with data in a format that can be automatically detected:

- **Country column**: Contains country names
- **Year column**: Contains year values
- **Value columns**: Contains numeric indicator values
- **Indicator column** (optional): Contains indicator names

The transformation script will automatically detect these columns and structure the data appropriately.

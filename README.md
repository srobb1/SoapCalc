# Sofia's Soap Calculator

A web-based soap recipe calculator built with Dash that helps soap makers calculate lye requirements, water ratios, and oil properties for hot process and cold process soap making.

## Features

- Calculate lye requirements (NaOH, KOH, 90% KOH, or Dual Lye)
- Flexible oil selection with SAP value calculations
- Water calculation methods (by oil weight %, lye weight %, or water:lye ratio)
- Post-cook superfat oils support
- HTFHP additives configuration
- Recipe export/import as JSON
- Print-friendly recipe output
- Real-time recipe property analysis
- Input validation and error messages

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager) or conda

### Quick Start

```bash
git clone <repository-url>
cd soap-calc-python
```

### Option 1: Using venv and pip

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment (macOS/Linux)
source venv/bin/activate

# Activate environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using Conda

```bash
# Create and activate environment
conda create --name soap-calc python=3.10
conda activate soap-calc

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:8050`

## Usage

1. **Enter Recipe Name & Notes** - Add a title and optional notes for your recipe
2. **Select Recipe Parameters** - Choose units, lye type, lye discount, oil input method, and water calculation method
3. **Select Oils** - Choose your soap oils from the dropdown and enter amounts in grams or ounces
4. **Configure Additives** - Adjust HTFHP additives in the accordion section
5. **Add Other Ingredients** - Add any additional ingredients (fragrances, colorants, etc.)
6. **Generate Recipe** - Click "Generate Recipe" to calculate all values
7. **Export or Print** - Export as JSON or print the recipe

## Project Structure

```
soap-calc-python/
├── app.py                    # Main Dash application
├── recipe_calculator.py      # Core calculation functions
├── additives_data.py         # HTFHP additives configuration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── data/
│   ├── Oil_Properties.tsv    # Oil SAP values
│   └── Oil_fats.tsv          # Oil fatty acid composition
└── assets/
    ├── style.css             # Main stylesheet
    └── print.css             # Print stylesheet
```

## Technologies Used

- **Dash** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Dash Bootstrap Components** - UI components
- **Plotly** - Interactive visualizations

## Notes

- Recipes can be saved and loaded via JSON export/import
- All calculations are performed client-side
- Print functionality works in most modern browsers

## License

This project is for personal use.

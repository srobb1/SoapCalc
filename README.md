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
- pip (Python package manager) OR conda

### Option 1: Using pip and venv

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd soap-calc-python
```

#### 2. Create a Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Option 2: Using Conda

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd soap-calc-python
```

#### 2. Create and Activate Conda Environment

```bash
conda create --name soap-calc python=3.10
conda activate soap-calc
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:

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

## File Structure

- `app.py` - Main Dash application
- `recipe_calculator.py` - Core calculation functions
- `additives_data.py` - HTFHP additives configuration
- `data/` - Oil properties and SAP values data files
- `assets/` - CSS and JavaScript files

## Project Structure

```
soap-calc-python/
├── app.py
├── recipe_calculator.py
├── additives_data.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── Oil_Properties.tsv
│   └── Oil_fats.tsv
└── assets/
    ├── style.css
    └── print.css
```

## Technologies Used

- **Dash** - Web framework
- **Pandas** - Data manipulation
- **Bootstrap** - UI components
- **Plotly** - Interactive visualizations

## License

This project is for personal use.

## Notes

- Recipes can be saved and loaded via JSON export/import
- All calculations are performed client-side
- Print functionality works in most modern browsers

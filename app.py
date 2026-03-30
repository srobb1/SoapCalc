# Import packages
from dash import Dash, html, dash_table, dcc, Output, Input, State, callback_context, dash_table, no_update
import pandas as pd
import dash_ag_grid as dag
import json
import base64
import io
import dash_bootstrap_components as dbc
from pathlib import Path

# conda activate soap-calc


# Configuration - Data file paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
OIL_PROPERTIES_FILE = DATA_DIR / 'Oil_Properties.tsv'
OIL_FATS_FILE = DATA_DIR / 'Oil_fats.tsv'

# Load data
oil_prop_df = pd.read_csv(OIL_PROPERTIES_FILE, header=0, index_col=0, sep="\t")
oil_fat_df = pd.read_csv(OIL_FATS_FILE, header=0, index_col=0, sep="\t")

# Constants
saturated_fats = ("Lauric","Myristic","Palmitic","Stearic")
unsaturated_fats = ("Oleic","Linoleic","Linolenic","Ricinoleic")

dt_oil_columns = ['Oil', 'NaOH SAP', 'KOH SAP', 'Grams', 'Ounces', 'Percent']
pcsf=("Argan Oil","Apricot Kernal Oil", "Coconut Oil","Olive Oil","Sweet Almond Oil","Cocoa Butter","Shea Butter","Jojoba Oil","Aloe Butter","Mango Button", "Kokum Butter","Grapeseed Oil")

# Import additive data and calculator functions
from additives_data import htfhp_additive_rowData, htfhp_tooltips, section_colors, section_descriptions
from recipe_calculator import (
    validate_recipe_inputs, 
    calculate_lye_requirements,
    calculate_water_requirements,
    calculate_soap_properties,
    create_other_ingredients_table,
    create_additives_details,
    create_overview_table,
    create_oils_table,
    create_summary_table,
    create_properties_table,
    create_fats_table,
    calculate_other_ingredients,
    convert_to_number
)
from compliance_report import create_compliance_report

htfhp_tooltip_data = [
    {column: {'value': str(row[column]), 'type': 'text'} for column in row}
    for row in htfhp_tooltips
]

# Enhance tooltip data with section descriptions
for i, row in enumerate(htfhp_additive_rowData):
    section = row.get('section')
    if section in section_descriptions:
        # Add description to the section cell tooltip
        if i < len(htfhp_tooltip_data):
            htfhp_tooltip_data[i]['section']['value'] = f"{section}\n\n📌 WHY THIS MATTERS:\n{section_descriptions[section]}"

htfhp_additive_columns = [
    {"name": "Category", "id": "section"},
    {"name": "Additive", "id": "Additive"},
    {"name": "Value", "id": "Value", "editable": True}
]

# Create conditional styles based on section names
style_data_conditional = []
for section, color in section_colors.items():
    style_data_conditional.extend([
        {
            'if': {
                'filter_query': f'{{section}} = "{section}"'
            },
            'backgroundColor': color,
            'color': 'black'
        }
    ])

# Add visual styling for read-only cells (Add to oil list, See LyeType)
style_data_conditional.extend([
    {
        'if': {
            'filter_query': '{Value} contains "Add to oil list" || {Value} contains "See LyeType"'
        },
        'backgroundColor': '#e8e8e8',
        'color': '#555',
        'fontStyle': 'italic',
        'opacity': '0.8'
    }
])

# Convert the list of dictionaries to a DataFrame
additive_df = pd.DataFrame(htfhp_additive_rowData)

additive_table = dash_table.DataTable(
    id='additives-table',
    columns=htfhp_additive_columns,
    data=additive_df.to_dict('records'),
    tooltip_data=htfhp_tooltip_data,
    tooltip_delay=200,
    tooltip_duration=None,
    style_cell={
        'textAlign': 'left',
        'padding': '10px',
        'fontSize': '13px',
        'whiteSpace': 'normal'
    },
    style_table={ 'border': '1px solid black', 'borderCollapse': 'collapse', 'whiteSpace': 'normal' ,'overflowX': 'hidden'},
    style_header={
          'fontSize': '13px',
          'fontWeight': 'bold',
          'paddingLeft': '10px',
          'backgroundColor' : '#fafafa'
    },
    style_data_conditional=style_data_conditional,    
    style_cell_conditional=[
        {'if': {'column_id': 'section'}, 'width': '30%'},
        {'if': {'column_id': 'Additive'}, 'width': '40%'},
        {'if': {'column_id': 'Value'}, 'width': '30%'},
    ]
)

other_ingredient_columns = [
    {"name": "Ingredient", "id": "Ingredient","editable": True},
    {"name": "Type", "id": "Type", "editable": False},
    {"name": "Amount", "id": "Amount","editable": True},
    {"name": "Unit", "id": "Unit","editable": True},
    {"name": "Notes", "id": "Notes", "editable": True}
]

# Columns for the generated recipe table (includes Calculated column)
other_ingredient_recipe_columns = [
    {"name": "Ingredient", "id": "Ingredient"},
    {"name": "Type", "id": "Type"},
    {"name": "Amount", "id": "Amount"},
    {"name": "Unit", "id": "Unit"},
    {"name": "Calculated", "id": "CalculatedAmount"},
    {"name": "Notes", "id": "Notes"}
]

other_ingredient_initial_rows = [
    {"Ingredient": "", "Type": "Fixed", "Amount": "", "Unit": "", "Notes": ""},
    {"Ingredient": "", "Type": "%TOW", "Amount": "", "Unit": "%", "Notes": ""},
]

# Initialize the app
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'],
           suppress_callback_exceptions=True,
           title="Sofia's Soap Calculator")

# Add custom CSS for prettier tooltips
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .dash-table-tooltip {
                background-color: #2c3e50 !important;
                color: #ecf0f1 !important;
                border: 2px solid #3498db !important;
                border-radius: 8px !important;
                padding: 12px 16px !important;
                font-size: 13px !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
                max-width: 300px !important;
                line-height: 1.6 !important;
                white-space: pre-wrap !important;
                word-wrap: break-word !important;
                z-index: 9999 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([html.Div([html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Span('🧼', style={'fontSize': '32px', 'marginRight': '15px'}),
                html.H1("Sofia's Soap Calculator", style={'textAlign': 'left', 'color': '#1f77b4', 'marginBottom': '0px', 'display': 'inline-block', 'fontWeight': '600', 'letterSpacing': '0.5px'})
            ], style={'display': 'flex', 'alignItems': 'center', 'paddingLeft': '10px', 'paddingTop': '15px', 'paddingBottom': '15px'}),
            width=5
        ),
        dbc.Col([
            dcc.Upload(
                id='upload-recipe-json',
                children=dbc.Button('Upload Recipe (JSON)', color='primary', outline=False, size='sm'),
                multiple=False
            ),
            html.Div(id='upload-recipe-json-output'),
        ], width=2, style={'textAlign': 'right', 'paddingRight': '10px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-end'})
    ]),
    dbc.Row([
        dbc.Col([
            html.P('📖 Based on "The Ultimate Guide to Hot Process Soap" by Ashley Green', 
                   style={'fontSize': '13px', 'color': '#666', 'marginBottom': '10px', 'paddingLeft': '10px', 'fontStyle': 'italic'})
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Accordion([
                    dbc.AccordionItem(
                        html.Div([
                                            dbc.Row(
                                dbc.Col([
                                ])
                            ),
                            dbc.Row(
                                dbc.Col([
                                    #html.Label(html.Strong('Recipe Name:'), style={'marginBottom': '8px'}),
                                     dcc.Input(
                                         id='recipe-name',
                                         placeholder='Enter recipe name',
                                         type='text',
                                         value='',
                                         style={'width': '100%', 'height': '35px', 'padding': '5px', 'border': '1px solid #ccc', 'borderRadius':
   '0.25rem'},
                                         required=True
                                     ),
                                 ], width=9),
                                 style={'marginBottom': '15px'}
                             ),
                             dbc.Row(
                                 dbc.Col([
                                     #html.Label(html.Strong('Recipe Notes:'), style={'marginBottom': '8px'}),
                                     dcc.Textarea(
                                         id='recipe-notes',
                                         placeholder='Enter recipe notes',
                                         value='',
                                         style={
                                             'width': '100%',
                                             'height': '100px',
                                             'resize': 'vertical',
                                             'padding': '8px',
                                             'border': '1px solid #ccc',
                                             'borderRadius': '0.25rem',
                                             'fontFamily': 'inherit',
                                             'whiteSpace': 'pre-wrap'
                                         }
                                     ),
                                 ], width=9)
                             ),
                         ], style={'width': '100%', 'paddingLeft': '10px'}),
                         title=html.Strong("Recipe Information"),
                         item_id="recipe-info-accordion"
                     )
                 ], active_item="recipe-info-accordion", style={'marginBottom': '20px'})
             ], width=7),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            dbc.Accordion([
                 dbc.AccordionItem(
                     html.Div([
                         dbc.Row([
                             dbc.Col([
                                 html.Div([
                                     html.Label([
                                         html.Span(html.Strong('Units:'), id='Units-tooltip'),
                                         dcc.RadioItems(
                                             options=[
                                                 {'label': 'Grams', 'value': 'Grams'},
                                                 {'label': 'Ounces', 'value': 'Ounces'}
                                             ],
                                             value='Grams',
                                             id='unit',
                                             labelStyle={'display': 'flex'},
                                             style={'paddingLeft': '10px'}
                                         )
                                     ]),
                                     dbc.Tooltip(
                                         "Enter the units you want to use to input weights into the Selected Oil table.",
                                         target="Units-tooltip"
                                     ),
                                 ]),
                                 html.Div([
                                     html.Label([
                                         html.Strong('Lye:'),
                                         dcc.RadioItems(
                                             options=[
                                                 {'label': html.Span('NaOH', id='NaOH-tooltip'), 'value': 'NaOH'},
                                                 {'label': html.Span('KOH', id='KOH-tooltip'), 'value': 'KOH'},
                                                 {'label': html.Span('90% KOH', id='KOH_90-tooltip'), 'value': 'KOH_90'},
                                                 {'label': html.Span('Dual Lye', id='dual_lye-tooltip'), 'value': 'dual_lye'}
                                             ],
                                             value='NaOH',
                                             id='lye_type',
                                             labelStyle={'display': 'flex'},
                                             style={'paddingLeft': '10px'}
                                         )
                                     ]),
                                     dbc.Tooltip(
                                         "Sodium Hydroxide is used in cold and hot process soap making.",
                                         target="NaOH-tooltip"
                                     ),
                                     dbc.Tooltip(
                                         "Potassium Hydroxide is used to make liquid soap.",
                                         target="KOH-tooltip"
                                     ),
                                     dbc.Tooltip(
                                         "90% pure Potassium Hydroxide, is used to make liquid soap.",
                                         target="KOH_90-tooltip"
                                     ),
                                     dbc.Tooltip(
                                         "95% NaOH and 5% KO is used to increase the lather in bar soaps.",
                                         target="dual_lye-tooltip"
                                     ),
                                 ])
                             ], width=2),
                             dbc.Col([
                                 html.Div([
                                     html.Label(html.Strong('Lye Discount (Cook Superfat):'), id='Discount-tooltip'),
                                     dcc.Input(id='lye_discount', type='number', value='5', style={'width': '45px', 'height': '20px', 'marginLeft':
   '5px'}),
                                     html.Label('%'),
                                     dbc.Tooltip(
                                         "A typical value is between 3 and 15. This is the percentage of lye you want reduced to allow for this percentage of un-saponified oils to remain",
                                         target="Discount-tooltip"
                                     ),
                                 ]),
                                 html.Br(),
                                 html.Div([
                                     html.Label([
                                         html.Span(html.Strong('Oils Entered by:'), id='Method-tooltip'),
                                         dcc.RadioItems(
                                             options=[
                                                 {'label': 'Weight', 'value': 'By_Weight'},
                                                 {'label': 'Percentage', 'value': 'By_Percent'}
                                             ],
                                             value='By_Weight',
                                             id='method_calculation'
                                         ),
                                         dcc.Input(
                                             id='total_weight',
                                             type='number',
                                             placeholder='Enter total weight (g or oz)',
                                             style={'display': 'none'}
                                         ),
                                     ]),
                                     dbc.Tooltip(
                                         "Do you want to enter exact Oil weights or do you want to use a percentage of a total oil weight?",
                                         target="Method-tooltip"
                                     ),
                                 ])
                             ], width=3),
                             dbc.Col(
                                 html.Div([
                                     html.Label(html.Strong('Calculate Water As:')),
                                     html.Div(
                                         [
                                             dcc.RadioItems(
                                                 id='water_calculation',
                                                 options=[
                                                     {
                                                         'label': html.Div(
                                                             [
                                                                 html.Label(
                                                                     [
                                                                         '% of Oil Weight: ',
                                                                         dcc.Input(
                                                                             id='water_by_oil_input',
                                                                             type='number',
                                                                             value='38',
                                                                             style={'width': '45px', 'height': '20px', 'marginLeft': '15px'}
                                                                         )
                                                                     ],
                                                                     style={'display': 'flex', 'alignItems': 'center'}
                                                                 ),
                                                                 html.Label('%'),
                                                             ],
                                                             style={'display': 'inline-flex', 'alignItems': 'center'}
                                                         ),
                                                         'value': 'water_by_oil'
                                                     },
                                                     {
                                                         'label': html.Div(
                                                             [
                                                                 html.Label(
                                                                     [
                                                                         '% of Lye Weight:',
                                                                         dcc.Input(
                                                                             id='water_by_lye_input',
                                                                             type='number',
                                                                             value='33',
                                                                             style={'width': '45px', 'height': '20px', 'marginLeft': '12px'}
                                                                         )
                                                                     ],
                                                                     style={'display': 'flex', 'alignItems': 'center'}
                                                                 ),
                                                                 html.Label('%'),
                                                             ],
                                                             style={'display': 'inline-flex', 'alignItems': 'center'}
                                                         ),
                                                         'value': 'water_by_lye'
                                                     },
                                                     {
                                                         'label': html.Div(
                                                             [
                                                                 html.Label(
                                                                     [
                                                                         'Water : Lye Ratio:',
                                                                         dcc.Input(
                                                                             id='water_lye_ratio_input',
                                                                             type='text',
                                                                             value='2:1',
                                                                             style={'width': '45px', 'height': '20px', 'marginLeft': '8px'}
                                                                         )
                                                                     ],
                                                                     style={'display': 'flex', 'alignItems': 'center'}
                                                                 ),
                                                             ],
                                                             style={'display': 'inline-flex', 'alignItems': 'center'}
                                                         ),
                                                         'value': 'water_lye_ratio'
                                                     },
                                                 ],
                                                 value='water_by_oil',
                                                 labelStyle={'display': 'block', 'marginRight': '10px'}
                                             ),
                                         ]
                                     )
                                 ]), width=4
                             ),
                         ]),
                     ], style={"width": "100%"}),
                     title=html.Strong("Select Your Recipe Parameters"),
                     item_id="recipe-params-accordion"
                 )
             ], active_item="recipe-params-accordion", style={'marginBottom': '20px'})
         ], width=7),
     ]),




     dbc.Row([
          dbc.Col([
              html.Br(),
              dbc.Accordion([
                  dbc.AccordionItem(
                      html.Div([
                          dbc.Row(
                              [
                                  dbc.Col(
                                      html.Div([
                                          dcc.Store(id='stored-selected-oils', storage_type='local'),
                                          #html.Label('Select your recipe oils:'),
                                          dcc.Dropdown(id='selected-oils', multi=True, style={'width': '100%'})
                                      ])
                                  ),
                                  dbc.Col(
                                      dbc.Button('Browse Oil Properties', id='oil-properties-btn', color='info', outline=True, size='sm'),
                                      width='auto',
                                      style={'paddingLeft': '10px'}
                                  )
                              ]
                          ),html.Br(),
                          html.Div(id='select-oils-output-container'),
                          html.Div([
                              dash_table.DataTable(
                                  id='selected-oils-data',
                                  columns=[{'name': col, 'id': col, 'editable': True} for col in dt_oil_columns],
                                  data=[],
                                  editable=True,
                                  row_deletable=True,
                                  style_header={
                                      'fontSize': '13px',
                                      'fontWeight': 'bold',
                                      'paddingLeft': '10px',
                                  },
                                  style_cell={
                                      'text-align': 'left',
                                      'paddingLeft': '10px',
                                      'fontSize': '13px',
                                  },
                              ),
                          ],
                          ),
                          html.Div(id='selected-oils-updated'),
                          html.Div(id='oils-totals', style={'paddingLeft': '10px', 'marginTop': '10px', 'fontWeight': 'bold'}),
                      ], style={"width": "100%"}),
                      title=html.Strong("Select Your Recipe Oils"),
                      item_id="recipe-oils-accordion"
                  )
              ], active_item="recipe-oils-accordion", style={'marginBottom': '20px'})
          ], width=7),
      ]),

     dbc.Modal([
         dbc.ModalHeader(dbc.ModalTitle("Oil Properties Browser")),
         dbc.ModalBody([
             dbc.Row([
                 dbc.Col([
                     html.Label(html.Strong('Compare Oils:'), style={'marginBottom': '8px'}),
                     dcc.Dropdown(
                         id='oil-properties-compare-oils',
                         multi=True,
                         placeholder='Select oils to compare...',
                         style={'width': '100%'}
                     )
                 ], width=12)
             ]),
             html.Br(),
             html.Div(id='oil-properties-compare-results'),
             html.Br(),
             html.Label(html.Strong('Or filter by properties:'), style={'marginBottom': '8px'}),


             html.Div([
                 dbc.Row([
                     dbc.Col([
                         html.Label(html.Strong('Hardness:'), style={'marginBottom': '8px'}),
                         dcc.RangeSlider(
                             id='hardness-filter',
                             min=0,
                             max=int(oil_prop_df['Hardness'].max()),
                             step=1,
                             value=[0, int(oil_prop_df['Hardness'].max())],
                             marks={i: str(i) for i in range(0, int(oil_prop_df['Hardness'].max()) + 1, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=4),
                     dbc.Col([
                         html.Label(html.Strong('Cleansing:'), style={'marginBottom': '8px'}),
                         dcc.RangeSlider(
                             id='cleansing-filter',
                             min=0,
                             max=int(oil_prop_df['Cleansing'].max()),
                             step=1,
                             value=[0, int(oil_prop_df['Cleansing'].max())],
                             marks={i: str(i) for i in range(0, int(oil_prop_df['Cleansing'].max()) + 1, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=4),
                     dbc.Col([
                         html.Label(html.Strong('Condition:'), style={'marginBottom': '8px'}),
                         dcc.RangeSlider(
                             id='condition-filter',
                             min=0,
                             max=int(oil_prop_df['Condition'].max()),
                             step=1,
                             value=[0, int(oil_prop_df['Condition'].max())],
                             marks={i: str(i) for i in range(0, int(oil_prop_df['Condition'].max()) + 1, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=4),
                 ]),
                 html.Br(),
                 dbc.Row([
                     dbc.Col([
                         html.Label(html.Strong('Bubbly:'), style={'marginBottom': '8px'}),
                         dcc.RangeSlider(
                             id='bubbly-filter',
                             min=0,
                             max=int(oil_prop_df['Bubbly'].max()),
                             step=1,
                             value=[0, int(oil_prop_df['Bubbly'].max())],
                             marks={i: str(i) for i in range(0, int(oil_prop_df['Bubbly'].max()) + 1, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=4),
                     dbc.Col([
                         html.Label(html.Strong('Creamy:'), style={'marginBottom': '8px'}),
                         dcc.RangeSlider(
                             id='creamy-filter',
                             min=0,
                             max=int(oil_prop_df['Creamy'].max()),
                             step=1,
                             value=[0, int(oil_prop_df['Creamy'].max())],
                             marks={i: str(i) for i in range(0, int(oil_prop_df['Creamy'].max()) + 1, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=4),
                 ]),
                 html.Br(),
                 html.Label(html.Strong('Fat Types:'), style={'marginBottom': '8px'}),
                 dbc.Row([
                     dbc.Col([
                         html.Label('Lauric:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='lauric-filter',
                             min=0,
                             max=50,
                             step=1,
                             value=[0, 50],
                             marks={i: '' for i in range(0, 51, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                     dbc.Col([
                         html.Label('Myristic:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='myristic-filter',
                             min=0,
                             max=30,
                             step=1,
                             value=[0, 30],
                             marks={i: '' for i in range(0, 31, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                     dbc.Col([
                         html.Label('Palmitic:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='palmitic-filter',
                             min=0,
                             max=50,
                             step=1,
                             value=[0, 50],
                             marks={i: '' for i in range(0, 51, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                     dbc.Col([
                         html.Label('Stearic:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='stearic-filter',
                             min=0,
                             max=50,
                             step=1,
                             value=[0, 50],
                             marks={i: '' for i in range(0, 51, 10)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                     dbc.Col([
                         html.Label('Oleic:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='oleic-filter',
                             min=0,
                             max=90,
                             step=1,
                             value=[0, 90],
                             marks={i: '' for i in range(0, 91, 15)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                     dbc.Col([
                         html.Label('Linoleic:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='linoleic-filter',
                             min=0,
                             max=80,
                             step=1,
                             value=[0, 80],
                             marks={i: '' for i in range(0, 81, 15)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                 ]),
                 dbc.Row([
                     dbc.Col([
                         html.Label('Linolenic:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='linolenic-filter',
                             min=0,
                             max=80,
                             step=1,
                             value=[0, 80],
                             marks={i: '' for i in range(0, 81, 15)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                     dbc.Col([
                         html.Label('Ricinoleic:', style={'fontSize': '12px'}),
                         dcc.RangeSlider(
                             id='ricinoleic-filter',
                             min=0,
                             max=90,
                             step=1,
                             value=[0, 90],
                             marks={i: '' for i in range(0, 91, 15)},
                             tooltip={"placement": "bottom", "always_visible": True}
                         )
                     ], width=2),
                 ]),
                 html.Br(),
                 dbc.Button('Search', id='search-oils-btn', color='primary', className='me-2'),
                 html.Br(),
                 html.Br(),
                 html.Div(id='oil-search-results')
             ])
         ]),
         dbc.ModalFooter([
             dbc.Button("Close", id="close-oil-modal", className="ms-auto", color='secondary')
         ]),
     ],
     id="oil-properties-modal",
     size="xl",
     is_open=False,
     ),

    dbc.Row([
         dbc.Col([
             html.Br(),
             dbc.Accordion([
                 dbc.AccordionItem(
                     html.Div([
                         dbc.Row(
                             [
                                 dbc.Col(
                                     html.Div([
                                         dcc.Store(id='stored-pcsf-selected-oils', storage_type='local'),
                                         dcc.Dropdown(id='pcsf-selected-oils', multi=True)
                                     ])
                                 ),
                             ]
                         ),html.Br(),
                         html.Div(id='select-oils-pcsf-output-container'),
                         dash_table.DataTable(
                             id='pcsf-selected-oils-data',
                             columns=[
                                 {'name': 'PCSF Oil', 'id': 'PCSF Oil'},
                                 {'name': '%TOW', 'id': '%TOW', 'editable': True},
                                 {'name': 'Grams', 'id': 'Grams', 'editable': False},
                                 {'name': 'Ounces', 'id': 'Ounces', 'editable': False}
                             ],
                             data=[],
                             editable=True,
                             row_deletable=True,
                             style_header={
                                 'fontSize': '13px',
                                 'fontWeight': 'bold',
                                 'paddingLeft': '10px',
                             },
                             style_cell={
                                 'text-align': 'left',
                                 'paddingLeft': '10px',
                                 'fontSize': '13px',
                             },
                             style_data_conditional=[
                                 {
                                     'if': {
                                         'column_id': '%TOW'
                                     },
                                     'backgroundColor': 'lightgreen',
                                     'color': 'black'
                                 }
                             ],
                         ),
                         html.Div(id='pcsf-selected-oils-updated'),
                     ], style={"width": "100%", 'paddingLeft': '10px'}),
                     title=html.Strong("Post Cook Superfat (PCSF) Oils"),
                     item_id="pcsf-accordion"
                 )
             ], active_item="pcsf-accordion", style={'marginBottom': '20px'})
         ], width=7),
     ]),

    dbc.Row([
        dbc.Col([
            html.Br(),
            dbc.Accordion([
                dbc.AccordionItem(
                    additive_table,
                    title=html.Strong("HTFHP Additives"),
                    item_id="additives-accordion"
                )
            ], active_item="additives-accordion", style={'marginBottom': '20px'})
        ], width=7),
    ]),


    dbc.Row([
         dbc.Col([
             html.Br(),
             dbc.Accordion([
                 dbc.AccordionItem(
                     html.Div([
                         html.Br(),
                         dash_table.DataTable(
                             id='other-ingredients-table',
                             columns=other_ingredient_columns,
                             data=other_ingredient_initial_rows,
                             editable=True,
                             row_deletable=True,
                             style_cell={
                                 'textAlign': 'left',
                                 'padding': '10px',
                                 'fontSize': '13px',
                             },
                             style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
                             style_header={
                                 'fontSize': '13px',
                                 'fontWeight': 'bold',
                                 'paddingLeft': '10px',
                                 'backgroundColor': '#fafafa'
                             },
                         ),
                         html.Div([
                             dbc.Button("Add Fixed Amount", id="add-row-button", color="primary", style={'marginRight': '10px'}),
                             dbc.Button("Add % of Total Weight", id="add-row-percentage-button", color="info")
                         ],
                             style={'display': 'flex', 'justifyContent': 'flex-end', 'marginTop': '20px'}
                         ),
                     ]),
                     title=html.Strong("Other Ingredients"),
                     item_id="other-ingredients-accordion"
                 )
             ], active_item="other-ingredients-accordion", style={'marginBottom': '20px'})
         ], width=7),
     ]),

    dbc.Row([
        dbc.Col([
            html.Div(id='error-message', style={'color': 'red'}),
            
        ],width=4)
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Button('Generate Recipe/Update Values', id='get-recipe', n_clicks=0, size='lg', style={'backgroundColor':'orange', 'color':'black'}),
            width='auto'
        ),
        dbc.Col(
            dbc.Button('Export Recipe (JSON)', id='export-recipe', n_clicks=0, color='primary', size='lg'),
            width='auto'
        ),
        dbc.Col(
            dbc.Button('Print Recipe', id='print-button', n_clicks=0, color='success', size='lg'),
            width='auto',
            id='print-button-container',
            style={'display': 'none'}
        )
    ]),

    ],className='no-print'),
    html.Div([
        dbc.Row(
            dbc.Col(
                html.Div(id='results'),
                width=8
            )
        ),
    ],className='print-content',style={'width': '100%'}),
    html.Div([
        dcc.Download(id='download-recipe'),  # Add this component
        html.Div(id='export-recipe-json-output')  # Output for export feedback
    ],className='no-print',style={'width': '100%'}),
], style={'paddingLeft': '20px','width': '100%'}
)

@app.callback(
    Output('other-ingredients-table', 'data'),
    [Input('add-row-button', 'n_clicks'),
     Input('add-row-percentage-button', 'n_clicks'),
     Input('upload-recipe-json', 'contents')],
    [State('upload-recipe-json', 'filename'),
     State('other-ingredients-table', 'data')],
    prevent_initial_call=True
)
def update_other_ingredients_table(n_clicks_fixed, n_clicks_percent, contents, filename, data):
    """
    Update other ingredients table when adding rows or uploading recipe
    
    Handles three actions:
    - Add Fixed Amount button: Appends fixed type row
    - Add % of Total Weight button: Appends percentage type row
    - Upload: Loads ingredients from JSON file
    """
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'upload-recipe-json' and contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                recipe = json.loads(decoded)
                new_data = recipe.get('other-ingredients-table', [])
                # Filter out empty rows
                new_data = [row for row in new_data if any(row.values())]
                return new_data
        except Exception as e:
            return no_update
    elif trigger_id == 'add-row-button' and n_clicks_fixed:
        data.append({"Ingredient": "", "Type": "Fixed", "Amount": "", "Unit": "", "CalculatedAmount": "", "Notes": ""})
        return data
    elif trigger_id == 'add-row-percentage-button' and n_clicks_percent:
        data.append({"Ingredient": "", "Type": "%TOW", "Amount": "", "Unit": "%", "CalculatedAmount": "", "Notes": ""})
        return data
    else:
        return no_update




@app.callback(
    Output('other-ingredients-table', 'data', allow_duplicate=True),
    Input('other-ingredients-table', 'data'),
    prevent_initial_call=True
)
def update_calculated_amounts(table_data):
    """Update calculated amounts in the table as user types"""
    if not table_data:
        return table_data
    
    # For display in the input table, use a default total weight of 1000g for preview
    # Real calculation happens during recipe generation
    default_total_weight = 1000
    
    updated_data = []
    data_changed = False
    
    for row in table_data:
        row_copy = row.copy()
        old_calc = row.get('CalculatedAmount', '')
        
        if not row.get('Ingredient'):
            # Keep empty rows as-is
            updated_data.append(row_copy)
            continue
        
        if row_copy.get('Type') == '%TOW':
            # Calculate preview amount as percentage
            amount_value = convert_to_number(row_copy.get('Amount', 0))
            if amount_value > 0:
                calculated = amount_value * (default_total_weight / 100)
                new_calc = f"{round(calculated, 2)} g"
                if old_calc != new_calc:
                    row_copy['CalculatedAmount'] = new_calc
                    data_changed = True
            else:
                if old_calc != "":
                    row_copy['CalculatedAmount'] = ""
                    data_changed = True
        else:
            # Fixed amount - show as entered
            amount = row_copy.get('Amount', '')
            unit = row_copy.get('Unit', '')
            if amount:
                new_calc = f"{amount} {unit}".strip()
                if old_calc != new_calc:
                    row_copy['CalculatedAmount'] = new_calc
                    data_changed = True
            else:
                if old_calc != "":
                    row_copy['CalculatedAmount'] = ""
                    data_changed = True
        
        updated_data.append(row_copy)
    
    # Only return updated data if something actually changed
    # This prevents unnecessary updates that interrupt editing
    return updated_data if data_changed else no_update

def _update_dropdown_state(selected_items, stored_items, all_options):
    """
    Helper function to update dropdown state and maintain selection
    
    Args:
        selected_items: Currently selected values
        stored_items: Previously stored values
        all_options: List of all available options
    
    Returns:
        tuple: (all_options, updated_selected_items)
    """
    if selected_items is None:
        selected_items = []
    if stored_items is None:
        stored_items = []
    
    updated_selected = list(set(stored_items + selected_items))
    return all_options, updated_selected

# Callback to update the pcsf dropdown options based on the data in the dropdown and selected oils
@app.callback(
  Output('pcsf-selected-oils', 'options'),
  Output('stored-pcsf-selected-oils', 'data'),
  Input('pcsf-selected-oils', 'value'),
  State('stored-pcsf-selected-oils', 'data')
)
def update_pcsf_dropdown(selected_oils, stored_selected_oils):
  """Update PCSF (Post Cook Superfat) dropdown options and maintain selection state"""
  all_options = [{'label': i, 'value': i} for i in pcsf]
  return _update_dropdown_state(selected_oils, stored_selected_oils, all_options)


# Callback to initialize and update the DataTable
@app.callback(
  [Output('pcsf-selected-oils-data', 'data'),
   Output('pcsf-selected-oils-data', 'columns'),
   Output('pcsf-selected-oils', 'value')],
  [Input('pcsf-selected-oils', 'value'),
   Input('pcsf-selected-oils-data', 'data_timestamp'),
   Input('upload-recipe-json', 'contents'),
   Input('selected-oils-data', 'data')],
  [State('upload-recipe-json', 'filename'),
   State('pcsf-selected-oils-data', 'data'),
   State('stored-pcsf-selected-oils', 'data')]
)
def update_pcsf_table(selected_oils, timestamp, contents, oils_data, filename, data, stored_selected_oils):
      """
      Update PCSF oils data table
      
      Handles dropdown selection changes and recipe uploads.
      Preserves existing %TOW values when oils are reselected.
      """
      ctx = callback_context
      trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

      if trigger_id == 'upload-recipe-json' and contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                recipe = json.loads(decoded)
                new_data = recipe.get('pcsf-selected-oils-data', [])
                return new_data, [{'name': 'PCSF Oil', 'id': 'PCSF Oil'}, {'name': '%TOW', 'id': '%TOW', 'editable': True}, {'name': 'Grams', 'id': 'Grams', 'editable': False}, {'name': 'Ounces', 'id': 'Ounces', 'editable': False}], [oil['PCSF Oil'] for oil in new_data]
        except Exception as e:
            return (no_update,no_update,no_update)

      if selected_oils is None:
          selected_oils = []
      if stored_selected_oils is None:
        stored_selected_oils = []

      # Create a dictionary of current data for easy lookup
      current_data = {row['PCSF Oil']: row for row in data} if data else {}

      new_data = []
      for oil in selected_oils:
          if oil in current_data:
              new_data.append(current_data[oil])
          else:
              new_data.append({
                  'PCSF Oil': oil,
                  '%TOW': 0,
              })


      # Calculate grams and ounces for PCSF oils
      if oils_data:
          total_oil_weight = sum(convert_to_number(row.get('Grams', 0)) for row in oils_data)
          for row in new_data:
              tow_value = convert_to_number(row.get('%TOW', 0))
              if tow_value > 0 and total_oil_weight > 0:
                  grams = tow_value * (total_oil_weight / 100)
                  ounces = grams / 28.3495
                  row['Grams'] = round(grams, 2)
                  row['Ounces'] = round(ounces, 2)
              else:
                  row['Grams'] = ""
                  row['Ounces'] = ""

      return new_data, [
        {'name': 'PCSF Oil', 'id': 'PCSF Oil'},
        {'name': '%TOW', 'id': '%TOW', 'editable': True},
        {'name': 'Grams', 'id': 'Grams', 'editable': False},
        {'name': 'Ounces', 'id': 'Ounces', 'editable': False}
      ], selected_oils


# Callback to show/hide total weight input based on method calculation
@app.callback(
  Output('total_weight', 'style'),
  Input('method_calculation', 'value')
)


def show_hide_total_weight_input(method):
  """Show/hide total weight input field based on calculation method"""
  if method == 'By_Percent':
      return {'display': 'block'}
  else:
      return {'display': 'none'}

# Callback to update the dropdown options based on the data in the dropdown and selected oils
@app.callback(
  Output('selected-oils', 'options'),
  Output('stored-selected-oils', 'data'),
  Input('selected-oils', 'value'),
  State('stored-selected-oils', 'data')
)
def update_dropdown(selected_oils, stored_selected_oils):
  """Update recipe oils dropdown options and maintain selection state"""
  all_options = [{'label': oil, 'value': oil} for oil in oil_prop_df.index.tolist()]
  return _update_dropdown_state(selected_oils, stored_selected_oils, all_options)


@app.callback(
    [Output('selected-oils-data', 'data'),
     Output('selected-oils-data', 'columns'),
     Output('selected-oils-data', 'style_data_conditional'),
     Output('error-message', 'children'),
     Output('selected-oils', 'value'),
     Output('recipe-name', 'value'),
     Output('recipe-notes', 'value'),
     Output('unit', 'value'),
     Output('lye_type', 'value'),
     Output('lye_discount', 'value'),
     Output('method_calculation', 'value'),
     Output('total_weight', 'value'),
     Output('water_calculation', 'value'),
     Output('water_by_oil_input', 'value'),
     Output('water_by_lye_input', 'value'),
     Output('water_lye_ratio_input', 'value'),
    ],
    [Input('selected-oils', 'value'),
     Input('lye_type', 'value'),
     Input('unit', 'value'),
     Input('method_calculation', 'value'),
     Input('selected-oils-data', 'data_timestamp'),
     Input('upload-recipe-json', 'contents')],
    [State('upload-recipe-json', 'filename'),
     State('selected-oils-data', 'data'),
     State('total_weight', 'value'),
     State('stored-selected-oils', 'data')]
)
def update_table(selected_oils, lye_type, unit, method, timestamp, contents, filename, data, total_weight, stored_selected_oils):
    """
    Main callback for selected oils table
    
    Handles:
    - Oil selection from dropdown
    - Unit changes (Grams/Ounces)
    - Method changes (By Weight/By Percent)
    - Data edits with automatic recalculation
    - Recipe JSON uploads
    
    Returns updated table data, columns, styling, and all recipe parameters
    """
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    editable_cols = []
    error_message = []

    if method == 'By_Weight':
        if unit == 'Grams':
            editable_cols = ['Grams']
        else:
            editable_cols = ['Ounces']
    else:
        editable_cols = ['Percent']

    style_data_conditional = [
        {
            'if': {'column_id': col},
            'backgroundColor': 'PaleGreen'
        } for col in editable_cols
    ]

    if trigger_id == 'upload-recipe-json' and contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                recipe = json.loads(decoded)
                new_data = recipe.get('selected_oils', [])
                recipe_name = recipe.get('recipe_name', '') or ''
                recipe_notes = recipe.get('recipe_notes', '') or ''
                unit = recipe.get('unit', '')
                lye_type = recipe.get('lye_type', '')
                lye_discount = recipe.get('lye_discount', '')
                method_calculation = recipe.get('method_calculation', '')
                total_weight = recipe.get('total_weight', '')
                water_calculation = recipe.get('water_calculation', '')
                water_by_oil_input = recipe.get('water_by_oil_input', '')
                water_by_lye_input = recipe.get('water_by_lye_input', '')
                water_lye_ratio_input = recipe.get('water_lye_ratio_input', '')

                return (new_data,
                        [{'name': col, 'id': col, 'editable': (col in editable_cols)} for col in dt_oil_columns],
                        style_data_conditional,
                        'Recipe uploaded successfully!',
                        [oil['Oil'] for oil in new_data],
                        recipe_name,
                        recipe_notes,
                        unit,
                        lye_type,
                        lye_discount, #10
                        method_calculation, # 11
                        total_weight,
                        water_calculation,
                        water_by_oil_input,
                        water_by_lye_input,
                        water_lye_ratio_input, #16
                      )
        except Exception as e:
            return (no_update, no_update, no_update,  #3
                    f'There was an error uploading the recipe: {str(e)}',  #4
                    no_update, no_update, no_update, #7
                    no_update, no_update, no_update, #10
                    no_update, no_update, no_update, #13
                    no_update, no_update, no_update) #16

    if trigger_id in ['selected-oils', 'unit', 'method_calculation']:
        if selected_oils is None:
            selected_oils = []

        current_data = {row['Oil']: row for row in data}
        new_data = []
        for oil in selected_oils:
            if oil in current_data:
                new_data.append(current_data[oil])
            else:
                new_data.append({
                    'Oil': oil,
                    'NaOH SAP': oil_prop_df.loc[oil, 'SAP_Value'],
                    'KOH SAP': oil_prop_df.loc[oil, 'SAP_KOH'],
                    'Grams': 0,
                    'Ounces': 0,
                    'Percent': 0
                })

        error_list = html.Ul([html.Li(x) for x in error_message])
        return (new_data,
                [{'name': col, 'id': col, 'editable': (col in editable_cols)} for col in dt_oil_columns],
                style_data_conditional,
                error_list,
                selected_oils, no_update, no_update,
                no_update, no_update, no_update,
                no_update, no_update, no_update,
                    no_update, no_update, no_update) #16

    if trigger_id == 'selected-oils-data' and data is not None:
        if method == 'By_Weight':
            total_weight = 0
            for row in data:
                if unit == 'Grams':
                    weight = float(row.get('Grams', 0))
                else:
                    weight = float(row.get('Ounces', 0)) * 28.3495
                total_weight += weight

            for row in data:
                if unit == 'Grams':
                    weight = float(row.get('Grams', 0))
                else:
                    weight = float(row.get('Ounces', 0)) * 28.3495
                row['Percent'] = round((weight / total_weight) * 100, 1) if total_weight > 0 else 0
                if unit == 'Grams':
                    row['Ounces'] = round(weight / 28.3495, 2)
                else:
                    row['Grams'] = round(weight, 1)

        else:
            total_percent = 0
            if total_weight is None or total_weight <= 0:
                error_message.append('Please enter a valid total weight for percentage calculations.')
            else:
                for row in data:
                    percent = float(row.get('Percent', 0))
                    total_percent += percent
                    if unit == 'Grams':
                        row['Grams'] = round((percent / 100) * total_weight, 1)
                        row['Ounces'] = round(row['Grams'] / 28.3495, 2)
                    else:
                        row['Ounces'] = round((percent / 100) * total_weight, 2)
                        row['Grams'] = round(row['Ounces'] * 28.3495, 1)
            if total_percent != 100:
                if total_percent < 100:
                    difference = 100 - total_percent
                    error_message.append(f'Please make sure your percentages add up to 100%. {total_percent}% is less than 100 by {difference}')
                else:
                    difference = total_percent - 100
                    error_message.append(f'Please make sure your percentages add up to 100%. {total_percent}% is more than 100 by {difference}')

        # Format Ounces to 2 decimals
        for row in data:
            if 'Ounces' in row:
                row['Ounces'] = round(float(row.get('Ounces', 0)), 2)
        
        error_list = html.Ul([html.Li(x) for x in error_message])
        return (data,
                [{'name': col, 'id': col, 'editable': (col in editable_cols)} for col in dt_oil_columns],
                style_data_conditional,
                error_list,
                selected_oils, no_update,no_update,
                no_update, no_update, no_update,
                no_update, no_update, no_update,
                no_update, no_update, no_update)

    if trigger_id == 'selected-oils-data':
        if selected_oils is not None:
            oils_in_data = [row['Oil'] for row in data]
            updated_selected_oils = [oil for oil in selected_oils if oil in oils_in_data]
            error_list = html.Ul([html.Li(x) for x in error_message])
            return (data,
                    [{'name': col, 'id': col, 'editable': (col in editable_cols)} for col in dt_oil_columns],
                    style_data_conditional,
                    error_list,
                    updated_selected_oils, no_update, no_update,
                    no_update, no_update, no_update,
                    no_update, no_update, no_update,
                    no_update, no_update, no_update)

    error_list = html.Ul([html.Li(x) for x in error_message])
    return (data,
            [{'name': col, 'id': col, 'editable': (col in editable_cols)} for col in dt_oil_columns],
            style_data_conditional,
            error_list,
            selected_oils, no_update, no_update,
            no_update, no_update, no_update,
            no_update, no_update, no_update,
            no_update, no_update, no_update)


@app.callback(
  Output('results', 'children'),
  Input('recipe-name','value'),
  Input('recipe-notes','value'),
  Input('selected-oils-data', 'data'),
  Input('lye_discount', 'value'),
  Input('water_calculation', 'value'),
  Input('water_by_oil_input', 'value'),
  Input('water_by_lye_input', 'value'),
  Input('water_lye_ratio_input', 'value'),
  Input('lye_type', 'value'),
  Input('get-recipe', 'n_clicks'),
  Input('pcsf-selected-oils-data', 'data'),
  State('additives-table', 'data'),
  State('other-ingredients-table', 'data')

)
def generate_recipe_table(recipe_name, recipe_notes, data, lye_discount, water_calculation, water_by_oil_input, water_by_lye_input, water_lye_ratio_input, lye_type, n_clicks, pcsf_oil_data, additives_data, other_ingredients_data):
   """Generate complete recipe table with all calculations and formatting"""
   if n_clicks is None:
        return ''
   
   # Validate inputs
   error = validate_recipe_inputs(recipe_name, data, pcsf_oil_data)
   if error:
        return error
 
   # Create other ingredients table (will be populated after calculating total weight)
   other_ingredient_recipe_table = None

   if n_clicks > 0 and data:
      lye_discount = float(lye_discount)
      
      # Define property ranges
      ranges = {
        "Hardness": "29 - 54",
        "Cleansing": "12 - 22",
        "Condition": "44 - 69",
        "Bubbly": "14 - 46",
        "Creamy": "16 - 48",
        "Iodine": "41 - 70",
        "INS": "136 - 165"
      }
      
      # Calculate lye requirements
      lye_adjusted, lye_adjusted_naoh, lye_adjusted_koh, total_oil_weight = calculate_lye_requirements(
          data, lye_type, lye_discount
      )
      
      # Calculate other ingredients with proper amounts based on total oil weight
      calculated_other_ingredients = calculate_other_ingredients(other_ingredients_data, total_oil_weight)
      other_ingredient_recipe_table = create_other_ingredients_table(
          calculated_other_ingredients, other_ingredient_recipe_columns
      )
      
      # Calculate water requirements
      water_needed = calculate_water_requirements(
          water_calculation, total_oil_weight, lye_adjusted,
          water_by_oil_input, water_by_lye_input, water_lye_ratio_input
      )
      
      # Calculate soap properties and fats
      properties, fats, fat_props, recipe_details = calculate_soap_properties(
          data, oil_prop_df, oil_fat_df
      )
      
      # Convert lye and water weights
      lye_weight_grams = lye_adjusted
      lye_weight_ounces = lye_weight_grams / 28.3495
      water_weight_grams = water_needed
      water_weight_ounces = water_weight_grams / 28.3495

      total_weight = total_oil_weight + water_weight_grams + lye_weight_grams

      # Create additives table
      recipe_additives_table = create_additives_details(
          additives_data, pcsf_oil_data, total_oil_weight
      )
      

      # Create overview table
      overview_dt = create_overview_table(
          total_oil_weight, water_weight_grams, lye_type, lye_discount, 
          lye_adjusted, fat_props
      )

      # Create oils table
      data_table = create_oils_table(recipe_details)

      # Create summary table
      summary_table = create_summary_table(
          total_oil_weight, water_weight_grams, water_weight_ounces,
          lye_weight_grams, lye_weight_ounces, total_weight, lye_type,
          lye_adjusted_naoh, lye_adjusted_koh
      )
      
      # Create properties and fats tables
      properties_table = create_properties_table(properties, ranges)
      fats_table = create_fats_table(fats)
      
      # Create compliance report
      compliance_report = create_compliance_report(
          data, total_oil_weight, water_weight_grams, total_weight,
          fat_props['saturated'], additives_data, pcsf_oil_data, oil_prop_df
      )

      return  html.Div([
          html.Div(id='print-trigger', style={'display': 'none'}),
          html.Br(className="no-print"),
          html.Div([
            dcc.Checklist(
              id='print-compliance-toggle',
              options=[{'label': ' Include compliance report in print', 'value': 1}],
              value=[],
              style={'fontSize': '12px', 'padding': '10px 0'}
            ),
          ], className="no-print"),
          html.Br(className="no-print"),
          html.Div(id="your-recipe", className="printable-content", children=[
      
          dbc.Row([
            dbc.Col([
              html.H4(recipe_name, className="print-header", style={'marginBottom': '4px', 'marginTop': '0px'}),
            ],width=12)
          ]),
          dbc.Row([
            dbc.Col([
              html.Div(recipe_notes, style={'whiteSpace': 'pre-wrap', 'fontSize': '14px', 'marginBottom': '4px'}),
           ],width=12)
          ]),
          
          dbc.Row([
            dbc.Col([
              compliance_report,
            ],width=12, style={'marginBottom': '4px'}, id='compliance-report-row')
          ]),
          
          dbc.Row([
              dbc.Col([
                overview_dt,
              ],width=4),
              dbc.Col([
                fats_table,
              ],width=4),
              dbc.Col([
                properties_table,
              ],width=4),
          ], style={'marginBottom': '4px'}),
          dbc.Row([
            dbc.Col([            
              data_table,
            ],width=6, style={'marginBottom': '6px'}),
            dbc.Col([
              summary_table,
            ],width=6, style={'marginBottom': '6px'}),
          ]),
          dbc.Row([
            dbc.Col([
              recipe_additives_table,
            ],width=12, style={'marginBottom': '6px'}),
          ]),
          dbc.Row([
            dbc.Col([
              other_ingredient_recipe_table,
            ],width=12),
          ])
      ], style={'paddingLeft': '10px', 'paddingRight': '10px'})
      ], style={'width': '100%'})
  #return html.Div()



# Callback to initialize and update the additives table with uploaded data
@app.callback(
   Output('additives-table', 'data'),
   Input('upload-recipe-json', 'contents'),
   State('upload-recipe-json', 'filename'),
   State('additives-table', 'data')
)
def update_additives_table(contents, filename, data):
      """Load additives table data from uploaded JSON recipe"""
      ctx = callback_context
      trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

      if trigger_id == 'upload-recipe-json' and contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                recipe = json.loads(decoded)
                new_data = recipe.get('additives-table', [])
                return new_data
         
        except Exception as e:
            return (no_update)

      else:
            return (data)


 
from slugify import slugify
# Callback to handle recipe export
@app.callback(
    Output('download-recipe', 'data'),
    Input('export-recipe', 'n_clicks'),
    State('selected-oils-data', 'data'),
    State('recipe-name', 'value'),
    State('recipe-notes', 'value'),
    State('unit', 'value'),
    State('lye_type', 'value'),
    State('lye_discount', 'value'),
    State('method_calculation', 'value'),
    State('total_weight', 'value'),
    State('water_calculation', 'value'),
    State('water_by_oil_input', 'value'),
    State('water_by_lye_input', 'value'),
    State('water_lye_ratio_input', 'value'),
    State('pcsf-selected-oils-data', 'data'),
    State('additives-table', 'data'),
    State('other-ingredients-table', 'data'),
    prevent_initial_call=True,
)
def export_recipe(n_clicks, selected_oils, recipe_name, recipe_notes, unit, lye_type, lye_discount, method_calculation, total_weight, water_calculation, water_by_oil_input, water_by_lye_input, water_lye_ratio_input,pcsf_data,additives_data,other_ingredients_data):
    """
    Export recipe to JSON file
    
    Converts all string values from Dash tables to proper numeric types
    before saving to ensure JSON can be reloaded correctly.
    """
    if n_clicks > 0:
        # Convert numeric string values to numbers for selected_oils
        cleaned_selected_oils = []
        for oil in selected_oils:
            cleaned_oil = oil.copy()
            try:
                cleaned_oil['Grams'] = float(oil['Grams']) if oil['Grams'] else 0
            except (ValueError, TypeError):
                cleaned_oil['Grams'] = 0
            try:
                cleaned_oil['Ounces'] = float(oil['Ounces']) if oil['Ounces'] else 0
            except (ValueError, TypeError):
                cleaned_oil['Ounces'] = 0
            try:
                cleaned_oil['Percent'] = float(oil['Percent']) if oil['Percent'] else 0
            except (ValueError, TypeError):
                cleaned_oil['Percent'] = 0
            cleaned_selected_oils.append(cleaned_oil)
        
        # Convert numeric string values for PCSF oils
        cleaned_pcsf_data = []
        for oil in pcsf_data:
            cleaned_oil = oil.copy()
            try:
                cleaned_oil['%TOW'] = float(oil['%TOW']) if oil['%TOW'] else 0
            except (ValueError, TypeError):
                cleaned_oil['%TOW'] = 0
            cleaned_pcsf_data.append(cleaned_oil)
        
        # Convert numeric values for scalar fields
        def to_number(val):
            if val is None or val == '':
                return None
            try:
                return float(val) if '.' in str(val) else int(val)
            except (ValueError, TypeError):
                return val
        
        # Prepare the recipe data
        recipe_data = {
            'selected_oils': cleaned_selected_oils,
            'recipe_name': recipe_name,
            'recipe_notes': recipe_notes,
            'unit': unit,
            'lye_type': lye_type,
            'lye_discount': to_number(lye_discount),
            'method_calculation': method_calculation,
            'total_weight': to_number(total_weight),
            'water_calculation': water_calculation,
            'water_by_oil_input': to_number(water_by_oil_input),
            'water_by_lye_input': to_number(water_by_lye_input),
            'water_lye_ratio_input': water_lye_ratio_input,
            'pcsf-selected-oils-data' : cleaned_pcsf_data,
            'additives-table' :  additives_data,
            'other-ingredients-table' :  other_ingredients_data 
        }

        # Convert the data to a JSON string
        json_data = json.dumps(recipe_data, indent=4)
        
        # Filename for the JSON file
        filename = slugify(recipe_name) + '.json'
        
        # Return the data for download
        return dcc.send_bytes(json_data.encode(), filename)
    
    return no_update


# Callback to display oils totals
@app.callback(
    Output('oils-totals', 'children'),
    Input('selected-oils-data', 'data')
)
def display_oils_totals(data):
    """Calculate and display totals for selected oils"""
    if not data:
        return html.Div()
    
    total_grams = sum(float(row.get('Grams', 0)) for row in data)
    total_ounces = sum(float(row.get('Ounces', 0)) for row in data)
    total_percent = sum(float(row.get('Percent', 0)) for row in data)
    
    # Color total percent text orange if over 100%
    percent_color = 'orange' if total_percent != 100 else 'black'
    
    return html.Div([
        f"Total Grams: {total_grams:.2f} | Total Ounces: {total_ounces:.2f} | ",
        html.Span(
            f"Total Percent: {total_percent:.1f}%",
            style={'color': percent_color, 'fontWeight': 'bold'}
        )
    ])


# Callback to show/hide export button based on user edits
@app.callback(
    Output('export-recipe-container', 'style'),
    Input('recipe-name', 'value'),
    Input('recipe-notes', 'value'),
    Input('selected-oils-data', 'data'),
    Input('lye_discount', 'value'),
    Input('unit', 'value'),
    Input('lye_type', 'value'),
    Input('method_calculation', 'value'),
    Input('total_weight', 'value'),
    Input('water_calculation', 'value'),
    Input('water_by_oil_input', 'value'),
    Input('water_by_lye_input', 'value'),
    Input('water_lye_ratio_input', 'value'),
    Input('pcsf-selected-oils-data', 'data'),
    Input('additives-table', 'data'),
    Input('other-ingredients-table', 'data'),
)
def show_export_button(*args):
    """Show export button if any edit has been made"""
    # Check if any input has a value (indicating user has made edits)
    has_edits = any(
        arg is not None and arg != '' and (not isinstance(arg, list) or len(arg) > 0)
        for arg in args
    )
    
    if has_edits:
        return {'display': 'block'}
    return {'display': 'none'}


# Clientside callback for print button
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks && n_clicks > 0) {
            window.print();
        }
        return '';
    }
    """,
    Output('print-trigger', 'children'),
    Input('print-button', 'n_clicks'),
    prevent_initial_call=True
)

# Callback to toggle oil properties modal
@app.callback(
    Output("oil-properties-modal", "is_open"),
    [Input("oil-properties-btn", "n_clicks"), Input("close-oil-modal", "n_clicks")],
    [State("oil-properties-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_oil_modal(open_clicks, close_clicks, is_open):
    """Toggle oil properties modal open/close"""
    if open_clicks or close_clicks:
        return not is_open
    return is_open


@app.callback(
    Output('oil-search-results', 'children'),
    [Input('search-oils-btn', 'n_clicks')],
    [State('cleansing-filter', 'value'),
     State('hardness-filter', 'value'),
     State('condition-filter', 'value'),
     State('bubbly-filter', 'value'),
     State('creamy-filter', 'value'),
     State('lauric-filter', 'value'),
     State('myristic-filter', 'value'),
     State('palmitic-filter', 'value'),
     State('stearic-filter', 'value'),
     State('oleic-filter', 'value'),
     State('linoleic-filter', 'value'),
     State('linolenic-filter', 'value'),
     State('ricinoleic-filter', 'value')],
    prevent_initial_call=True
)
def search_oils(n_clicks, cleansing_range, hardness_range, condition_range, bubbly_range, creamy_range, lauric_range, myristic_range, palmitic_range, stearic_range, oleic_range, linoleic_range, linolenic_range, ricinoleic_range):
    """Search and filter oils based on property criteria"""
    if n_clicks is None or n_clicks == 0:
        return html.Div()
    
    cleansing_min, cleansing_max = cleansing_range
    hardness_min, hardness_max = hardness_range
    condition_min, condition_max = condition_range
    bubbly_min, bubbly_max = bubbly_range
    creamy_min, creamy_max = creamy_range
    lauric_min, lauric_max = lauric_range
    myristic_min, myristic_max = myristic_range
    palmitic_min, palmitic_max = palmitic_range
    stearic_min, stearic_max = stearic_range
    oleic_min, oleic_max = oleic_range
    linoleic_min, linoleic_max = linoleic_range
    linolenic_min, linolenic_max = linolenic_range
    ricinoleic_min, ricinoleic_max = ricinoleic_range
    
    # Merge oil properties with fat data
    merged_df = oil_prop_df.merge(oil_fat_df, left_index=True, right_index=True, how='left')
    
    filtered_df = merged_df[
        (merged_df['Cleansing'] >= cleansing_min) & (merged_df['Cleansing'] <= cleansing_max) &
        (merged_df['Hardness'] >= hardness_min) & (merged_df['Hardness'] <= hardness_max) &
        (merged_df['Condition'] >= condition_min) & (merged_df['Condition'] <= condition_max) &
        (merged_df['Bubbly'] >= bubbly_min) & (merged_df['Bubbly'] <= bubbly_max) &
        (merged_df['Creamy'] >= creamy_min) & (merged_df['Creamy'] <= creamy_max) &
        (merged_df['Lauric'] >= lauric_min) & (merged_df['Lauric'] <= lauric_max) &
        (merged_df['Myristic'] >= myristic_min) & (merged_df['Myristic'] <= myristic_max) &
        (merged_df['Palmitic'] >= palmitic_min) & (merged_df['Palmitic'] <= palmitic_max) &
        (merged_df['Stearic'] >= stearic_min) & (merged_df['Stearic'] <= stearic_max) &
        (merged_df['Oleic'] >= oleic_min) & (merged_df['Oleic'] <= oleic_max) &
        (merged_df['Linoleic'] >= linoleic_min) & (merged_df['Linoleic'] <= linoleic_max) &
        (merged_df['Linolenic'] >= linolenic_min) & (merged_df['Linolenic'] <= linolenic_max) &
        (merged_df['Ricinoleic'] >= ricinoleic_min) & (merged_df['Ricinoleic'] <= ricinoleic_max)
    ]
    
    if filtered_df.empty:
        return html.Div([
            html.Br(),
            html.P("No oils found matching your criteria.", style={'color': 'red', 'fontWeight': 'bold'})
        ])
    
    results_table = dash_table.DataTable(
        data=filtered_df.reset_index().to_dict('records'),
        columns=[
            {'name': 'Oil', 'id': 'Oil'},
            {'name': 'Cleansing', 'id': 'Cleansing'},
            {'name': 'Hardness', 'id': 'Hardness'},
            {'name': 'Condition', 'id': 'Condition'},
            {'name': 'Bubbly', 'id': 'Bubbly'},
            {'name': 'Creamy', 'id': 'Creamy'},
            {'name': 'Iodine', 'id': 'Iodine'},
            {'name': 'INS', 'id': 'INS'},
            {'name': 'Lauric', 'id': 'Lauric'},
            {'name': 'Myristic', 'id': 'Myristic'},
            {'name': 'Palmitic', 'id': 'Palmitic'},
            {'name': 'Stearic', 'id': 'Stearic'},
            {'name': 'Oleic', 'id': 'Oleic'},
            {'name': 'Linoleic', 'id': 'Linoleic'},
            {'name': 'Linolenic', 'id': 'Linolenic'},
            {'name': 'Ricinoleic', 'id': 'Ricinoleic'},
        ],
        sort_action="native",
        style_header={
            'fontSize': '13px',
            'fontWeight': 'bold',
            'paddingLeft': '10px',
            'backgroundColor': '#fafafa',
            'cursor': 'pointer'
        },
        style_cell={
            'textAlign': 'left',
            'paddingLeft': '10px',
            'fontSize': '12px',
        },
        style_as_list_view=True,
    )
    
    return html.Div([
        html.Br(),
        html.P(f"Found {len(filtered_df)} oil(s) matching your criteria:", style={'fontWeight': 'bold'}),
        results_table
    ])


# Callback to show/hide print button based on results
@app.callback(
    Output('print-button-container', 'style'),
    Input('results', 'children')
)
def show_print_button(results):
    """Show print button only when results exist"""
    if results and results != html.Div():
        return {'display': 'block'}
    return {'display': 'none'}


# Callback to toggle compliance report print visibility
@app.callback(
    Output('compliance-report-row', 'className'),
    Input('print-compliance-toggle', 'value')
)
def toggle_compliance_print(toggle_value):
    """Add/remove no-print class based on toggle"""
    if toggle_value and 1 in toggle_value:
        return ''  # Remove no-print class so it prints
    return 'no-print'  # Add no-print class to hide from print


# Callback to populate oil comparison dropdown
@app.callback(
    Output('oil-properties-compare-oils', 'options'),
    Input('oil-properties-modal', 'is_open')
)
def populate_oil_dropdown(is_open):
    """Populate the oil selection dropdown"""
    if is_open:
        return [{'label': oil, 'value': oil} for oil in oil_prop_df.index]
    return []


# Callback to display comparison results
@app.callback(
    Output('oil-properties-compare-results', 'children'),
    Input('oil-properties-compare-oils', 'value')
)
def display_oil_comparison(selected_oils):
    """Display comparison table for selected oils"""
    if not selected_oils or len(selected_oils) == 0:
        return html.Div()

    # Merge oil properties with fat data
    merged_df = oil_prop_df.merge(oil_fat_df, left_index=True, right_index=True, how='left')

    # Filter to selected oils
    comparison_df = merged_df.loc[selected_oils]

    comparison_table = dash_table.DataTable(
        data=comparison_df.reset_index().to_dict('records'),
        columns=[
            {'name': 'Oil', 'id': 'Oil'},
            {'name': 'Cleansing', 'id': 'Cleansing'},
            {'name': 'Hardness', 'id': 'Hardness'},
            {'name': 'Condition', 'id': 'Condition'},
            {'name': 'Bubbly', 'id': 'Bubbly'},
            {'name': 'Creamy', 'id': 'Creamy'},
            {'name': 'Iodine', 'id': 'Iodine'},
            {'name': 'INS', 'id': 'INS'},
            {'name': 'Lauric', 'id': 'Lauric'},
            {'name': 'Myristic', 'id': 'Myristic'},
            {'name': 'Palmitic', 'id': 'Palmitic'},
            {'name': 'Stearic', 'id': 'Stearic'},
            {'name': 'Oleic', 'id': 'Oleic'},
            {'name': 'Linoleic', 'id': 'Linoleic'},
            {'name': 'Linolenic', 'id': 'Linolenic'},
            {'name': 'Ricinoleic', 'id': 'Ricinoleic'},
        ],
        sort_action="native",
        style_header={
            'fontSize': '13px',
            'fontWeight': 'bold',
            'paddingLeft': '10px',
            'backgroundColor': '#fafafa',
        },
        style_cell={
            'textAlign': 'left',
            'paddingLeft': '10px',
            'fontSize': '12px',
        },
        style_as_list_view=True,
    )

    return html.Div([
        comparison_table
    ])


if __name__ == '__main__':
  app.run(debug=True)

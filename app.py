# Import packages
from dash import Dash, html, dash_table, dcc, Output, Input, State, callback_context, dash_table, no_update
import pandas as pd
import dash_ag_grid as dag
import json
import base64
import io
import dash_bootstrap_components as dbc
from pathlib import Path

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
pcsf=("Argan Oil","Apricot Kernal Oil", "Coconut Oil","Olive Oil","Sweet Almond Oil","Cocoa Butter","Shea Butter")

# Initial data for the DataTable

htfhp_additive_rowData = [
    {"section": "Trace Accelerants", "Additive": "Stearic Acid (%TOW)", "Value": "Add to oil list at 5-8%"},
    {'section': "Trace Accelerants", 'Additive': 'Finished Soap (%TOW)', 'Value': None},
    {'section': "Trace Accelerants", 'Additive': 'Eugenol (drops)', 'Value': None, 'Placeholder' : 'drops'},
    {"section": "Humectants and Hardeners", 'Additive': 'Sodium Lactate (%TOW)', 'Value': None},
    {'section': "Humectants and Hardeners", 'Additive': 'Sodium Chloride (%TOW)', 'Value': None},
    {"section": "Lather", 'Additive': 'Castor Oil (%TOW)', 'Value': 'Add to oil list at 5-15%'},
    {'section': "Lather", 'Additive': 'Jojoba Oil (%TOW) ', 'Value': 'Add to oil list at 5-10%'},
    {'section': "Lather", 'Additive': 'Dual Lye', 'Value': 'See LyeType'},
    {'section': "Lather", 'Additive': 'Sorbitol (%TOW)', 'Value': None},
    {'section': "Lather", 'Additive': 'Cetyl Alcohol (%TOW)', 'Value': None},
    {'section': "Lather", 'Additive': 'Citric Acid (%TOW)', 'Value': None},
    {'section': "Lather", 'Additive': 'Honey (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Yogurt (%TOW)', 'Value': None}
]

# Define tooltips for each cell
htfhp_tooltips = [
    {"section": "Oil used to speed up trace", "Additive": "Stearic acid acts as a thicking agent and emulsion stabilizer. Weigh, mix, and melt with your other recipe oils. Add to your recipe oil list for correct lye calculation.", "Value": "5-8% is recommended in your recipe"},
    {"section": "Additive used to speed up trace", "Additive": "Finished soap acts as a emulsion accelerant. Grate and melt with oils.", "Value": "0.05-1.0% TOW is recommended"},
    {"section": "Additive used to speed up trace", "Additive": "Clove and cinnamon oil both act as trace accelerants. Add a few drop to the heated oil. ", "Value": "a few drops of either are recommended"},
    {"section": "Section for humectants and hardeners", "Additive": "Sodium lactate is a humectant due to its ability to bind woater molecules.", "Value": "3-4% TOW is recommended"},
    {"section": "Section for humectants and hardeners", "Additive": "NaCl or table salt acts similar to Sodium lactate.", "Value": "0.05%-1% TOW is recommended"},
    {"section": "Section for lather", "Additive": "The high content of ricinoleic acid in Castor oil helps increase the solubility of soap and allows more soap to dissolve at a faster rate therefore increasing the reate of lather formation. Good to use with lauric and myristic acid. Add Castor oil to your recipe oil list for correct lye calculation.", "Value": "5-15% TOW is recommended in your recipe"},
    {"section": "Section for lather", "Additive": "Jojoba is actually a wax and not an oil and generates the formation of soap and an alcohol. The alcohol adds stability and longevity to the lather. Add Jojoba to your recipe oil list for correct lye calculation.", "Value": "5-10% TOW is recommended in your recipe"},
    {"section": "Section for lather", "Additive": "The presence of a small amount of KOH (5%) helps to increase the rate of lather formation and stability. Excellent for castile soaps. Select Dual lye in selection above.", "Value": "See lye type"},
    {"section": "Section for lather", "Additive": "Sorbitol will help create a super sudsy and bubbly later", "Value": "1-5% TOW is recommended"},
    {"section": "Section for lather", "Additive": "Cetyl Alcohol acts similarly to Jojoba oil. The alcohol adds stability and longevity to the lather.", "Value": "1-3% TOW is recommeded"},
    {"section": "Section for lather", "Additive": "Citric acid helps lather by chelating minerals", "Value": "1-2% TOW is recommended"},
    {"section": "Section for lather", "Additive": "Honey, sugar, and molassas act similarly to Sorbitol, increasing lather. It also has chelating effects.", "Value": "1-5% TOW is recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Yogurt or buttermilk, goat milk, coconut yogrt, almond milk, juice, tofu,wine, and coconut milk help to increase the fluidity of the cook.", "Value": "2-5% TOW is recommended"}
]

htfhp_tooltip_data = [
    {column: {'value': str(row[column]), 'type': 'text'} for column in row}
    for row in htfhp_tooltips
]

htfhp_additive_columns = [
    {"name": "Category", "id": "section"},
    {"name": "Additive", "id": "Additive"},
    {"name": "Value", "id": "Value", "editable": True}
]
# Define colors for each section
section_colors = {
    "Trace Accelerants": "#fcfce9",
    "Humectants and Hardeners": "#e9fcfc",
    "Lather": "#e9f2fc",
    "Fluid Enhancer":"#fce9e9"
}

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

# Convert the list of dictionaries to a DataFrame
additive_df = pd.DataFrame(htfhp_additive_rowData)

additive_table = dash_table.DataTable(
    id='additives-table',
    columns=htfhp_additive_columns,
    data=additive_df.to_dict('records'),
    tooltip_data=htfhp_tooltip_data,
    style_cell={
        'textAlign': 'left',
        'padding': '10px',
        'font-size': '13px',
        'text-wrap': 'stable'
    },
    style_table={ 'border': '1px solid black', 'borderCollapse': 'collapse', 'text-wrap': 'stable' ,'overflowX': 'hidden'},
    style_header={
          'font-size': '13px',
          'font-weight': 'bold',
          'padding-left': '10px',
          'background-color' : '#fafafa'
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
    {"name": "Amount", "id": "Amount","editable": True},
    {"name": "Unit", "id": "Unit","editable": True},
    {"name": "Notes", "id": "Notes", "editable": True}
]

other_ingredient_initial_rows = [
    {"Ingredient": "", "Amount": "", "Unit": "", "Notes": ""},
    {"Ingredient": "", "Amount": "", "Unit": "", "Notes": ""}
]

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'])

# App layout
app.layout = html.Div([
    html.Div([
    dbc.Row(
        dbc.Col(
            html.H1("Sofia's Soap Calculator", style={'textAlign': 'left', 'color': '#000', 'padding-left': '10px'}),
            width=4
        )
    ),
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Hr(),
            html.H3("Your Recipe:"),
            dcc.Upload(id='upload-recipe-json',children=html.Button('Upload Recipe (JSON)', style={'border': 'none', 'border-radius': '0.25rem', 'padding': '0.5rem 1rem', 'background-color': '#007bff', 'color': 'white', 'font-size': '1rem', 'cursor': 'pointer'}),multiple=False,style={'display': 'inline-block'}),
            html.Div(id='upload-recipe-json-output'),  # Output for upload feedback
            html.Hr(),
        ], width=12)
    ),
    dbc.Row(
        dbc.Col(
            html.Div([
                dcc.Input(id='recipe-name', placeholder='Enter recipe name', type='text', style={'width': '30%', 'height': '30px'}, required=True),
            ])
        )
    ),
    dbc.Row(
        dbc.Col(
            html.Div([
                dcc.Input(id='recipe-notes', placeholder='Enter recipe notes', type='text', style={'width': '30%', 'height': '80px'}),
            ])
        )
    ),
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Hr(),
            html.H3("Select Your Recipe Parameters:"),
            html.Hr(),
        ], width=4)
    ),
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
                        style={'padding-left': '10px'}
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
                        style={'padding-left': '10px'}
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
        ], width=1),
        dbc.Col([
            html.Div([
                html.Label(html.Strong('Lye Discount:'), id='Discount-tooltip'),
                html.Br(),
                dcc.Input(id='lye_discount', type='number', value='5', style={'width': '45px', 'height': '20px', 'margin-left': '25px'}),
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
        ], width=1),
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
                                                    '% of Oil Weight:',
                                                    dcc.Input(
                                                        id='water_by_oil_input',
                                                        type='number',
                                                        value='38',
                                                        style={'width': '45px', 'height': '20px', 'margin-left': '5px'}
                                                    )
                                                ],
                                                style={'display': 'flex', 'align-items': 'center'}
                                            ),
                                            html.Label('%'),
                                        ],
                                        style={'display': 'inline-flex', 'align-items': 'center'}
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
                                                        style={'width': '45px', 'height': '20px', 'margin-left': '5px'}
                                                    )
                                                ],
                                                style={'display': 'flex', 'align-items': 'center'}
                                            ),
                                            html.Label('%'),
                                        ],
                                        style={'display': 'inline-flex', 'align-items': 'center'}
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
                                                        style={'width': '45px', 'height': '20px', 'margin-left': '5px'}
                                                    )
                                                ],
                                                style={'display': 'flex', 'align-items': 'center'}
                                            ),
                                        ],
                                        style={'display': 'inline-flex', 'align-items': 'center'}
                                    ),
                                    'value': 'water_lye_ratio'
                                },
                            ],
                            value='water_by_oil',
                            labelStyle={'display': 'block', 'margin-right': '10px'}
                        ),
                    ]
                )
            ]), width=2
        ),
    ]),
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Hr(),
            html.H3("Recipe Oils:"),
            html.Hr(),
        ], width=4)
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Store(id='stored-selected-oils', storage_type='local'),
                    html.Label([
                        html.Strong('Select your recipe oils:'),
                        dcc.Dropdown(id='selected-oils', multi=True)
                    ], style={"width": "100%", 'padding-left': '10px'}),
                ]),
                width=4
            ),
        ]
    ),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Div(id='select-oils-output-container'),
            html.Div([
                dash_table.DataTable(
                    id='selected-oils-data',
                    columns=[{'name': col, 'id': col, 'editable': True} for col in dt_oil_columns],
                    data=[],
                    editable=True,
                    row_deletable=True,
                    style_header={
                        'font-size': '13px',
                        'font-weight': 'bold',
                        'padding-left': '10px',
                    },
                    style_cell={
                        'text-align': 'left',
                        'padding-left': '10px',
                        'font-size': '13px',
                    },
                ),
            ],
                style={'padding-left': '10px'},  # Add left padding here
            ),
            html.Div(id='selected-oils-updated'),
        ], width=4)
    ]),
    dbc.Row(
        dbc.Col([
            html.Br(), html.Hr(), html.Br(),
        ], width=3, style={'padding-left': '25px'})
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Store(id='stored-pcsf-selected-oils', storage_type='local'),
                    html.Label([
                        html.Strong('Select your Post Cook Superfat Oils:'),
                        dcc.Dropdown(id='pcsf-selected-oils', multi=True)
                    ], style={"width": "100%", 'padding-left': '10px'}),
                ]),
                width=4
            ),
        ]
    ),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Br(),
                html.Div(id='select-oils-pcsf-output-container'),
                dash_table.DataTable(
                    id='pcsf-selected-oils-data',
                    columns=[
                        {'name': 'PCSF Oil', 'id': 'PCSF Oil'},
                        {'name': '%TOW', 'id': '%TOW', 'editable': True}
                    ],
                    data=[],
                    editable=True,
                    row_deletable=True,
                    style_header={
                        'font-size': '13px',
                        'font-weight': 'bold',
                        'padding-left': '10px',
                    },
                    style_cell={
                        'text-align': 'left',
                        'padding-left': '10px',
                        'font-size': '13px',
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
            ], style={"width": "100%", 'padding-left': '10px'}),
            width=2
        )
    ]),
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Hr(),
            html.H3("Additives for HTFHP Soap making:"),
            html.Hr(),
        ], width=4)
    ),
    dbc.Row([
        dbc.Col(additive_table, width=6),
    ]),
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Hr(),
            html.H3("Other Ingredients:"),
            html.Hr(),
        ], width=4)
    ),
    dbc.Row([
      dbc.Col([
      # New table for other ingredients
        html.Br(),
        dash_table.DataTable(
         id='other-ingredients-table',
         columns=other_ingredient_columns,
         data=other_ingredient_initial_rows,
         row_deletable=True,
        style_cell={
          'textAlign': 'left',
          'padding': '10px',
          'font-size': '13px',
        },
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_header={
          'font-size': '13px',
          'font-weight': 'bold',
          'padding-left': '10px',
          'background-color' : '#fafafa'
        },
        #style_table={'overflowX': 'auto'}
      ),
      html.Div(
        dbc.Button("Add Row", id="add-row-button", color="primary"),
        style={'display': 'flex', 'justify-content': 'flex-end', 'margin-top': '20px'}
      ),
      #html.Button('Add Row', id='add-row-button' ,style={'display':'right'}),
      ],width=4)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='error-message', style={'color': 'red'}),
            
        ],width=4)
    ]),
    dbc.Row(
        dbc.Col(
            html.Div(
                dbc.Button('Generate Recipe', id='get-recipe', n_clicks=0, style={'background-color':'orange', 'color':'black'}),
                #style={'padding-left': '10px'}
            ),
            width=4
        )
    ),

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
    dbc.Row(
      dbc.Col([
          html.Br(),
          html.Hr(),
          html.Br(),
          dbc.Button('Export Recipe (JSON)', id='export-recipe', n_clicks=0, color='primary'),
          dcc.Download(id='download-recipe'),  # Add this component
          html.Div(id='export-recipe-json-output')  # Output for export feedback
      ], width=4)
    )],className='no-print',style={'width': '100%'}),
], style={'padding-left': '20px','width': '100%'})

@app.callback(
    Output('other-ingredients-table', 'data'),
    [Input('add-row-button', 'n_clicks'),
     Input('upload-recipe-json', 'contents')],
    [State('upload-recipe-json', 'filename'),
     State('other-ingredients-table', 'data')],
    prevent_initial_call=True
)
def update_other_ingredients_table(n_clicks, contents, filename, data):
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
    elif trigger_id == 'add-row-button' and n_clicks:
        data.append({"Ingredient": "", "Amount": "", "Unit": "", "Notes": ""})
        return data
    else:
        return no_update


# Callback to update the pcsf dropdown options based on the data in the dropdown and selected oils
@app.callback(
  Output('pcsf-selected-oils', 'options'),
  Output('stored-pcsf-selected-oils', 'data'),
  Input('pcsf-selected-oils', 'value'),
  State('stored-pcsf-selected-oils', 'data')
)
def update_pcsf_dropdown(selected_oils, stored_selected_oils):
  if selected_oils is None:
      selected_oils = []
  if stored_selected_oils is None:
      stored_selected_oils = []

  all_options = [{'label': i, 'value': i} for i in pcsf]
  updated_selected_oils = list(set(stored_selected_oils + selected_oils))

  return all_options, updated_selected_oils


# Callback to initialize and update the DataTable
@app.callback(
  [Output('pcsf-selected-oils-data', 'data'),
   Output('pcsf-selected-oils-data', 'columns'),
   Output('pcsf-selected-oils', 'value')],
  [Input('pcsf-selected-oils', 'value'),
   Input('pcsf-selected-oils-data', 'data_timestamp'),
   Input('upload-recipe-json', 'contents')],
  [State('upload-recipe-json', 'filename'),
   State('pcsf-selected-oils-data', 'data'),
   State('stored-pcsf-selected-oils', 'data')]
)
def update_pcsf_table(selected_oils,timestamp, contents, filename, data, stored_selected_oils):
      ctx = callback_context
      trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

      if trigger_id == 'upload-recipe-json' and contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                recipe = json.loads(decoded)
                new_data = recipe.get('pcsf-selected-oils-data', [])
                return new_data, [{'name': 'PCSF Oil', 'id': 'PCSF Oil'} , {'name': '%TOW', 'id': '%TOW' , 'editable': True}], [oil['PCSF Oil'] for oil in new_data]
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

      return new_data, [
        {'name': 'PCSF Oil', 'id': 'PCSF Oil'} , {'name': '%TOW', 'id': '%TOW' , 'editable': True}
      ], selected_oils


# Callback to show/hide total weight input based on method calculation
@app.callback(
  Output('total_weight', 'style'),
  Input('method_calculation', 'value')
)
def show_hide_total_weight_input(method):
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
  if selected_oils is None:
      selected_oils = []
  if stored_selected_oils is None:
      stored_selected_oils = []

  all_options = [{'label': oil, 'value': oil} for oil in oil_prop_df.index.tolist()] #df['Oil']]
  updated_selected_oils = list(set(stored_selected_oils + selected_oils))

  return all_options, updated_selected_oils


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
                recipe_name = recipe.get('recipe_name', '')
                recipe_notes = recipe.get('recipe_notes', '')
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
                        row['Grams'] = (percent / 100) * total_weight
                        row['Ounces'] = row['Grams'] / 28.3495
                    else:
                        row['Ounces'] = (percent / 100) * total_weight
                        row['Grams'] = row['Ounces'] * 28.3495
            if total_percent != 100:
                if total_percent < 100:
                    difference = 100 - total_percent
                    error_message.append(f'Please make sure your percentages add up to 100%. {total_percent}% is less than 100 by {difference}')
                else:
                    difference = total_percent - 100
                    error_message.append(f'Please make sure your percentages add up to 100%. {total_percent}% is more than 100 by {difference}')

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
   if n_clicks is None:
        return ''
   if not recipe_name:
        return html.Div('Recipe name is required!', style={'color': 'red'})
   if not data:
        return html.Div('At least one oil must be selected!', style={'color': 'red'})
   else:
     for row in data:
       if row['Grams'] == 0:
         return html.Div(f'Error: Grams value for {row["Oil"]} cannot be 0!', style={'color': 'red'})

   if pcsf_oil_data:
      for row in pcsf_oil_data:
        if row['%TOW'] == 0:
          return html.Div(f'Error: %TOW for PCSF Oil: {row["PCSF Oil"]} cannot be 0!', style={'color': 'red'})
 
   def convert_to_number(value):
       try:
          return float(value)
       except (ValueError, TypeError):
          return 0
   
   # Extract additive values from the additives_data
   additives = {row['Additive']: convert_to_number(row['Value']) for row in additives_data}
   finished_soap = additives.get('Finished Soap', 0)
   eugenol = additives.get('Eugenol', 0)
   sodium_lactate = additives.get('Sodium Lactate', 0)
   sodium_chloride = additives.get('Sodium Chloride', 0)
   sorbitol = additives.get('Sorbitol', 0)
   cetyl_alcohol = additives.get('Cetyl Alcohol', 0)
   citric_acid = additives.get('Citric Acid', 0)
   honey = additives.get('Honey', 0)
   yogurt = additives.get('Yogurt', 0)

   # Remove empty rows
   other_ingredients_filtered_data = [row for row in other_ingredients_data if any(row.values())]
   
   # Convert to DataFrame
   other_df = pd.DataFrame(other_ingredients_filtered_data)

   other_ingredient_recipe_table = dash_table.DataTable(
          columns=other_ingredient_columns,
          data=other_df.to_dict('records'),
          style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', "white-space": "pre-wrap"},
          style_cell={'textAlign': 'center', 'padding': '8px',"white-space": "pre-wrap"},
          style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
      )

   if n_clicks > 0 and data:
      lye_needed = 0
      lye_needed_naoh = 0
      lye_needed_koh = 0
      lye_discount = float(lye_discount)
      total_oil_weight = 0

      # Conversion factors
      naoh_to_koh = 40.00 / 56.11  # NaOH to KOH conversion factor

      recipe_details = []
      properties = {
          'Hardness': 0,
          'Cleansing': 0,
          'Condition': 0,
          'Bubbly': 0,
          'Creamy': 0,
          'Iodine' : 0,
          'INS' : 0,
      }
      ranges = {
        "Hardness": "29 - 54",
        "Cleansing": "12 - 22",
        "Condition": "44 - 69",
        "Bubbly": "14 - 46",
        "Creamy": "16 - 48",
        "Iodine": "41 - 70",
        "INS": "136 - 165"
      }
      fats = {
          'Lauric': 0,
          'Myristic': 0,
          'Palmitic': 0,
          'Stearic': 0,
          'Oleic': 0,
          'Linoleic': 0,
          'Linolenic': 0,
          'Ricinoleic': 0,
      }

      # Define lye proportions for dual
      naoh_proportion = 0.95
      koh_proportion = 0.05 
       
      for row in data:
          weight_grams = float(row['Grams'])
          weight_ounces = weight_grams / 28.3495
          percent = float(row['Percent'])

          total_oil_weight += weight_grams

          sap_value = float(row['NaOH SAP'])

          #lye_needed += sap_value * weight_grams
          #total_oil_weight += weight_grams
          if lye_type == 'NaOH':
              # Use SAP value for NaOH
              lye_needed += sap_value * weight_grams
          elif 'KOH' in lye_type:
              # Adjust SAP value for KOH
              sap_value /= naoh_to_koh
              if lye_type == 'KOH_90':
                  sap_value *= 1.10
              lye_needed += sap_value * weight_grams
          elif lye_type == 'dual_lye':
              # Calculate for NaOH
              naoh_sap_value = sap_value
              lye_needed_naoh += naoh_sap_value * weight_grams * naoh_proportion
              
              # Calculate for KOH
              koh_sap_value = sap_value / naoh_to_koh
              lye_needed_koh += koh_sap_value * weight_grams * koh_proportion
              
              # Combine both lye needs
              lye_needed = lye_needed_naoh + lye_needed_koh
      
          # Add properties from the oil_prop_df
          for prop in properties.keys():
              properties[prop] += round(float(oil_prop_df.loc[row['Oil'], prop]) * (percent/100),0)

          for fat in fats.keys():
              fats[fat] += round(float(oil_fat_df.loc[row['Oil'], fat])  * (percent/100) ,0)

          recipe_details.append({
              'Oil': row['Oil'],
              'Grams': weight_grams,
              'Ounces': weight_ounces,
              'Percent': percent
          })
      # initialize fat prop dict
      fat_props = {
        'saturated' : 0,
        'unsaturated' : 0
      }
      for fat in fats:
        if fat in saturated_fats:
          fat_props['saturated'] += fats[fat] 
        else: 
          fat_props['unsaturated'] += fats[fat] 

      lye_adjusted = lye_needed - (lye_needed * (lye_discount / 100)) if lye_discount else lye_needed

      water_needed = 0
      if water_calculation == 'water_by_oil':
          water_needed = total_oil_weight * (float(water_by_oil_input) / 100)
      elif water_calculation == 'water_by_lye':
          water_needed = (lye_adjusted / (float(water_by_lye_input) / 100)) - lye_adjusted
      elif water_calculation == 'water_lye_ratio':
          ratio_parts = water_lye_ratio_input.split(':')
          if len(ratio_parts) == 2:
              water_ratio = float(ratio_parts[0])
              lye_ratio = float(ratio_parts[1])
              water_needed = lye_adjusted * (water_ratio / lye_ratio)

      # Convert lye and water weights
      lye_weight_grams = lye_adjusted
      lye_weight_ounces = lye_weight_grams / 28.3495
      water_weight_grams = water_needed
      water_weight_ounces = water_weight_grams / 28.3495

      total_weight = total_oil_weight + water_weight_grams + lye_weight_grams

      # Additives details including directions, with dynamically formatted labels
      # Note: You can set the value of the 'value' field in grams for each additive accordingly
      additives_details = {
          f'Lather: Sorbitol ({sorbitol}% TOW)': {'value': sorbitol, 'type': 'TOW', 'directions': 'Add to the lye solution, at trace, after the cook, or mixed with colorants.'},
          f'Lather: Citric Acid ({citric_acid}% TOW)': {'value': citric_acid, 'type': 'TOW', 'directions': 'Dissolve in the lye solution.'},
          f'Humectants: Sodium Chloride ({sodium_chloride}% TOW)': {'value': sodium_chloride, 'type': 'TOW', 'directions': 'Dissolve in the lye solution or add to oils.'},
          f'Trace Accelerants: Finished Soap ({finished_soap}% TOW)': {'value': finished_soap, 'type': 'TOW', 'directions': 'Melt with oils.'},
          f'Trace Accelerants: Eugenol ({eugenol} drops)': {'value': eugenol, 'type': 'drops', 'directions': 'Add a few drops to heated oils.'},
          f'Humectants: Sodium Lactate ({sodium_lactate}% TOW)': {'value': sodium_lactate, 'type': 'TOW', 'directions': 'Add 30-60 seconds after mixing oils and lye solution, after a very thick trace, and before the expansion of the recipe.'},
          f'Lather: Cetyl Alcohol ({cetyl_alcohol}% TOW)': {'value': cetyl_alcohol, 'type': 'TOW', 'directions': 'Melted and added after trace.'},
          f'Lather: Honey ({honey}% TOW)': {'value': honey, 'type': 'TOW', 'directions': 'Add after the cook.'},
          f'Fluid Enhancer: Yogurt ({yogurt}% TOW)': {'value': yogurt, 'type': 'TOW', 'directions': 'Add after the cook.'},
      }
      for row in pcsf_oil_data:
          oil = row['PCSF Oil']
          tow = row['%TOW']
          additives_details[f'PCSF:{oil} ({tow} %TOW)'] = {'value': int(tow), 'type': 'TOW', 'directions': 'Add after the cook.'}

      
      # Conversion factor
      drops_to_grams = 1 / 30
      
      # Filter out additives with None or zero values
      filtered_additives = {k: v for k, v in additives_details.items() if v['value'] is not None and v['value'] > 0}
      
      # Convert to DataFrame
      recipe_additives_data = []
      for k, v in filtered_additives.items():
          if v['type'] == 'TOW':
              grams = round((v['value']/100) * total_oil_weight,2) 
          elif v['type'] == 'drops':
              grams = v['value'] * drops_to_grams
          else:
              grams = v['value']
          
          ounces = grams / 28.3495
          recipe_additives_data.append({
              'Additive': k,
              'grams': f"{grams:.2f}g",
              'ounces': f"{ounces:.2f}oz",
              'directions': v['directions']
          })
      
      recipe_additives_df = pd.DataFrame(recipe_additives_data)
      
      # Generate the Dash DataTable
      recipe_additives_table = dash_table.DataTable(
          id='recipe-additives-table',
          columns=[
              {'name': 'Additive', 'id': 'Additive'},
              {'name': 'Weight (g)', 'id': 'grams'},
              {'name': 'Weight (oz)', 'id': 'ounces'},
              {'name': 'Directions', 'id': 'directions'}
          ],
          data=recipe_additives_df.to_dict('records'),
          style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
          style_cell={'textAlign': 'center', 'padding': '8px'},
          style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
          style_cell_conditional=[
              {'if': {'column_id': 'grams'}, 'textAlign': 'center', 'width': '10%'},
              {'if': {'column_id': 'ounces'}, 'textAlign': 'center', 'width': '10%'},
              {'if': {'column_id': 'directions'}, 'textAlign': 'left', 'width': '50%'}
          ]
      )
      

      # prepare datatable for overview
      # Data for the overview table
      overview_data = {
          "Total Oil Weight": f"{total_oil_weight}g",
          "Water as percent of oil weight": f"{round((water_weight_grams / total_oil_weight) * 100)}%",
          "Lye Type": lye_type,
          "Lye Discount": f"{round(lye_discount)}%",
          "Lye Concentration": f"{round((lye_adjusted / (water_weight_grams + lye_adjusted)) * 100,1)}%",
          "Water : Lye Ratio": f"{water_weight_grams / lye_adjusted:.1f}:1",
          "Sat : Unsat Ratio": f"{round(fat_props['saturated']/(fat_props['saturated']+fat_props['unsaturated'])*100)}:{round(fat_props['unsaturated']/(fat_props['saturated']+fat_props['unsaturated'])*100)}",
           "" : ""
      }
      
      # Transform the data into a list of dictionaries
      transposed_data = [{"Prop": key, "Value": value} for key, value in overview_data.items()]
     
      
      # Columns for the transposed table
      transposed_columns = [
          {"name": "Prop", "id": "Prop"},
          {"name": "Value", "id": "Value"}
      ]
      
      # Create the DataTable for the transposed data
      overview_dt = dash_table.DataTable(
          id='overview-table',
          columns=transposed_columns,
          data=transposed_data,
          style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
          style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
          style_cell={'textAlign': 'center', 'padding': '5px', 'text-size':'12px'},
      ) 

      # Prepare DataTable for Oils columns and data
      columns = [
          {"name": "Oil", "id": "Oil"},
          {"name": "Grams", "id": "Grams"},
          {"name": "Ounces", "id": "Ounces"},
          {"name": "Percent", "id": "Percent"}
      ]

      data_table = dash_table.DataTable(
          columns=columns,
          data=[{
              'Oil': item['Oil'],
              'Grams': f"{item['Grams']:.2f}",
              'Ounces': f"{item['Ounces']:.2f}",
              'Percent': f"{item['Percent']:.2f}"
          } for item in recipe_details],
          style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
          style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
          style_cell={'textAlign': 'center', 'padding': '5px','text-size':'12px'},
      )

      # Generate a summara table
      # Create the summary data
      if lye_type == 'KOH_90':
        lye_type = 'KOH 90% purity'
      summary_data = {
          "Summary": [
              "Water Needed",
              f"Lye Needed ({lye_type})",
              "Total Oil Weight",
              "Total Weight"
          ],
          "Weight (g)": [
              f"{water_weight_grams:.2f}",
              f"{lye_weight_grams:.2f}",
              f"{total_oil_weight:.2f}",
              f"{total_weight:.2f}"
          ],
          "Weight (oz)": [
              f"{water_weight_ounces:.2f}",
              f"{lye_weight_ounces:.2f}",
              f"{total_oil_weight / 28.3495:.2f}",
              f"{total_weight / 28.3495:.2f}"
          ]
      }
      if lye_type == 'dual_lye':
        lye_adjusted_naoh = lye_needed_naoh - (lye_needed_naoh * (lye_discount / 100)) if lye_discount else lye_needed_naoh
        lye_adjusted_koh = lye_needed_koh - (lye_needed_koh * (lye_discount / 100)) if lye_discount else lye_needed_koh
        summary_data = {
          "Summary": [
              "Total Oil Weight",
              "Water Needed",
              "Lye Needed (NaOH)",
              "Lye Needed (KOH)",
              "Total Weight"
          ],
          "Weight (g)": [
              f"{total_oil_weight:.2f}",
              f"{water_weight_grams:.2f}",
              f"{lye_adjusted_naoh:.2f}",
              f"{lye_adjusted_koh:.2f}",
              f"{total_weight:.2f}"
          ],
          "Weight (oz)": [
              f"{total_oil_weight / 28.3495:.2f}",
              f"{water_weight_ounces:.2f}",
              f"{lye_adjusted_naoh / 28.3495:.2f}",
              f"{lye_adjusted_koh / 28.3495:.2f}",
              f"{total_weight / 28.3495:.2f}"
          ]
        }
  
      # Convert to DataFrame
      summary_df = pd.DataFrame(summary_data)
      
      summary_table = dash_table.DataTable(
          id='summary-table',
          columns=[{'name': col, 'id': col} for col in summary_df.columns],
          data=summary_df.to_dict('records'),
          style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
          style_cell={'textAlign': 'center', 'padding': '5px','text-size':'12px'},
          style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
      )
      
      # Generate properties table
      # Convert the properties and ranges into a DataFrame
      prop_data_df = pd.DataFrame({
        "Property": properties.keys(),
        "Range": ranges.values(),
        "Value": properties.values()
      })

      fats_df = pd.DataFrame(list(fats.items()), columns=['Fat Type', 'Amount'])
      prop_data_dict = prop_data_df.to_dict('records')
      properties_table = dash_table.DataTable(
        id='properties-table',
        columns=[{'name': col, 'id': col} for col in prop_data_df.columns],
        data=prop_data_dict,
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px','text-size':'12px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
      )

      # Generate the Dash DataTable

      fats_table = dash_table.DataTable(
        id='fats-table',
        columns=[{'name': col, 'id': col} for col in fats_df.columns],
        data=fats_df.to_dict('records'),
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse','overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px','text-size':'12px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
      )

      return  html.Div([
          dbc.Button('Print Recipe', id='print-button', n_clicks=0, className="no-print", style={'background-color':'primary', 'color':'white','padding-right': '38px','padding-left': '38px'}),
          html.Br(className="no-print"),
          html.Br(className="no-print"),
          html.Div(id="your-recipe", className="printable-content", children=[
      
          dbc.Row([
            dbc.Col([
              html.H4(recipe_name,className="print-header"),
            ],width=12)
          ]),
          dbc.Row([
            dbc.Col([
              html.Label(recipe_notes),
              html.Br(),
              html.Br(),
           ],width=12)
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
          ]),
          dbc.Row([
            dbc.Col([            
              html.Br(),
              data_table,
              html.Br(),
              summary_table,
              html.Br(),
              recipe_additives_table,
              html.Br(),
              other_ingredient_recipe_table,
            ],width=12),
          ])
      ],style={'left-padding':'20px'})
      ],style={'width':'100%'})
  #return html.Div()



# Callback to initialize and update the additives table with uploaded data
@app.callback(
   Output('additives-table', 'data'),
   Input('upload-recipe-json', 'contents'),
   State('upload-recipe-json', 'filename'),
   State('additives-table', 'data')
)
def update_additives_table(contents, filename, data):
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
if __name__ == '__main__':
  app.run(debug=True)

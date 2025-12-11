"""
Recipe calculation helper functions for soap calculator
"""
import pandas as pd
from dash import dash_table, html
import dash_bootstrap_components as dbc


def convert_to_number(value):
    """Convert string value to number, return 0 if conversion fails"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def validate_recipe_inputs(recipe_name, data, pcsf_oil_data):
    """
    Validate recipe inputs and return error message if invalid
    
    Returns:
        str or None: Error message HTML Div if invalid, None if valid
    """
    if not recipe_name:
        return html.Div('Recipe name is required!', style={'color': 'red'})
    if not data:
        return html.Div('At least one oil must be selected!', style={'color': 'red'})
    
    for row in data:
        if row['Grams'] == 0:
            return html.Div(f'Error: Grams value for {row["Oil"]} cannot be 0!', style={'color': 'red'})
    
    if pcsf_oil_data:
        for row in pcsf_oil_data:
            if row['%TOW'] == 0:
                return html.Div(f'Error: %TOW for PCSF Oil: {row["PCSF Oil"]} cannot be 0!', style={'color': 'red'})
    
    return None


def calculate_lye_requirements(data, lye_type, lye_discount):
    """
    Calculate lye requirements based on oils and lye type
    
    Returns:
        tuple: (lye_needed, lye_needed_naoh, lye_needed_koh, total_oil_weight)
    """
    lye_needed = 0
    lye_needed_naoh = 0
    lye_needed_koh = 0
    total_oil_weight = 0
    
    # Conversion factors
    naoh_to_koh = 40.00 / 56.11  # NaOH to KOH conversion factor
    
    # Define lye proportions for dual
    naoh_proportion = 0.95
    koh_proportion = 0.05
    
    for row in data:
        weight_grams = float(row['Grams'])
        total_oil_weight += weight_grams
        sap_value = float(row['NaOH SAP'])
        
        if lye_type == 'NaOH':
            lye_needed += sap_value * weight_grams
        elif 'KOH' in lye_type:
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
    
    # Apply lye discount
    lye_adjusted = lye_needed - (lye_needed * (lye_discount / 100)) if lye_discount else lye_needed
    lye_adjusted_naoh = lye_needed_naoh - (lye_needed_naoh * (lye_discount / 100)) if lye_discount else lye_needed_naoh
    lye_adjusted_koh = lye_needed_koh - (lye_needed_koh * (lye_discount / 100)) if lye_discount else lye_needed_koh
    
    return lye_adjusted, lye_adjusted_naoh, lye_adjusted_koh, total_oil_weight


def calculate_water_requirements(water_calculation, total_oil_weight, lye_adjusted, 
                                  water_by_oil_input, water_by_lye_input, water_lye_ratio_input):
    """Calculate water needed based on calculation method"""
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
    
    return water_needed


def calculate_soap_properties(data, oil_prop_df, oil_fat_df):
    """
    Calculate soap properties and fat composition from oils
    
    Args:
        data: List of oil dictionaries with Oil, Grams, Percent, etc
        oil_prop_df: DataFrame with oil properties (Hardness, Cleansing, etc)
        oil_fat_df: DataFrame with fat composition (Lauric, Myristic, etc)
    
    Returns:
        tuple: (properties dict, fats dict, fat_props dict, recipe_details list)
    """
    properties = {
        'Hardness': 0,
        'Cleansing': 0,
        'Condition': 0,
        'Bubbly': 0,
        'Creamy': 0,
        'Iodine': 0,
        'INS': 0,
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
    
    saturated_fats = ("Lauric", "Myristic", "Palmitic", "Stearic")
    recipe_details = []
    
    for row in data:
        weight_grams = float(row['Grams'])
        weight_ounces = weight_grams / 28.3495
        percent = float(row['Percent'])
        oil_name = row['Oil']
        
        # Add properties from the oil_prop_df
        for prop in properties.keys():
            properties[prop] += round(float(oil_prop_df.loc[oil_name, prop]) * (percent/100), 0)
        
        # Calculate fats from oil_fat_df
        for fat in fats.keys():
            fats[fat] += round(float(oil_fat_df.loc[oil_name, fat]) * (percent/100), 0)
        
        recipe_details.append({
            'Oil': oil_name,
            'Grams': weight_grams,
            'Ounces': weight_ounces,
            'Percent': percent
        })
    
    # Calculate fat proportions
    fat_props = {
        'saturated': 0,
        'unsaturated': 0
    }
    for fat, value in fats.items():
        if fat in saturated_fats:
            fat_props['saturated'] += value
        else:
            fat_props['unsaturated'] += value
    
    return properties, fats, fat_props, recipe_details


def create_other_ingredients_table(other_ingredients_data, other_ingredient_columns):
    """Create DataTable for other ingredients"""
    other_ingredients_filtered_data = [row for row in other_ingredients_data if any(row.values())]
    other_df = pd.DataFrame(other_ingredients_filtered_data)
    
    return dash_table.DataTable(
        columns=other_ingredient_columns,
        data=other_df.to_dict('records'),
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', "white-space": "pre-wrap"},
        style_cell={'textAlign': 'center', 'padding': '8px', "white-space": "pre-wrap"},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )


def create_additives_details(additives_data, pcsf_oil_data, total_oil_weight):
    """
    Create additives details dictionary with calculated weights
    
    Returns:
        dash_table.DataTable: Recipe additives table
    """
    # Extract additive values
    additives = {row['Additive']: convert_to_number(row['Value']) for row in additives_data}
    
    # Build additives details
    additives_details = {
        f'Lather: Sorbitol ({additives.get("Sorbitol (%TOW)", 0)}% TOW)': {
            'value': additives.get('Sorbitol (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Add to the lye solution, at trace, after the cook, or mixed with colorants.'
        },
        f'Lather: Citric Acid ({additives.get("Citric Acid (%TOW)", 0)}% TOW)': {
            'value': additives.get('Citric Acid (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Dissolve in the lye solution.'
        },
        f'Humectants: Sodium Chloride ({additives.get("Sodium Chloride (%TOW)", 0)}% TOW)': {
            'value': additives.get('Sodium Chloride (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Dissolve in the lye solution or add to oils.'
        },
        f'Trace Accelerants: Finished Soap ({additives.get("Finished Soap (%TOW)", 0)}% TOW)': {
            'value': additives.get('Finished Soap (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Melt with oils.'
        },
        f'Trace Accelerants: Eugenol ({additives.get("Eugenol (drops)", 0)} drops)': {
            'value': additives.get('Eugenol (drops)', 0), 
            'type': 'drops', 
            'directions': 'Add a few drops to heated oils.'
        },
        f'Humectants: Sodium Lactate ({additives.get("Sodium Lactate (%TOW)", 0)}% TOW)': {
            'value': additives.get('Sodium Lactate (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Add 30-60 seconds after mixing oils and lye solution, after a very thick trace, and before the expansion of the recipe.'
        },
        f'Lather: Cetyl Alcohol ({additives.get("Cetyl Alcohol (%TOW)", 0)}% TOW)': {
            'value': additives.get('Cetyl Alcohol (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Melted and added after trace.'
        },
        f'Lather: Honey ({additives.get("Honey (%TOW)", 0)}% TOW)': {
            'value': additives.get('Honey (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Add after the cook.'
        },
        f'Fluid Enhancer: Yogurt ({additives.get("Yogurt (%TOW)", 0)}% TOW)': {
            'value': additives.get('Yogurt (%TOW)', 0), 
            'type': 'TOW', 
            'directions': 'Add after the cook.'
        },
    }
    
    # Add PCSF oils
    for row in pcsf_oil_data:
        oil = row['PCSF Oil']
        tow = row['%TOW']
        additives_details[f'PCSF:{oil} ({tow} %TOW)'] = {
            'value': int(tow), 
            'type': 'TOW', 
            'directions': 'Add after the cook.'
        }
    
    # Conversion factor
    drops_to_grams = 1 / 30
    
    # Filter out additives with None or zero values
    filtered_additives = {k: v for k, v in additives_details.items() if v['value'] is not None and v['value'] > 0}
    
    # Convert to DataFrame
    recipe_additives_data = []
    for k, v in filtered_additives.items():
        if v['type'] == 'TOW':
            grams = round((v['value']/100) * total_oil_weight, 2)
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
    return dash_table.DataTable(
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


def create_overview_table(total_oil_weight, water_weight_grams, lye_type, lye_discount, 
                          lye_adjusted, fat_props):
    """Create overview data table"""
    overview_data = {
        "Total Oil Weight": f"{total_oil_weight}g",
        "Water as percent of oil weight": f"{round((water_weight_grams / total_oil_weight) * 100)}%",
        "Lye Type": lye_type,
        "Lye Discount": f"{round(lye_discount)}%",
        "Lye Concentration": f"{round((lye_adjusted / (water_weight_grams + lye_adjusted)) * 100, 1)}%",
        "Water : Lye Ratio": f"{water_weight_grams / lye_adjusted:.1f}:1",
        "Sat : Unsat Ratio": f"{round(fat_props['saturated']/(fat_props['saturated']+fat_props['unsaturated'])*100)}:{round(fat_props['unsaturated']/(fat_props['saturated']+fat_props['unsaturated'])*100)}",
        "": ""
    }
    
    transposed_data = [{"Prop": key, "Value": value} for key, value in overview_data.items()]
    transposed_columns = [
        {"name": "Prop", "id": "Prop"},
        {"name": "Value", "id": "Value"}
    ]
    
    return dash_table.DataTable(
        id='overview-table',
        columns=transposed_columns,
        data=transposed_data,
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px', 'text-size': '12px'},
    )


def create_oils_table(recipe_details):
    """Create oils data table"""
    columns = [
        {"name": "Oil", "id": "Oil"},
        {"name": "Grams", "id": "Grams"},
        {"name": "Ounces", "id": "Ounces"},
        {"name": "Percent", "id": "Percent"}
    ]
    
    return dash_table.DataTable(
        columns=columns,
        data=[{
            'Oil': item['Oil'],
            'Grams': f"{item['Grams']:.2f}",
            'Ounces': f"{item['Ounces']:.2f}",
            'Percent': f"{item['Percent']:.2f}"
        } for item in recipe_details],
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px', 'text-size': '12px'},
    )


def create_summary_table(total_oil_weight, water_weight_grams, water_weight_ounces, 
                        lye_weight_grams, lye_weight_ounces, total_weight, lye_type,
                        lye_adjusted_naoh=None, lye_adjusted_koh=None):
    """Create summary table with lye and water totals"""
    if lye_type == 'KOH_90':
        lye_type = 'KOH 90% purity'
    
    if lye_type == 'dual_lye':
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
    else:
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
    
    summary_df = pd.DataFrame(summary_data)
    
    return dash_table.DataTable(
        id='summary-table',
        columns=[{'name': col, 'id': col} for col in summary_df.columns],
        data=summary_df.to_dict('records'),
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px', 'text-size': '12px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )


def create_properties_table(properties, ranges):
    """Create properties table"""
    prop_data_df = pd.DataFrame({
        "Property": properties.keys(),
        "Range": ranges.values(),
        "Value": properties.values()
    })
    
    return dash_table.DataTable(
        id='properties-table',
        columns=[{'name': col, 'id': col} for col in prop_data_df.columns],
        data=prop_data_df.to_dict('records'),
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px', 'text-size': '12px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )


def create_fats_table(fats):
    """Create fats composition table"""
    fats_df = pd.DataFrame(list(fats.items()), columns=['Fat Type', 'Amount'])
    
    return dash_table.DataTable(
        id='fats-table',
        columns=[{'name': col, 'id': col} for col in fats_df.columns],
        data=fats_df.to_dict('records'),
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px', 'text-size': '12px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )

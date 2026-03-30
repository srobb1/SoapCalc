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


def calculate_other_ingredients(other_ingredients_data, total_oil_weight_grams):
    """
    Calculate other ingredients with fixed amounts and percentages
    
    Args:
        other_ingredients_data: List of ingredient dicts with Type, Amount, Unit, etc.
        total_oil_weight_grams: Total weight of oils in grams
    
    Returns:
        List of ingredient dicts with CalculatedAmount populated
    """
    results = []
    for ingredient in other_ingredients_data:
        # Skip empty rows
        if not ingredient.get('Ingredient'):
            continue
        
        ing_copy = ingredient.copy()
        
        if ing_copy.get('Type') == '%TOW':
            # Calculate amount as percentage of total oil weight
            amount_value = convert_to_number(ing_copy.get('Amount', 0))
            calculated = amount_value * (total_oil_weight_grams / 100)
            ing_copy['CalculatedAmount'] = f"{round(calculated, 2)} g"
        else:
            # Fixed amount - just use the amount as entered
            amount = ing_copy.get('Amount', '')
            unit = ing_copy.get('Unit', '')
            ing_copy['CalculatedAmount'] = f"{amount} {unit}".strip()
        
        results.append(ing_copy)
    
    return results


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
        cell_selectable=False,
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', "white-space": "pre-wrap"},
        style_cell={'textAlign': 'center', 'padding': '8px', "white-space": "pre-wrap"},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )


def create_additives_details(additives_data, pcsf_oil_data, total_oil_weight):
    """
    Create additives details dictionary with calculated weights
    Dynamically handles any additive with numeric values and proper directions
    
    Returns:
        dash_table.DataTable: Recipe additives table
    """
    # Mapping of additive names to their directions
    additive_directions = {
        'Sorbitol (1-5% TOW)': 'Add to lye, trace, after cook, or colorants',
        'Citric Acid (1-2% TOW)': 'Add to lye solution',
        'Sodium Chloride (0.5-1% TOW)': 'Dissolve in lye or add directly',
        'Finished Soap (0.05-1% TOW)': 'Grate and melt with oils',
        'Eugenol (drops)': 'Add drops to heated oil',
        'Sodium Lactate (3-4% TOW)': 'Add 30-60 sec after mixing oils/lye',
        'Cetyl Alcohol (1-3% TOW)': 'Add to oils at beginning',
        'Honey (1-5% TOW)': 'Heat-sensitive - add room temp or after cook',
        'Molasses (1-5% TOW)': 'Heat-sensitive - add room temp or after cook',
        'Yogurt (2-5% TOW)': 'Add after cook - room temperature or slightly warmed',
        'Milk - Dairy/Plant (2-5% TOW)': 'Add after cook - room temperature or slightly warmed',
        'Buttermilk (2-5% TOW)': 'Add after cook - room temperature or warmed',
        'Heavy Cream (2-5% TOW)': 'Add after cook - room temperature or warmed',
        'Goat Milk (2-5% TOW)': 'Add after cook - heat sensitive',
        'Almond Milk (2-5% TOW)': 'Add after cook - room temperature or warmed',
        'Coconut Yogurt (2-5% TOW)': 'Add after cook - room temperature or warmed',
        'Juice/Fruit Puree (2-5% TOW)': 'WARM before adding to HTHP after cook',
        'Tofu (2-5% TOW)': 'Add room temperature after cook',
    }
    
    # Conversion factor
    drops_to_grams = 1 / 30
    
    recipe_additives_data = []
    
    # Process all additives from the data table
    for row in additives_data:
        additive_name = row.get('Additive', '')
        value_str = str(row.get('Value', '')).strip()
        
        # Skip if no numeric value
        if not value_str or value_str in ['', 'Add to oil list', 'Grate and melt with oils', 'Add drops to heated oil', 'See LyeType']:
            continue
        
        # Try to convert value to number
        try:
            value = float(value_str)
        except ValueError:
            continue
        
        if value <= 0:
            continue
        
        # Determine the type and calculate grams
        if 'drops' in additive_name.lower():
            unit_type = 'drops'
            grams = value * drops_to_grams
            weight_display = f"{value:.0f} drops"
        elif '%TOW' in additive_name:
            unit_type = 'TOW'
            grams = round((value/100) * total_oil_weight, 2)
            weight_display = f"{grams:.2f}g"
        else:
            # Default to TOW if not specified
            unit_type = 'TOW'
            grams = round((value/100) * total_oil_weight, 2)
            weight_display = f"{grams:.2f}g"
        
        ounces = grams / 28.3495
        ounces_display = f"{ounces:.2f}oz"
        
        # Get directions from mapping or use default
        directions = additive_directions.get(additive_name, 'Add as directed')
        
        # Create section label (try to extract from additive name)
        section = ''
        if any(x in additive_name for x in ['Stearic', 'Lauric', 'Myristic', 'Finished Soap', 'Eugenol']):
            section = 'Trace Accelerants: '
        elif any(x in additive_name for x in ['Sodium Lactate', 'Sodium Chloride']):
            section = 'Humectants: '
        elif any(x in additive_name for x in ['Sorbitol', 'Cetyl', 'Citric Acid', 'Honey', 'Molasses']):
            section = 'Lather: '
        elif any(x in additive_name for x in ['Yogurt', 'Milk', 'Buttermilk', 'Cream', 'Juice', 'Tofu']):
            section = 'Fluid Enhancer: '
        elif any(x in additive_name for x in ['Molasses']):
            section = 'Soap Solvent: '
        
        recipe_additives_data.append({
            'Additive': f'{section}{additive_name}',
            'grams': weight_display,
            'ounces': ounces_display,
            'directions': directions
        })
    
    # Add PCSF oils
    for row in pcsf_oil_data:
        oil = row['PCSF Oil']
        tow = row['%TOW']
        try:
            tow_val = float(tow)
            if tow_val > 0:
                grams = round((tow_val/100) * total_oil_weight, 2)
                ounces = grams / 28.3495
                recipe_additives_data.append({
                    'Additive': f'PCSF: {oil}',
                    'grams': f"{grams:.2f}g",
                    'ounces': f"{ounces:.2f}oz",
                    'directions': 'Add after the cook.'
                })
        except (ValueError, TypeError):
            pass
    
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
        cell_selectable=False,
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
        cell_selectable=False,
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontSize': '12px'},
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
        cell_selectable=False,
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontSize': '12px'},
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
        cell_selectable=False,
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px', 'fontSize': '12px'},
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
        cell_selectable=False,
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px', 'fontSize': '12px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )


def create_fats_table(fats):
    """Create fats composition table"""
    fats_df = pd.DataFrame(list(fats.items()), columns=['Fat Type', 'Amount'])
    
    return dash_table.DataTable(
        id='fats-table',
        columns=[{'name': col, 'id': col} for col in fats_df.columns],
        data=fats_df.to_dict('records'),
        cell_selectable=False,
        style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px', 'fontSize': '12px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )


def create_htfhp_instructions(additives_data):
    """Create High Temperature Hot Process soap making instructions"""
    
    instructions = [
        html.H5("🔥 HTFHP Instructions", style={'marginTop': '8px', 'marginBottom': '6px', 'fontSize': '13px'}),
        html.Div([
            html.Ol([
                html.Li("Heat oils to 215°F. Add lye solution and blend continuously (3-5 min).", style={'fontSize': '11px', 'marginBottom': '2px'}),
                html.Li("Watch for trace → expansion → gel stage (looks like baby food).", style={'fontSize': '11px', 'marginBottom': '2px'}),
                html.Li("If expansion rises, stir down and resume mixing. Cover 2-3 min to finish.", style={'fontSize': '11px', 'marginBottom': '2px'}),
            ], style={'lineHeight': '1.4', 'marginBottom': '4px'})
        ]),
    ]
    
    # Add additive timing if additives are present
    additive_notes = []
    post_cook_additives = []
    
    if additives_data:
        # Handle both list of dicts (from form) and dict (from callback)
        items = additives_data.items() if isinstance(additives_data, dict) else additives_data
        
        for item in items:
            if isinstance(additives_data, dict):
                additive_name, value = item
            else:
                # List of dicts from DataTable
                additive_name = item.get('Category') or item.get('Additive', '')
                value = convert_to_number(item.get('Amount', 0))
            
            if isinstance(value, (int, float)) and value > 0:
                if 'Sodium Lactate' in additive_name:
                    additive_notes.append(f"• {additive_name}: Add at thick trace (before expansion begins)")
                elif any(x in additive_name for x in ['Sorbitol', 'Honey', 'Molasses', 'Sugar']):
                    additive_notes.append(f"• {additive_name}: Mix into lye solution before combining with oils")
                elif any(x in additive_name for x in ['Yogurt', 'Milk', 'Cream', 'Goat', 'Juice', 'Tofu']):
                    post_cook_additives.append(additive_name)
    
        if post_cook_additives:
            additive_notes.append(f"• {', '.join(post_cook_additives)}: Add after saponification is complete (post-cook). Use warmed or room-temperature additive and blend gently with spatula.")
        
        if additive_notes:
            instructions.append(
                html.Div([
                    html.Strong("Additive Timing:", style={'fontSize': '12px'}),
                    html.Ul([html.Li(note, style={'fontSize': '12px'}) for note in additive_notes], 
                            style={'marginTop': '4px', 'marginBottom': '0px'})
                ], style={'marginTop': '8px'})
            )
    
    instructions.extend([
        html.Div([
            html.Strong("Post-Cook Steps:", style={'fontSize': '12px'}),
            html.Ul([
                html.Li("Test pH with zap test or pH solution to confirm saponification is complete.", style={'fontSize': '12px'}),
                html.Li("Add warmed post-cook superfat, blend gently, cover for 1-2 minutes.", style={'fontSize': '12px'}),
                html.Li("Add fragrance oil and mix thoroughly.", style={'fontSize': '12px'}),
                html.Li("Divide into containers and add colorants/other room-temperature additives. Use warm tools if needed for mixing.", style={'fontSize': '12px'}),
            ], style={'marginTop': '4px', 'marginBottom': '0px'})
        ], style={'marginTop': '8px'}),
        html.Div([
            html.Strong("Molding & Setting:", style={'fontSize': '12px'}),
            html.Ul([
                html.Li("Fill mold and tap firmly on counter to remove air pockets. Cover and place in freezer or refrigerator for several hours if possible.", style={'fontSize': '12px'}),
                html.Li("Cutting time varies by recipe: pure coconut oil recipes (~30 min), others up to 24 hours.", style={'fontSize': '12px'}),
                html.Li("Soap is fully saponified and ready to use immediately after unmolding. Cure 4-6 weeks for harder bars.", style={'fontSize': '12px'}),
            ], style={'marginTop': '4px', 'marginBottom': '0px'})
        ], style={'marginTop': '8px'})
    ])
    
    return html.Div(instructions, style={
        'border': '1px solid #ddd', 
        'padding': '10px', 
        'backgroundColor': '#f9f9f9',
        'borderRadius': '4px',
        'fontSize': '12px'
    })

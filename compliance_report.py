"""
HTFHP Recipe Compliance Report Generator
Checks recipe against 11 HTFHP criteria from The Ultimate Guide to Hot Process Soap
"""
import pandas as pd
from dash import dash_table, html
import dash_bootstrap_components as dbc
from recipe_calculator import convert_to_number
from additives_data import pcsf_oils


def create_compliance_report(selected_oils_data, total_oil_weight, water_weight, total_weight, 
                            saturated_fat, additives_data, pcsf_oil_data, oil_prop_df):
    """
    Create HTFHP recipe compliance report checking against 11 criteria
    
    Args:
        selected_oils_data: List of selected oils with properties
        total_oil_weight: Total weight of oils in grams
        water_weight: Total water weight in grams
        total_weight: Total recipe weight (oils + water + lye)
        saturated_fat: Saturated fat percentage
        additives_data: Additives table data
        pcsf_oil_data: Post-cook superfat oils data
        oil_prop_df: Oil properties dataframe
    
    Returns:
        html.Div with compliance table and explanations
    """
    
    compliance_results = []
    
    # 1. Water 36-40% of oil weight (NOT total weight)
    water_to_oil_percent = (water_weight / total_oil_weight) * 100 if total_oil_weight > 0 else 0
    water_pass = 36 <= water_to_oil_percent <= 40
    compliance_results.append({
        'Criterion': '1. Water 36-40%',
        'Status': '✓' if water_pass else '✗',
        'Actual': f'{water_to_oil_percent:.1f}%',
        'Expected': '36-40%',
        'Pass': water_pass
    })
    
    # 2. Cleansing oils (cleansing >= 40) = 10-20% TOW
    cleansing_oils = [row for row in selected_oils_data 
                     if oil_prop_df.loc[row['Oil'], 'Cleansing'] >= 40]
    cleansing_tow = sum(convert_to_number(row.get('Grams', 0)) for row in cleansing_oils)
    cleansing_percent = (cleansing_tow / total_oil_weight) * 100 if total_oil_weight > 0 else 0
    cleansing_pass = 10 <= cleansing_percent <= 20
    compliance_results.append({
        'Criterion': '2. Cleansing Oils (≥40) 10-20%',
        'Status': '✓' if cleansing_pass else '✗',
        'Actual': f'{cleansing_percent:.1f}%',
        'Expected': '10-20%',
        'Pass': cleansing_pass
    })
    
    # 3. Castor oil = 10-15% TOW
    castor_oils = [row for row in selected_oils_data if 'castor' in row['Oil'].lower()]
    castor_tow = sum(convert_to_number(row.get('Grams', 0)) for row in castor_oils)
    castor_percent = (castor_tow / total_oil_weight) * 100 if total_oil_weight > 0 else 0
    castor_pass = 10 <= castor_percent <= 15 if castor_tow > 0 else False
    compliance_results.append({
        'Criterion': '3. Castor Oil 10-15%',
        'Status': '✓' if castor_pass else '✗',
        'Actual': f'{castor_percent:.1f}%',
        'Expected': '10-15%',
        'Pass': castor_pass
    })
    
    # 4. Condition oils (condition >= 80) = 15-30% TOW
    condition_oils = [row for row in selected_oils_data 
                     if oil_prop_df.loc[row['Oil'], 'Condition'] >= 80]
    condition_tow = sum(convert_to_number(row.get('Grams', 0)) for row in condition_oils)
    condition_percent = (condition_tow / total_oil_weight) * 100 if total_oil_weight > 0 else 0
    condition_pass = 15 <= condition_percent <= 30
    compliance_results.append({
        'Criterion': '4. Condition Oils (≥80) 15-30%',
        'Status': '✓' if condition_pass else '✗',
        'Actual': f'{condition_percent:.1f}%',
        'Expected': '15-30%',
        'Pass': condition_pass
    })
    
    # 5. Hardness oils (hardness >= 40) = 45-60% TOW
    hardness_oils = [row for row in selected_oils_data 
                    if oil_prop_df.loc[row['Oil'], 'Hardness'] >= 40]
    hardness_tow = sum(convert_to_number(row.get('Grams', 0)) for row in hardness_oils)
    hardness_percent = (hardness_tow / total_oil_weight) * 100 if total_oil_weight > 0 else 0
    hardness_pass = 45 <= hardness_percent <= 60
    compliance_results.append({
        'Criterion': '5. Hardness Oils (≥40) 45-60%',
        'Status': '✓' if hardness_pass else '✗',
        'Actual': f'{hardness_percent:.1f}%',
        'Expected': '45-60%',
        'Pass': hardness_pass
    })
    
    # 6. Saturated fat = 40-60%
    saturated_pass = 40 <= saturated_fat <= 60
    compliance_results.append({
        'Criterion': '6. Saturated Fat 40-60%',
        'Status': '✓' if saturated_pass else '✗',
        'Actual': f'{saturated_fat:.1f}%',
        'Expected': '40-60%',
        'Pass': saturated_pass
    })
    
    # 7. Trace accelerant (stearic acid, soap, eugenol)
    trace_accelerants = ['stearic acid', 'soap', 'eugenol']
    
    # Check additives table - look in both Additive name and Value
    has_accelerant = any(
        any(acc.lower() in str(row.get('Additive', '')).lower() or acc.lower() in str(row.get('Value', '')).lower() for acc in trace_accelerants)
        for row in (additives_data or [])
        if row.get('Value') and str(row.get('Value')).strip() not in ['', 'Add to oil list', 'See LyeType', 'Dissolve in lye or add directly', 'Heat-sensitive - add room temp or after cook', 'Heat-sensitive - may cause caramelization', 'Add room temperature or slightly warmed', 'Add room temperature or warmed', 'WARM before adding to HTHP', 'Add room temperature', 'Add to oils at beginning', 'Add to lye solution', 'Grate and melt with oils', 'Add drops to heated oil']
    )
    
    # Also check if stearic acid is in recipe oils
    if not has_accelerant:
        has_accelerant = any(
            'stearic acid' in row.get('Oil', '').lower()
            for row in selected_oils_data
        )
    
    compliance_results.append({
        'Criterion': '7. Trace Accelerant',
        'Status': '✓' if has_accelerant else '✗',
        'Actual': '✓ Found' if has_accelerant else '✗ Missing',
        'Expected': 'Stearic Acid/Soap/Eugenol',
        'Pass': has_accelerant
    })
    
    # 8. PCSF oil in recipe at 1-3% TOC + 3-6% TOW PCSF
    pcsf_oil_names = [o.lower() for o in pcsf_oils]
    pcsf_in_recipe = any(
        oil.get('Oil', '').lower() in pcsf_oil_names
        for oil in selected_oils_data
    )
    pcsf_total = sum(convert_to_number(row.get('%TOW', 0)) for row in (pcsf_oil_data or []))
    pcsf_pass = pcsf_in_recipe and 3 <= pcsf_total <= 6
    compliance_results.append({
        'Criterion': '8. PCSF Oil (1-3% TOC, 3-6% TOW)',
        'Status': '✓' if pcsf_pass else '✗',
        'Actual': f'{pcsf_total:.1f}% PCSF' if pcsf_oil_data else 'None',
        'Expected': '3-6% TOW',
        'Pass': pcsf_pass
    })
    
    # 9. Salt (3-4% SL Sodium Lactate or 0.5-1% NaCl Sodium Chloride)
    salt_value = None
    for row in (additives_data or []):
        additive_name = str(row.get('Additive', '')).lower()
        if 'sodium lactate' in additive_name or 'sodium chloride' in additive_name or 'salt' in additive_name:
            salt_value = convert_to_number(row.get('Value', 0))
            if salt_value > 0:
                break
    has_salt = salt_value is not None and salt_value > 0
    salt_pass = (0.5 <= salt_value <= 4) if has_salt else False
    compliance_results.append({
        'Criterion': '9. Salt (3-4% SL or 0.5-1% NaCl)',
        'Status': '✓' if salt_pass else '✗',
        'Actual': f'{salt_value}%' if has_salt else '✗ Missing',
        'Expected': '0.5-4%',
        'Pass': salt_pass
    })
    
    # 10. Sugar (1-5% TOW) - includes sugar, honey, sorbitol, molasses
    sugar_value = None
    for row in (additives_data or []):
        additive_name = str(row.get('Additive', '')).lower()
        if 'sugar' in additive_name or 'honey' in additive_name or 'sorbitol' in additive_name or 'molasses' in additive_name:
            sugar_value = convert_to_number(row.get('Value', 0))
            if sugar_value > 0:
                break
    has_sugar = sugar_value is not None and sugar_value > 0
    sugar_pass = (1 <= sugar_value <= 5) if has_sugar else False
    compliance_results.append({
        'Criterion': '10. Sugar (1-5% TOW)',
        'Status': '✓' if sugar_pass else '✗',
        'Actual': f'{sugar_value}%' if has_sugar else '✗ Missing',
        'Expected': '1-5%',
        'Pass': sugar_pass
    })
    
    # 11. Liquid additives (2-5% TOW) - check for any Fluid Enhancer category
    liquid_value = None
    for row in (additives_data or []):
        if row.get('section') == 'Fluid Enhancer':
            liquid_value = convert_to_number(row.get('Value', 0))
            if liquid_value and liquid_value > 0:
                break
    has_liquid = liquid_value is not None and liquid_value > 0
    liquid_pass = (2 <= liquid_value <= 5) if has_liquid else False
    compliance_results.append({
        'Criterion': '11. Liquid Additives (2-5% TOW)',
        'Status': '✓' if liquid_pass else '✗',
        'Actual': f'{liquid_value}%' if has_liquid else '✗ Missing',
        'Expected': '2-5%',
        'Pass': liquid_pass
    })
    
    # Create compliance dataframe
    compliance_df = pd.DataFrame(compliance_results)
    
    # Split results into two parts (6 items, then 5 items)
    left_results = compliance_results[:6]      # 1-6
    right_results = compliance_results[6:]     # 7-11
    
    # Create table with conditional styling
    pass_count = sum(1 for r in compliance_results if r['Pass'])
    pass_percent = (pass_count / len(compliance_results)) * 100
    
    # Helper function to create compliance table
    def create_compliance_table(data, table_id):
        return dash_table.DataTable(
            id=table_id,
            columns=[
                {'name': 'Criterion', 'id': 'Criterion'},
                {'name': 'Status', 'id': 'Status'},
                {'name': 'Actual', 'id': 'Actual'},
                {'name': 'Expected', 'id': 'Expected'},
            ],
            data=[
                {
                    'Criterion': r['Criterion'],
                    'Status': r['Status'],
                    'Actual': r['Actual'],
                    'Expected': r['Expected'],
                }
                for r in data
            ],
            cell_selectable=False,
            style_table={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse', 'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px', 'fontSize': '13px'},
            style_header={'backgroundColor': '#fafafa', 'fontWeight': 'bold', 'paddingLeft': '10px', 'fontSize': '13px'},
            style_data_conditional=[
                {
                    'if': {'column_id': 'Status', 'filter_query': '{Status} contains "✓"'},
                    'backgroundColor': '#d4edda',
                    'color': '#155724',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'column_id': 'Status', 'filter_query': '{Status} contains "✗"'},
                    'backgroundColor': '#f8d7da',
                    'color': '#721c24',
                    'fontWeight': 'bold'
                },
            ]
        )
    
    return html.Div([
        html.H5("HTFHP Compliance", style={'marginTop': '3px', 'marginBottom': '2px', 'fontWeight': 'bold', 'fontSize': '11px'}),
        html.Div(f"✓ {pass_count}/{len(compliance_results)} criteria met ({pass_percent:.0f}%)", 
                style={'marginBottom': '3px', 'fontSize': '9px', 'fontWeight': 'bold',
                       'color': 'green' if pass_count == len(compliance_results) else 'orange'}),
        dbc.Row([
            dbc.Col([
                create_compliance_table(left_results, 'compliance-table-left')
            ], width=6, style={'paddingRight': '1px'}),
            dbc.Col([
                create_compliance_table(right_results, 'compliance-table-right')
            ], width=6, style={'paddingLeft': '1px'})
        ], style={'marginBottom': '6px'})
    ])

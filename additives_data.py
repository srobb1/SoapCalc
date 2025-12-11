"""
Additive data and configuration for HTFHP soap making
"""

# Initial data for the additives DataTable
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

# Define colors for each section
section_colors = {
    "Trace Accelerants": "#fcfce9",
    "Humectants and Hardeners": "#e9fcfc",
    "Lather": "#e9f2fc",
    "Fluid Enhancer":"#fce9e9"
}

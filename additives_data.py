"""
Additive data and configuration for HTFHP soap making
"""

# Initial data for the additives DataTable
htfhp_additive_rowData = [
    {"section": "Trace Accelerants", "Additive": "Stearic Acid (%TOW)", "Value": "Add to oil list at 5-8%"},
    {"section": "Trace Accelerants", 'Additive': 'Lauric Acid (%TOW)', 'Value': 'Add to oil list at 5-8%'},
    {"section": "Trace Accelerants", 'Additive': 'Myristic Acid (%TOW)', 'Value': 'Add to oil list at 5-8%'},
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
    {"section": "Fluid Enhancer", 'Additive': 'Yogurt (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Milk - Dairy or Plant (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Buttermilk (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Heavy Cream (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Goat Milk (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Almond Milk (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Coconut Yogurt (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Juice or Fruit Puree (%TOW)', 'Value': None},
    {"section": "Fluid Enhancer", 'Additive': 'Tofu (%TOW)', 'Value': None},
    {"section": "Soap Solvent", 'Additive': 'Glycerin (%TOW)', 'Value': None},
    {"section": "Soap Solvent", 'Additive': 'Molasses (%TOW)', 'Value': None},
]

# Define tooltips for each cell
htfhp_tooltips = [
    {"section": "Oil used to speed up trace", "Additive": "Stearic acid acts as a thicking agent and emulsion stabilizer. Saturated fatty acid that readily combines with lye, accelerating trace. Also hardens finished soap.", "Value": "5-8% TOW recommended"},
    {"section": "Trace accelerant (alternative to stearic)", "Additive": "Lauric acid is a saturated fatty acid that acts as both trace accelerant and emulsion stabilizer. Also adds lathering and cleansing properties to finished soap. Usually more expensive than stearic acid.", "Value": "5-8% TOW recommended"},
    {"section": "Trace accelerant (alternative to stearic)", "Additive": "Myristic acid is a saturated fatty acid that acts as both trace accelerant and emulsion stabilizer. Also adds lathering and cleansing properties to finished soap. Usually more expensive than stearic acid.", "Value": "5-8% TOW recommended"},
    {"section": "Additive used to speed up trace", "Additive": "Finished soap acts as an emulsion accelerant and surfactant. Grate and melt with oils. Alternative if you don't have stearic acid or prefer to avoid it.", "Value": "0.05-1.0% TOW recommended"},
    {"section": "Additive used to speed up trace", "Additive": "Clove oil, cinnamon oil, or products containing eugenol act as trace accelerants. Add a few drops to heated oil. Useful for recipes high in unsaturated fats.", "Value": "A few drops recommended"},
    {"section": "Section for humectants and hardeners", "Additive": "Sodium lactate is a humectant that binds water molecules, increasing fluidity and maintaining gel phase. Add 30-60 seconds after mixing oils and lye, after thick trace and before expansion. Can add additional 1% for softer recipes.", "Value": "3-4% TOW recommended"},
    {"section": "Section for humectants and hardeners", "Additive": "Sodium chloride (table salt) acts similar to sodium lactate. Can dissolve in lye solution at beginning or add directly. WARNING: Too high concentration may cause recipe to thicken.", "Value": "0.5-1% TOW recommended"},
    {"section": "Section for lather", "Additive": "Castor oil is high in ricinoleic acid which increases soap solubility, lather formation rate, and lather stability. Works well with lauric and myristic acids. Add to your recipe oil list for correct lye calculation.", "Value": "5-15% TOW recommended"},
    {"section": "Section for lather", "Additive": "Jojoba is actually a wax, not an oil. Generates soap and an alcohol when saponified. The alcohol adds stability and longevity to lather. Add to your recipe oil list for correct lye calculation.", "Value": "5-10% TOW recommended"},
    {"section": "Section for lather", "Additive": "A small amount of KOH (5%) helps increase rate of lather formation and stability. Excellent for castile soaps (high unsaturated fat recipes). Select Dual Lye in the lye type section above.", "Value": "See lye type"},
    {"section": "Section for lather", "Additive": "Sorbitol creates super sudsy and bubbly lather. Increases solubility of soap, rate of lather formation, and lather stability. Most powerful impact of all sugar sources. Can add to lye, at trace, after cook, or in colorants.", "Value": "1-5% TOW recommended"},
    {"section": "Section for lather", "Additive": "Cetyl alcohol acts similarly to Jojoba oil. The alcohol adds stability and longevity to lather. Natural byproduct of soap, acts as humectant and emollient.", "Value": "1-3% TOW recommended"},
    {"section": "Section for lather", "Additive": "Citric acid helps lather by chelating minerals. Useful for hard water areas. Can also lower pH slightly but not significantly neutralize lye.", "Value": "1-2% TOW recommended"},
    {"section": "Section for lather", "Additive": "Honey creates bubbly lather and has chelating effects. Heat-sensitive: oxidizes and can cause color change from tan to golden to brown when heated with proteins (in milk/yogurt).", "Value": "1-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Yogurt increases fluidity and has acidic nature. Acts as humectant. Easier to mix than pure water. Add room temperature or slightly warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Milk (dairy or plant-based) increases fluidity and binds water molecules. Easier to mix than pure water sources like juice. Add room temperature or slightly warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Buttermilk is thick and creamy, excellent for fluidity. One of the best high-water additives per PDF author's recommendation. Add room temperature or warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Heavy cream is thick and creamy, providing rich fluidity. One of the best high-water additives per PDF author. Add room temperature or warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Goat milk is heat-sensitive and can cause discoloration if added too hot. PDF recommends adding after cook to prevent browning from sugar oxidation. Use room temperature. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Almond milk provides fluidity with subtle properties. Vegan option. Add room temperature or warmed. For acidic version, mix with small amount of citric acid. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Coconut yogurt mixed with beet lactic acid or citric acid is a vegan option. Provides fluidity similar to yogurt with acidic properties. Add room temperature or warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Fruit juices and purees add fluidity with natural sugars. More concentrated water sources than milk. IMPORTANT: Warm before adding to HTHP recipes. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Tofu is a plant-based option for increasing fluidity. Provides texture and properties similar to yogurt. Add room temperature. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Soap solvent - NOT recommended for HP", "Additive": "Glycerin is a natural byproduct of soap that acts as humectant, emollient, and soap solvent. Increases lather formation rate and bubble longevity. WARNING: PDF author does NOT recommend glycerin for hot process soap, only for cold/melt & pour. Bridges oil-water gap.", "Value": "Varies - not recommended for HP"},
    {"section": "Soap solvent - sugar source", "Additive": "Molasses is a sugar source that increases lather (bubbly). Heat-sensitive: causes caramelization ranging from light tan to deep brown/near black depending on temperature and duration. Similar effect to honey. Can also add: maple syrup, corn syrup.", "Value": "1-5% TOW recommended"},
]

# Define colors for each section
section_colors = {
    "Trace Accelerants": "#fcfce9",
    "Humectants and Hardeners": "#e9fcfc",
    "Lather": "#e9f2fc",
    "Fluid Enhancer":"#fce9e9",
    "Soap Solvent":"#f5e9fc"
}

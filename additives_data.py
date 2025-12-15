"""
Additive data and configuration for HTFHP soap making
"""

# Initial data for the additives DataTable
htfhp_additive_rowData = [
    {"section": "Trace Accelerants", "Additive": "Stearic Acid (5-8% TOW)", "Value": "Add to oil list"},
    {"section": "Trace Accelerants", 'Additive': 'Lauric Acid (5-8% TOW)', 'Value': 'Add to oil list'},
    {"section": "Trace Accelerants", 'Additive': 'Myristic Acid (5-8% TOW)', 'Value': 'Add to oil list'},
    {'section': "Trace Accelerants", 'Additive': 'Finished Soap (0.05-1% TOW)', 'Value': 'Grate and melt with oils'},
    {'section': "Trace Accelerants", 'Additive': 'Eugenol (drops)', 'Value': 'Add drops to heated oil', 'Placeholder' : 'drops'},
    {"section": "Humectants and Hardeners", 'Additive': 'Sodium Lactate (3-4% TOW)', 'Value': 'Add 30-60 sec after mixing oils/lye'},
    {'section': "Humectants and Hardeners", 'Additive': 'Sodium Chloride (0.5-1% TOW)', 'Value': 'Dissolve in lye or add directly'},
    {"section": "Lather", 'Additive': 'Castor Oil (5-15% TOW)', 'Value': 'Add to oil list'},
    {'section': "Lather", 'Additive': 'Jojoba Oil (5-10% TOW)', 'Value': 'Add to oil list'},
    {'section': "Lather", 'Additive': 'Dual Lye (5% KOH)', 'Value': 'See LyeType'},
    {'section': "Lather", 'Additive': 'Sorbitol (1-5% TOW)', 'Value': 'Add to lye, trace, after cook, or colorants'},
    {'section': "Lather", 'Additive': 'Cetyl Alcohol (1-3% TOW)', 'Value': 'Add to oils at beginning'},
    {'section': "Lather", 'Additive': 'Citric Acid (1-2% TOW)', 'Value': 'Add to lye solution'},
    {'section': "Lather", 'Additive': 'Honey (1-5% TOW)', 'Value': 'Heat-sensitive - add room temp or after cook'},
    {"section": "Fluid Enhancer", 'Additive': 'Yogurt (2-5% TOW)', 'Value': 'Add room temperature or slightly warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Milk - Dairy/Plant (2-5% TOW)', 'Value': 'Add room temperature or slightly warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Buttermilk (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Heavy Cream (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Goat Milk (2-5% TOW)', 'Value': 'Add after cook - heat sensitive'},
    {"section": "Fluid Enhancer", 'Additive': 'Almond Milk (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Coconut Yogurt (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Juice/Fruit Puree (2-5% TOW)', 'Value': 'WARM before adding to HTHP'},
    {"section": "Fluid Enhancer", 'Additive': 'Tofu (2-5% TOW)', 'Value': 'Add room temperature'},
    {"section": "Soap Solvent", 'Additive': 'Molasses (1-5% TOW)', 'Value': 'Heat-sensitive - may cause caramelization'},
]

# Section descriptions explaining why each category is important
section_descriptions = {
    "Trace Accelerants": "INCREASES CHEMICAL REACTION RATE & EMULSIFICATION. Accelerates trace by increasing molecular contact speed. Essential for HTHP success with saturated or moderate-fat recipes. Acts as emulsion stabilizer for better glide and fluidity during cooking.",
    
    "Humectants and Hardeners": "INCREASES FLUIDITY & MAINTAINS GEL PHASE. Sodium lactate binds water molecules, making soap more fluid during cook. Maintains gel phase appearance. Creates denser, harder finished bar. Essential for even consistency throughout HTHP process.",
    
    "Lather": "IMPROVES BUBBLE FORMATION, STABILITY & LONGEVITY. Enhances soap's solubility so more soap dissolves in water = faster lather formation. Stabilizes bubbles so lather lasts longer. Creates super sudsy, voluminous lather that feels luxurious.",
    
    "Fluid Enhancer": "INCREASES FLUIDITY FOR EASIER WORKING. Binds water molecules in thicker, creamier form than plain water. Creates a fluid, pourable soap that's easy to work with, mix, and pour. Essential for beginners learning HTHP. Allows manipulation during cook without excessive mixing.",
    
    "Soap Solvent": "BRIDGES OIL-WATER GAP & ACCELERATES TRACE. Sugar and glycerin aggregate around soap molecules' hydrophilic heads, making them attract water molecules more. This speeds emulsification, reaction rate, and phase change. Increases lather formation rate and bubble stability."
}

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

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
    {'section': "Lather", 'Additive': 'Molasses (1-5% TOW)', 'Value': 'Heat-sensitive - may cause caramelization'},
    {"section": "Fluid Enhancer", 'Additive': 'Yogurt (2-5% TOW)', 'Value': 'Add room temperature or slightly warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Milk - Dairy/Plant (2-5% TOW)', 'Value': 'Add room temperature or slightly warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Buttermilk (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Heavy Cream (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Goat Milk (2-5% TOW)', 'Value': 'Add after cook - heat sensitive'},
    {"section": "Fluid Enhancer", 'Additive': 'Almond Milk (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Coconut Yogurt (2-5% TOW)', 'Value': 'Add room temperature or warmed'},
    {"section": "Fluid Enhancer", 'Additive': 'Juice/Fruit Puree (2-5% TOW)', 'Value': 'WARM before adding to HTHP'},
    {"section": "Fluid Enhancer", 'Additive': 'Tofu (2-5% TOW)', 'Value': 'Add room temperature'},
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
    {"section": "Oil used to speed up trace", "Additive": "A saturated fatty acid that promotes faster saponification and strengthens bar hardness. Helps create stable emulsions during hot process cooking.", "Value": "5-8% TOW recommended"},
    {"section": "Trace accelerant (alternative to stearic)", "Additive": "A saturated fatty acid that speeds saponification and stabilizes emulsions. Also contributes lathering and cleansing properties to finished bar. Generally pricier than stearic acid.", "Value": "5-8% TOW recommended"},
    {"section": "Trace accelerant (alternative to stearic)", "Additive": "A saturated fatty acid that promotes saponification and emulsion stability. Adds lathering and cleansing characteristics to the final product. More expensive option compared to stearic acid.", "Value": "5-8% TOW recommended"},
    {"section": "Additive used to speed up trace", "Additive": "A soap or essential oil component that accelerates saponification by acting as a surfactant. Melt with oils for use. Good alternative when you prefer to avoid stearic acids.", "Value": "0.05-1.0% TOW recommended"},
    {"section": "Additive used to speed up trace", "Additive": "Clove, cinnamon, or products with eugenol speed up trace reaction. Add to heated oils in small amounts. Particularly useful for recipes with high unsaturated fat content.", "Value": "A few drops recommended"},
    {"section": "Section for humectants and hardeners", "Additive": "A humectant that attracts and holds water molecules, making soap easier to work with during hot process. Creates gel phase consistency and produces denser, more durable finished bars. Use 30-60 seconds after oils and lye mixture begins blending.", "Value": "3-4% TOW recommended"},
    {"section": "Section for humectants and hardeners", "Additive": "A salt that works like sodium lactate to attract water. Can dissolve in lye at start or add separately. Note: Excessive amounts may cause thickening.", "Value": "0.5-1% TOW recommended"},
    {"section": "Section for lather", "Additive": "Contains ricinoleic acid, which improves soap's ability to dissolve and lather quickly. Bubbles last longer. Pairs well with saturated fatty acids in your recipe.", "Value": "5-15% TOW recommended"},
    {"section": "Section for lather", "Additive": "Not an oil but a liquid wax. When mixed with lye, produces both soap and an alcohol compound. This alcohol boosts bubble formation and longevity.", "Value": "5-10% TOW recommended"},
    {"section": "Section for lather", "Additive": "A small amount of potassium hydroxide encourages faster lather and better bubble stability. Excellent choice for recipes heavy in unsaturated oils. Select Dual Lye option above to use.", "Value": "See lye type"},
    {"section": "Section for lather", "Additive": "A sugar that dramatically boosts bubble formation and lather volume. Improves how readily soap molecules dissolve and stabilizes bubbles. Most effective sugar for lather. Can be added at various stages: lye, trace, after cooking, or with colors.", "Value": "1-5% TOW recommended"},
    {"section": "Section for lather", "Additive": "An alcohol-based additive that functions like jojoba oil. The alcohol component strengthens and extends bubble life. Natural byproduct of soap that moisturizes skin.", "Value": "1-3% TOW recommended"},
    {"section": "Section for lather", "Additive": "Captures hard water minerals (chelation), improving lather in mineral-rich water. Can slightly lower pH but won't neutralize lye significantly.", "Value": "1-2% TOW recommended"},
    {"section": "Section for lather", "Additive": "A natural sweetener that boosts bubble formation and has chelating properties. Color-sensitive when heat is applied—especially with proteins in dairy products, causing browning from light tan to deep brown.", "Value": "1-5% TOW recommended"},
    {"section": "Section for lather", "Additive": "A sugar source that increases bubble formation. Caramelizes under heat (light tan to dark brown depending on temperature). Works similarly to other sugars. Also used: maple syrup, corn syrup.", "Value": "1-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "A cultured dairy product that increases workability and has mild acidity. Binds water more effectively than plain water. Use cooled to room temperature or slightly warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Dairy or plant-based option that promotes fluidity and water absorption. More stable than juice-based liquids. Apply at room temperature or slightly warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "A thick, tangy dairy liquid excellent for fluidity and workability. Highly recommended option for improving soap texture. Use at room temperature or warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "A thick, rich dairy product providing excellent fluidity and smooth texture. High-quality option for improving soap workability. Apply at room temperature or warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "A dairy option sensitive to high temperatures—may discolor if overheated. Recommended to add after main cooking to prevent browning from heat reacting with milk proteins. Use cooled. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "A plant-based milk that promotes fluidity with subtle properties. Vegan alternative. Use at room temperature or warmed. Can add citric acid for mild acidity. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Vegan dairy alternative combined with acidifying agents (lactic or citric acid). Provides fluidity similar to yogurt with acidic benefits. Apply at room temperature or warmed. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "Natural fruit liquids and purees boost workability with added sugars for lather benefit. More concentrated than dairy liquids. Essential: Warm before adding to hot process recipes. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Section for fluid enhancers", "Additive": "A plant-based option for increasing workability. Offers texture and consistency similar to yogurt. Add at room temperature. NOTE: All fluid enhancers 2-5% TOW.", "Value": "2-5% TOW recommended"},
    {"section": "Lather - sugar source", "Additive": "A dark sugar that boosts bubbles and provides caramel color. Heat-sensitive: color ranges from light tan to dark brown depending on temperature. Similar effects to honey and other sugars. Alternatives: maple syrup, corn syrup.", "Value": "1-5% TOW recommended"},
]

# Define colors for each section
section_colors = {
    "Trace Accelerants": "#fcfce9",
    "Humectants and Hardeners": "#e9fcfc",
    "Lather": "#e9f2fc",
    "Fluid Enhancer":"#fce9e9",
    "Soap Solvent":"#f5e9fc"
}

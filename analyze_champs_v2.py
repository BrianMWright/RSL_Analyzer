import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# Read the champion data from a CSV file
df = pd.read_csv('champion_data.csv')

# Print the data types of the columns
print(df.dtypes)

# Convert the numeric columns to the appropriate data type
numeric_cols = ['HP', 'ATK', 'DEF', 'CritRate', 'CritDamage', 'SPD', 'ACC', 'RES']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Map the numeric Affinity values to their string representations
affinity_mapping = {1: 'Magic', 2: 'Force', 3: 'Spirit', 4: 'Void'}
df['Affinity'] = df['Affinity'].map(affinity_mapping)

# Calculate Effective Health Points (EHP)
df['EHP'] = df['HP'] * (1 + df['DEF'] / 100)

# Placeholder data for Buff and Debuff skills
# Replace with actual data as necessary
df['Buff_Skill_Cooldown'] = [3] * len(df)  # Example cooldown
df['Debuff_Skill_Cooldown'] = [4] * len(df)  # Example cooldown

# Calculate Buff and Debuff Application Rates
df['Buff_Application_Rate'] = 1 / df['Buff_Skill_Cooldown']
df['Debuff_Application_Rate'] = 1 / df['Debuff_Skill_Cooldown']

# Perform the other analyses
top_hp = df.nlargest(5, 'HP')[['Name', 'HP']]
affinity_distribution = df['Affinity'].value_counts()
correlation = df[numeric_cols + ['EHP']].corr()

# Define roles and corresponding weighted stats
roles = {
    'Tank': {'DEF': 0.5, 'HP': 0.5},
    'Damage Dealer': {'ATK': 0.5, 'CritRate': 0.25, 'CritDamage': 0.25},
    'Support': {'HP': 0.4, 'SPD': 0.4, 'ACC': 0.2},
    'Debuffer': {'ACC': 0.5, 'SPD': 0.3, 'HP': 0.2},
    'Healer': {'HP': 0.4, 'SPD': 0.4, 'RES': 0.2}
}

# Function to calculate a weighted score for each role
def calculate_role_score(row, weights):
    return sum(row[stat] * weight for stat, weight in weights.items())

# Calculate scores for each role and find the best champions
best_champions_by_role = {}
for role, weights in roles.items():
    df[f'{role}_Score'] = df.apply(calculate_role_score, weights=weights, axis=1)
    best_champions_by_role[role] = df.nlargest(5, f'{role}_Score')[['Name', f'{role}_Score']]

    # Debugging: Print the top 5 champions for each role
    print(f"Top 5 {role} Champions:")
    print(best_champions_by_role[role])
    print("\n")  # Add a new line for better readability

# Define the max level for each rank
max_levels = {
    1: 10,
    2: 20,
    3: 30,
    4: 40,
    5: 50,
    6: 60
}

# Filter champions by rank and max level
max_level_ranks = pd.DataFrame()
for rank, max_level in max_levels.items():
    rank_df = df[(df['Rank'] == rank) & (df['Level'] == max_level)]
    max_level_ranks = pd.concat([max_level_ranks, rank_df])

# Proceed with the rest of the analysis
# ...

# Break out how many champions are at each rank
rank_counts = max_level_ranks['Rank'].value_counts().sort_index()

# Save the analyses to a PDF file
pdf_path = 'champion_report_v4.pdf'
with PdfPages(pdf_path) as pdf:
    # Top 5 Champions by HP
    plt.figure(figsize=(12, 6))
    plt.barh(top_hp['Name'], top_hp['HP'], color='skyblue')
    plt.gca().invert_yaxis()
    for index, value in enumerate(top_hp['HP']):
        plt.text(value, index, str(value))
    plt.xlabel('HP')
    plt.title('Top 5 Champions by HP')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Affinity Distribution
    affinity_distribution.plot(kind='bar', figsize=(8, 6), color='skyblue')
    plt.title('Distribution of Champions by Affinity')
    plt.xlabel('Affinity')
    plt.ylabel('Number of Champions')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Correlation Heatmap
    plt.figure(figsize=(10, 8))
    plt.matshow(correlation, fignum=1)
    plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=90)
    plt.yticks(range(len(correlation.columns)), correlation.columns)
    plt.colorbar()
    plt.title('Correlation Between Key Stats', pad=20)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Best Champions by Role
    for role, data in best_champions_by_role.items():
        plt.figure(figsize=(8, 6))
        plt.barh(data['Name'], data[f'{role}_Score'], color='skyblue')
        plt.gca().invert_yaxis()
        for index, value in enumerate(data[f'{role}_Score']):
            plt.text(value, index, str(round(value, 2)))
        plt.xlabel(f'{role} Score')
        plt.title(f'Top 5 {role} Champions')
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    # Top 20 Speediest Champions
    top_speed = df.nlargest(20, 'SPD')[['Name', 'SPD']]
    plt.figure(figsize=(12, 6))
    plt.barh(top_speed['Name'], top_speed['SPD'], color='skyblue')
    plt.gca().invert_yaxis()
    for index, value in enumerate(top_speed['SPD']):
        plt.text(value, index, str(value))
    plt.xlabel('SPD')
    plt.title('Top 20 Speediest Champions')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Top 5 Champions by EHP
    top_ehp = df.nlargest(5, 'EHP')[['Name', 'EHP']]
    plt.figure(figsize=(12, 6))
    plt.barh(top_ehp['Name'], top_ehp['EHP'], color='skyblue')
    plt.gca().invert_yaxis()
    for index, value in enumerate(top_ehp['EHP']):
        plt.text(value, index, str(int(value)))
    plt.xlabel('EHP')
    plt.title('Top 5 Champions by EHP')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Top 5 Buff Appliers
    top_buff_appliers = df.nlargest(5, 'Buff_Application_Rate')[['Name', 'Buff_Application_Rate']]
    plt.figure(figsize=(12, 6))
    plt.barh(top_buff_appliers['Name'], top_buff_appliers['Buff_Application_Rate'], color='skyblue')
    plt.gca().invert_yaxis()
    for index, value in enumerate(top_buff_appliers['Buff_Application_Rate']):
        plt.text(value, index, f"{value:.2f}")
    plt.xlabel('Buff Application Rate')
    plt.title('Top 5 Buff Appliers')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Top 5 Debuff Appliers
    top_debuff_appliers = df.nlargest(5, 'Debuff_Application_Rate')[['Name', 'Debuff_Application_Rate']]
    plt.figure(figsize=(12, 6))
    plt.barh(top_debuff_appliers['Name'], top_debuff_appliers['Debuff_Application_Rate'], color='skyblue')
    plt.gca().invert_yaxis()
    for index, value in enumerate(top_debuff_appliers['Debuff_Application_Rate']):
        plt.text(value, index, f"{value:.2f}")
    plt.xlabel('Debuff Application Rate')
    plt.title('Top 5 Debuff Appliers')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Rank 5 and Below Champions at Max Level
    plt.figure(figsize=(12, 6))
    plt.barh(max_level_ranks['Name'], max_level_ranks['Rank'], color='skyblue')
    plt.gca().invert_yaxis()
    for index, value in enumerate(max_level_ranks['Rank']):
        plt.text(value, index, str(value))
    plt.xlabel('Rank')
    plt.title('Rank 5 and Below Champions at Max Level')
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    if not rank_counts.empty:
        # Number of Champions at Each Rank
        plt.figure(figsize=(8, 6))
        rank_counts.plot(kind='bar', color='skyblue')
        plt.title('Number of Champions at Each Rank (5 and below) at Max Level')
        plt.xlabel('Rank')
        plt.ylabel('Number of Champions')
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        # List of Champions at Each Rank
        for rank in rank_counts.index:
            champions_at_rank = max_level_ranks[max_level_ranks['Rank'] == rank]['Name']
            plt.figure(figsize=(8, 6))
            plt.barh(champions_at_rank, [rank] * len(champions_at_rank), color='skyblue')
            plt.gca().invert_yaxis()
            for index, name in enumerate(champions_at_rank):
                plt.text(rank, index, name)
            plt.xlabel('Rank')
            plt.title(f'Champions at Rank {rank} and Max Level')
            plt.tight_layout()
            pdf.savefig()
            plt.close()
    else:
        print("No champions found at Rank 5 or below at Max Level.")

print(f'Report saved to {pdf_path}')


import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# Read the champion data from a CSV file
df = pd.read_csv('champion_data.csv')

# Print the data types of the columns
print(df.dtypes)


# Convert the numeric columns to the appropriate data type
numeric_cols = ['HP', 'ATK', 'DEF', 'CritRate', 'CritDamage', 'SPD', 'ACC', 'RES']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

# Map the numeric Affinity values to their string representations
affinity_mapping = {1: 'Magic', 2: 'Force', 3: 'Spirit', 4: 'Void'}
df['Affinity'] = df['Affinity'].map(affinity_mapping)


# Perform the other analyses
top_hp = df.nlargest(5, 'HP')[['Name', 'HP']]
affinity_distribution = df['Affinity'].value_counts()
correlation = df[numeric_cols].corr()

# Save the analyses to a PDF file
pdf_path = 'champion_report.pdf'
with PdfPages(pdf_path) as pdf:
    # Top 5 Champions by HP
    plt.figure(figsize=(12, 6))
    plt.barh(top_hp['Name'], top_hp['HP'], color='skyblue')
    plt.xlabel('HP')
    plt.title('Top 5 Champions by HP')
    plt.tight_layout()
    pdf.savefig()
    plt.close()


    # Affinity Distribution
    affinity_distribution.plot(kind='bar', figsize=(8, 6))
    plt.title('Distribution of Champions by Affinity')
    plt.xlabel('Affinity')
    plt.ylabel('Number of Champions')
    pdf.savefig()
    plt.close()

    # Correlation Heatmap
    plt.figure(figsize=(10, 8))
    plt.matshow(correlation, fignum=1)
    plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=90)
    plt.yticks(range(len(correlation.columns)), correlation.columns)
    plt.colorbar()
    plt.title('Correlation Between Key Stats', pad=20)
    pdf.savefig()
    plt.close()

print(f'Report saved to {pdf_path}')

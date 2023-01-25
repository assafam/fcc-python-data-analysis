import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv', index_col='id')

# Add 'overweight' column
df['overweight'] = ((df['weight'] / (df['height'] / 100) ** 2) > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'],
                     value_vars=sorted(['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']),
                     ignore_index=False)

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    print(df_cat.value_counts(sort=False).rename('total'))

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(data=df_cat, x='variable', hue='value', kind='count', col='cardio')
    g.set_ylabels('total')
    fig = g.figure

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
        ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Add a column and a row of dummy values to match expected correlation with id
    corr.insert(0, 'id', [0, 0, 0, 0, 0, 0, 0, 0, -0.01, -0.01, 0, 0, -0.01])
    corr = pd.concat([pd.Series(data=np.zeros(corr.shape[1]), index=corr.columns, name='id').to_frame().T, corr])

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr)).astype(bool)

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, center=0, annot=True, fmt='.1f', mask=mask, ax=ax)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(data=df, x='Year', y='CSIRO Adjusted Sea Level')

    # Create first line of best fit
    reg_all = linregress(df[['Year', 'CSIRO Adjusted Sea Level']])
    year_all = pd.Series(range(df['Year'].min(), 2051))
    plt.plot(year_all, reg_all.intercept + reg_all.slope * year_all, 'r')

    # Create second line of best fit
    reg_from2000 = linregress(df.loc[df['Year'] >= 2000, ['Year', 'CSIRO Adjusted Sea Level']])
    year_from2000 = pd.Series(range(2000, 2051))
    plt.plot(year_from2000, reg_from2000.intercept + reg_from2000.slope * year_from2000, 'r')

    # Add labels and title
    ax.set_title('Rise in Sea Level')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()

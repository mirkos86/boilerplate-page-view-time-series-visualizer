import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import datetime

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean data
df = df[
    (df['value'] > df['value'].quantile(0.025)) &
    (df['value'] < df['value'].quantile(0.975))]

df.reset_index(drop=True, inplace=True)


def draw_line_plot():
    # We inizialize a new dataframe for each plot.
    # Here is the first one, for the line plot where, havign in mind the plot we aim at,
    # we extract the date from the timestamp in the date column:
    df_line = df.copy()
    df_line['date'] = pd.to_datetime(df_line['date']).dt.date

    # Draw line plot
    fig, axes = plt.subplots(figsize=(20, 5))
    axes.plot(df['date'], df['value'], color='red')

    tick_locations = [df_line['date'][40+i*180] for i in range(0, 7)]
    last_tick = tick_locations[-1] + datetime.timedelta(days=180)
    tick_locations = tick_locations+[last_tick]

    ticks = [d.strftime('%Y-%m') for d in tick_locations]
    axes.xaxis.set_ticks(ticks)

    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():

    # Let's create a copy of the dataframe to work on for the purpose of creating the bar plot
    df_bar = df.copy()

    # We must average the number of page views per month over the dataframe
    # So we create individual years and months columns
    df_bar['year'] = df_bar.loc[:, 'date'].str[0:4].astype(int)
    df_bar['month'] = df_bar.loc[:, 'date'].str[5:7].astype(int)

    # Now I turn df_bar into a more synthetic dataframe
    # by averaging the values of each distinct month and I round them up to integers
    df_bar_grouped = df_bar.groupby(['year', 'month'])[
        'value'].mean().reset_index()
    df_bar_grouped['value'] = df_bar_grouped['value'].astype(int)

    # Next we pivot the months to create a table on which the pandas `.plot()` method can act seamlessly
    df_bar_pivot = df_bar_grouped.pivot(
        index='year', columns='month', values='value')

    # Let me rename the months column
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                  7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    df_bar_pivot.rename(columns=month_dict, inplace=True)

    # Time to draw the actual bar plot
    fig, axes = plt.subplots(figsize=(20, 5))
    df_bar_pivot.plot(kind='bar', ax=axes)

    # Let's set up axes and legend
    axes.set_xlabel('Years')
    axes.set_ylabel('Average Page Views')
    axes.legend(title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['date'] = pd.to_datetime(df_box['date']).dt.date
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # Time to draw the actual bar plot
    fig, axes = plt.subplots(1, 2, figsize=(20, 5))

    # Group by year and create a box plot
    sns.boxplot(x='year', y='value', data=df_box, palette='Set3', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    plt.suptitle('')  # Suppress the automatic pandas-generated title
    #plt.show()

    # Group by month and create a box plot
    month_order = [datetime.date(2000, i, 1).strftime('%b')
                   for i in range(1, 13)]
    sns.boxplot(x='month', y='value', order=month_order,
                data=df_box, palette='Set3', ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    plt.suptitle('')  # Suppress the automatic pandas-generated title
    #plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_elo_rating(players, title):
    """Plot the elo rating evolution"""
    plt.figure(figsize=(12,6))
    for player, elos in players.items():
        plt.plot(elos, label=player)
    #sns.lineplot(x=elo_rating.index, y=elo_rating.values)
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title='Players')
    plt.show()

def plot_box_plot(df, fname):
    """Plot the elo rating evolution"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))
    
    ax1 = sns.boxplot(data=df, x='system', y='champ_wr', whis=10, ax=ax1)
    ax1 = sns.swarmplot(data=df, x='system', y='champ_wr', color=".25", ax=ax1)
    ax2 = sns.boxplot(data=df, x='system', y='match_wr', whis=10, ax=ax2)
    ax2 = sns.swarmplot(data=df, x='system', y='match_wr', color=".25", ax=ax2)
    
    plt.show()
    fig.savefig(
        f'../reports/figures/{fname}.png', dpi=300, bbox_inches="tight")

def plot_mu_matrix(df, fname):
    
    plt.subplots(figsize=(18,14))
    g = sns.heatmap(
        df,
        annot=True,
        center=0,
        cmap="Spectral",#PuOr_r
        cbar=False,
        linewidth=2,
        vmin=0, vmax=100
        #square=True
    )
    plt.title(
        "Matriz de Matchups (Predicción en base a TrueSkill)",
        loc="left",
    )
    g.figure.tight_layout()
    g.figure.savefig(
        f'../reports/figures/{fname}.png', dpi=300, bbox_inches="tight")

def plot_tournament_metric(df, metric, title):
    df_pivot = df.pivot_table(index='player',columns='system', values=metric, aggfunc='mean')
    plt.subplots(figsize=(5,5))
    g = sns.heatmap(
        df_pivot,
        annot=True,
        center=0,
        cmap="PuOr_r",
        cbar=False,
        linewidth=2,
        #square=True
    )
    plt.title(
        title,
        loc="left",
    )
    g.figure.tight_layout()
    g.figure.savefig(
        f'../reports/figures/{metric}.png', dpi=100, bbox_inches="tight")

def plot_tournament_metric_pivoted(df, metric, title):
    #df_pivot = df.pivot_table(index='player',columns='system', values=metric, aggfunc='mean')
    plt.subplots(figsize=(5,5))
    g = sns.heatmap(
        df,
        annot=True,
        center=0,
        cmap="PuOr_r",
        cbar=False,
        linewidth=2,
        #square=True
    )
    plt.title(
        title,
        loc="left",
    )
    g.figure.tight_layout()
    g.figure.savefig(
        f'../reports/figures/{metric}.png', dpi=100, bbox_inches="tight")


def plot_players_metric_pivoted(df, metric, title):
    #df_pivot = df.pivot_table(index='player',columns='system', values=metric, aggfunc='mean')
    plt.subplots(figsize=(3,4))
    g = sns.heatmap(
        df,
        annot=True,
        center=0,
        cmap="PuOr_r",
        cbar=False,
        linewidth=2,
        fmt='.2f'
        #square=True
    )
    plt.title(
        title,
        loc="left",
    )
    g.figure.tight_layout()
    g.figure.savefig(
        f'../reports/figures/{metric}.png', dpi=100, bbox_inches="tight")
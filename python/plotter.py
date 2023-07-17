import json
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import utils
import os


def build_dataframe():
    dataframe = []
    for file in utils.open_results():
        with open(file, 'r') as f:
            results = json.load(f)
            f.close()
        for key in results:
            for model in results[key]:
                for matrix in results[key][model]:
                    count = Counter(results[key][model][matrix]['m'])
                    dataframe.append({
                        'n': int(key),
                        'id': int(matrix),
                        'type': model,
                        'hearts': results[key][model][matrix]['hearts'],
                        'clubs': results[key][model][matrix]['clubs'],
                        'spades': results[key][model][matrix]['spades'],
                        'diamonds': results[key][model][matrix]['diamonds'],
                        'blocked': count[5],
                        'occupied': count[1] + count[2] + count[3] + count[4],
                        'execution_time': min(300.0, results[key][model][matrix]['execution_time']),
                        'score': results[key][model][matrix]['steps'][-1]['score'] if len(
                            results[key][model][matrix]['steps']) > 0 else 0
                    })
    dataframe = pd.DataFrame(dataframe)
    dataframe = dataframe.sort_values(by=["n", "id", "type"])
    dataframe.to_csv("dataframe.csv", index=False)
    return dataframe


def compute_fraction(df: pd.DataFrame):
    df['occupied_fraction'] = df['occupied'] / (df['n'] * df['n'])
    df['blocked_fraction'] = df['blocked'] / (df['n'] * df['n'])
    df['free_fraction'] = 1 - df['occupied_fraction'] - df['blocked_fraction']
    return df


def lineplt(df, model):
    sns.lineplot(x="id", y="execution_time", data=df[df['type'] == model], hue="n", palette="Set2")
    plt.title("Execution time for " + model)
    plt.savefig("img/execution_time_" + model + ".png")
    plt.clf()


def boxplt(df, model):
    sns.boxplot(x="n", y="execution_time", data=df[df['type'] == model], palette="Set2")
    plt.title("Execution time for " + model)
    plt.savefig("img/boxplot_" + model + ".png")
    plt.clf()


def correlation_plot(df: pd.DataFrame, model):
    df['non_free_fraction'] = df['occupied_fraction'] + df['blocked_fraction']
    corr = df[df['type'] == model][['execution_time', 'n', 'blocked', 'occupied', 'free_fraction', 'non_free_fraction']].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cbar=False)
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    plt.title("Correlation for " + model)
    plt.savefig("img/correlation_" + model + ".png")
    plt.clf()


def cmpplot(df: pd.DataFrame):
    g = sns.FacetGrid(df, col="n", hue="type", palette="Set2", col_wrap=3, sharey=False)
    g.map(sns.lineplot, "id", "execution_time")
    g.add_legend()
    plt.savefig("img/cmpplot.png")
    plt.clf()


def plot(df: pd.DataFrame):
    plt.figure(figsize=(8, 8))
    fig = plt.gcf()
    fig.set_dpi(800)
    sns.set_style("whitegrid")
    for model in df['type'].unique():
        lineplt(df, model)
        boxplt(df, model)
        correlation_plot(df, model)
    cmpplot(df)


if __name__ == '__main__':
    if os.path.isfile("dataframe.csv"):
        df = pd.read_csv("dataframe.csv")
    else:
        df = build_dataframe()
    df = compute_fraction(df)
    plot(df)



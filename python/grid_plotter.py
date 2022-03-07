import json
import os.path
import sys

import numpy as np
import math
import matplotlib.pyplot as pl

HEARTS_SYMBOL = u"\u2665"
CLUBS_SYMBOL = u"\u2663"
SPADES_SYMBOL = u"\u2660"
DIAMONDS_SYMBOL = u"\u2666"
BLOCKED_SYMBOL = u"\u2612"


def get_symbol(value: int):
    if value == 0:
        return ""
    elif value == 1:
        return HEARTS_SYMBOL
    elif value == 2:
        return CLUBS_SYMBOL
    elif value == 3:
        return SPADES_SYMBOL
    elif value == 4:
        return DIAMONDS_SYMBOL
    else:
        return BLOCKED_SYMBOL


def symbolize_matrix(matrix: np.ndarray):
    symbolized_matrix = np.empty(matrix.shape, dtype=str)
    for (x, y), value in np.ndenumerate(matrix):
        symbolized_matrix[x, y] = get_symbol(value)
    return symbolized_matrix


def build_steps_from_json(steps):
    steps_list = []
    for step in steps:
        steps_list.append(Step(step["step"], step["m"], step["score"]))
    return steps_list


def build_ndarray(matrix: list):
    n = int(math.sqrt(len(matrix)))
    return np.array(matrix).reshape(n, n)


def check_dir_existence(path: str):
    return os.path.isdir(path)


def gen_matrix_fig(matrix, hearts, clubs, spades, diamonds, path, score=None, execution_time=None):
    symbol_matrix = symbolize_matrix(matrix)
    fontSize = 7
    textSize = 0.0138 * fontSize
    colWidths = [0.2] * n
    tableHeight = 0.225 * n
    horizontalPadding = (1.5 - 0.2 * n) / 2
    pl.figure(figsize=(1.5, 2.5), dpi=200)
    pl.table(
        cellText=symbol_matrix,
        colWidths=colWidths,
        bbox=[horizontalPadding / 1.5, (2.5 - tableHeight) / 2.5, 0.2 * n / 1.5, tableHeight / 2.5],
        cellLoc='center'
    )
    ax = pl.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    pl.text(0.05, 0.5 - textSize / 2.5, "Available", fontsize=fontSize)
    pl.text(
        0.05,
        0.5 - textSize * 2 / 2.5 - 0.015,
        "#" + HEARTS_SYMBOL + "=" + str(hearts - np.count_nonzero(matrix == 1)),
        fontsize=fontSize
    )
    pl.text(
        0.05,
        0.5 - textSize * 3 / 2.5 - 0.045,
        "#" + CLUBS_SYMBOL + "=" + str(clubs - np.count_nonzero(matrix == 2)),
        fontsize=fontSize
    )
    pl.text(
        0.05,
        0.5 - textSize * 4 / 2.5 - 0.075,
        "#" + SPADES_SYMBOL + "=" + str(spades - np.count_nonzero(matrix == 3)),
        fontsize=fontSize
    )
    pl.text(
        0.05,
        0.5 - textSize * 5 / 2.5 - 0.105,
        "#" + DIAMONDS_SYMBOL + "=" + str(diamonds - np.count_nonzero(matrix == 4)),
        fontsize=fontSize
    )
    pl.text(0.55, 0.5 - textSize / 2.5, "Total", fontsize=fontSize)
    pl.text(
        0.55,
        0.5 - textSize * 2 / 2.5 - 0.015,
        "#" + HEARTS_SYMBOL + "=" + str(hearts),
        fontsize=fontSize
    )
    pl.text(
        0.55,
        0.5 - textSize * 3 / 2.5 - 0.045,
        "#" + CLUBS_SYMBOL + "=" + str(clubs),
        fontsize=fontSize
    )
    pl.text(
        0.55,
        0.5 - textSize * 4 / 2.5 - 0.075,
        "#" + SPADES_SYMBOL + "=" + str(spades),
        fontsize=fontSize
    )
    pl.text(
        0.55,
        0.5 - textSize * 5 / 2.5 - 0.105,
        "#" + DIAMONDS_SYMBOL + "=" + str(diamonds),
        fontsize=fontSize
    )
    if score is not None:
        if execution_time is not None:
            color = "red"
            fontweight = "bold"
        else:
            color = "black"
            fontweight = "normal"
        pl.text(
            0.05,
            0.1,
            "Score = " + str(score),
            fontsize=fontSize,
            fontweight=fontweight,
            color=color
        )
    if execution_time is not None:
        pl.text(
            0.05,
            0.1 - textSize/1.5,
            "Exec. time = " + str(execution_time),
            fontsize=fontSize
        )
    pl.savefig(path)
    pl.close()


class Result:
    def __init__(self, json_result):
        self.n = json_result["n"]
        self.hearts = json_result["hearts"]
        self.clubs = json_result["clubs"]
        self.spades = json_result["spades"]
        self.diamonds = json_result["diamonds"]
        self.start_matrix = build_ndarray(json_result["m"])
        self.steps = build_steps_from_json(json_result["steps"])
        self.exe_time = json_result["execution_time"]


class Step:
    def __init__(self, number: int, matrix: list, score: int):
        self.number = number
        self.matrix = build_ndarray(matrix)
        self.score = score


if __name__ == '__main__':
    file = "../results/" + sys.argv[1]
    with open(file, 'r') as f:
        results = json.load(f)
        f.close()
    for key in results:
        n = int(key)
        for i in range(1, 21):
            mzn_result = Result(results[key]["mzn"][str(i)])
            asp_result = Result(results[key]["asp"][str(i)])

            current_mzn_dir = "../minizinc/results/size_" + str(n) + "/" + str(i)
            if not check_dir_existence(current_mzn_dir):
                os.makedirs(current_mzn_dir)

            gen_matrix_fig(
                mzn_result.start_matrix,
                mzn_result.hearts,
                mzn_result.clubs,
                mzn_result.spades,
                mzn_result.diamonds,
                current_mzn_dir + "/start.png"
            )
            for count, step in enumerate(mzn_result.steps):
                if count == len(mzn_result.steps) - 1:
                    gen_matrix_fig(
                        step.matrix,
                        mzn_result.hearts,
                        mzn_result.clubs,
                        mzn_result.spades,
                        mzn_result.diamonds,
                        current_mzn_dir + "/step_" + str(step.number) + ".png",
                        step.score,
                        mzn_result.exe_time
                    )
                else:
                    gen_matrix_fig(
                        step.matrix,
                        mzn_result.hearts,
                        mzn_result.clubs,
                        mzn_result.spades,
                        mzn_result.diamonds,
                        current_mzn_dir + "/step_" + str(step.number) + ".png",
                        step.score
                    )

            current_asp_dir = "../asp/results/size_" + str(n) + "/" + str(i)
            if not check_dir_existence(current_asp_dir):
                os.makedirs(current_asp_dir)

            gen_matrix_fig(
                asp_result.start_matrix,
                asp_result.hearts,
                asp_result.clubs,
                asp_result.spades,
                asp_result.diamonds,
                current_asp_dir + "/start.png"
            )
            for count, step in enumerate(asp_result.steps):
                if count == len(asp_result.steps) - 1:
                    gen_matrix_fig(
                        step.matrix,
                        asp_result.hearts,
                        asp_result.clubs,
                        asp_result.spades,
                        asp_result.diamonds,
                        current_asp_dir + "/step_" + str(step.number) + ".png",
                        step.score,
                        asp_result.exe_time
                    )
                else:
                    gen_matrix_fig(
                        step.matrix,
                        asp_result.hearts,
                        asp_result.clubs,
                        asp_result.spades,
                        asp_result.diamonds,
                        current_asp_dir + "/step_" + str(step.number) + ".png",
                        step.score
                    )

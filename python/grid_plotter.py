import json
import os.path
import sys
import chime
import tqdm
import numpy as np
import matplotlib.pyplot as pl
import utils

MIN_TABLE_HEIGHT = 2.5


def check_dir_existence(path: str):
    return os.path.isdir(path)


def gen_matrix_fig(matrix, hearts, clubs, spades, diamonds, path, colors, score=None, execution_time=None):
    matrix_size = matrix.shape[0]
    plotHeight = max(MIN_TABLE_HEIGHT, matrix_size * 0.5)
    symbol_matrix = utils.symbolize_matrix(matrix)
    fontSize = 7
    textSize = 0.0138 * fontSize
    colWidths = [0.2] * matrix_size
    tableHeight = 0.225 * matrix_size
    horizontalPadding = (1.5 - 0.2 * matrix_size) / 2
    pl.figure(figsize=(1.5, plotHeight), dpi=200)
    pl.table(
        cellText=symbol_matrix,
        colWidths=colWidths,
        bbox=[
            horizontalPadding / 1.5,
            (plotHeight - tableHeight) / plotHeight,
            0.2 * matrix_size / 1.5,
            tableHeight / plotHeight
        ],
        cellLoc='center',
        cellColours=colors
    )
    ax = pl.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    pl.text(0.05, 0.5 - textSize / plotHeight, "Available", fontsize=fontSize)
    pl.text(
        0.05,
        0.5 - textSize * 2 / plotHeight - 0.015,
        "#" + utils.HEARTS_SYMBOL + "=" + str(hearts - np.count_nonzero(matrix == 1)),
        fontsize=fontSize
    )
    pl.text(
        0.05,
        0.5 - textSize * 3 / plotHeight - 0.045,
        "#" + utils.CLUBS_SYMBOL + "=" + str(clubs - np.count_nonzero(matrix == 2)),
        fontsize=fontSize
    )
    pl.text(
        0.05,
        0.5 - textSize * 4 / plotHeight - 0.075,
        "#" + utils.SPADES_SYMBOL + "=" + str(spades - np.count_nonzero(matrix == 3)),
        fontsize=fontSize
    )
    pl.text(
        0.05,
        0.5 - textSize * 5 / plotHeight - 0.105,
        "#" + utils.DIAMONDS_SYMBOL + "=" + str(diamonds - np.count_nonzero(matrix == 4)),
        fontsize=fontSize
    )
    pl.text(0.55, 0.5 - textSize / plotHeight, "Total", fontsize=fontSize)
    pl.text(
        0.55,
        0.5 - textSize * 2 / plotHeight - 0.015,
        "#" + utils.HEARTS_SYMBOL + "=" + str(hearts),
        fontsize=fontSize
    )
    pl.text(
        0.55,
        0.5 - textSize * 3 / plotHeight - 0.045,
        "#" + utils.CLUBS_SYMBOL + "=" + str(clubs),
        fontsize=fontSize
    )
    pl.text(
        0.55,
        0.5 - textSize * 4 / plotHeight - 0.075,
        "#" + utils.SPADES_SYMBOL + "=" + str(spades),
        fontsize=fontSize
    )
    pl.text(
        0.55,
        0.5 - textSize * 5 / plotHeight - 0.105,
        "#" + utils.DIAMONDS_SYMBOL + "=" + str(diamonds),
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
            0.025,
            0.1,
            "Score = " + str(score),
            fontsize=fontSize,
            fontweight=fontweight,
            color=color
        )
    if execution_time is not None:
        pl.text(
            0.025,
            0.1 - textSize/1.5,
            "Exec. time = " + str(execution_time),
            fontsize=fontSize
        )
    pl.savefig(path)
    pl.close()


def gen_matrix_plot(mat_size: int, step_num: int, is_mzn: bool, result: utils.Result):
    if is_mzn:
        current_dir = "../minizinc/results/size_" + str(mat_size) + "/" + str(step_num)
    else:
        current_dir = "../asp/results/size_" + str(mat_size) + "/" + str(step_num)

    if not check_dir_existence(current_dir):
        os.makedirs(current_dir)

    colors_matrix = []
    for row in result.start_matrix:
        row_colors = []
        for col in row:
            if col == 0:
                row_colors.append("w")
            elif col == 5:
                row_colors.append("#ff5733")
            else:
                row_colors.append("#ffc300")
        colors_matrix.append(row_colors)

    gen_matrix_fig(
        result.start_matrix,
        result.hearts,
        result.clubs,
        result.spades,
        result.diamonds,
        current_dir + "/start.png",
        colors_matrix
    )

    for count, step in enumerate(result.steps):
        if count == len(result.steps) - 1:
            gen_matrix_fig(
                step.matrix,
                result.hearts,
                result.clubs,
                result.spades,
                result.diamonds,
                current_dir + "/step_" + str(step.number) + ".png",
                colors_matrix,
                step.score,
                result.exe_time
            )
        else:
            gen_matrix_fig(
                step.matrix,
                result.hearts,
                result.clubs,
                result.spades,
                result.diamonds,
                current_dir + "/step_" + str(step.number) + ".png",
                colors_matrix,
                step.score
            )


if __name__ == '__main__':
    for arg in range(1, len(sys.argv)):
        file = sys.argv[arg]
        with open(file, 'r') as f:
            results = json.load(f)
            f.close()
        for key in results:
            n = int(key)
            print("Working on size " + str(n) + "...")
            matrix_pbar = tqdm.tqdm(range(1, 21))
            for i in matrix_pbar:
                mzn_result = utils.Result(results[key]["mzn"][str(i)])
                asp_result = utils.Result(results[key]["asp"][str(i)])

                gen_matrix_plot(n, i, True, mzn_result)
                gen_matrix_plot(n, i, False, asp_result)

                matrix_pbar.set_description("Processing matrix # %d" % i)

    chime.theme("big-sur")
    chime.success()

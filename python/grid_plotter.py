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
    plot_height = 1.4 + 0.2 * matrix_size
    plot_width = 1.44 + 0.02 * matrix_size
    symbol_matrix = utils.symbolize_matrix(matrix)
    font_size = 7
    text_size = 0.0138 * font_size
    pl.figure(figsize=(plot_width, plot_height), dpi=600)
    pl.table(
        cellText=symbol_matrix,
        loc='best',
        cellLoc='center',
        cellColours=colors,

    )
    ax = pl.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    pl.axis("off")
    pl.text(0.05, 0.5 - text_size / plot_height - matrix_size * 0.02, "Available", fontsize=font_size)
    pl.text(
        0.05,
        0.5 - text_size * 2 / plot_height - 0.015 - matrix_size * 0.02,
        "#" + utils.HEARTS_SYMBOL + "=" + str(hearts - np.count_nonzero(matrix == 1)),
        fontsize=font_size
    )
    pl.text(
        0.05,
        0.5 - text_size * 3 / plot_height - 0.045 - matrix_size * 0.02,
        "#" + utils.CLUBS_SYMBOL + "=" + str(clubs - np.count_nonzero(matrix == 2)),
        fontsize=font_size
    )
    pl.text(
        0.05,
        0.5 - text_size * 4 / plot_height - 0.075 - matrix_size * 0.02,
        "#" + utils.SPADES_SYMBOL + "=" + str(spades - np.count_nonzero(matrix == 3)),
        fontsize=font_size
    )
    pl.text(
        0.05,
        0.5 - text_size * 5 / plot_height - 0.105 - matrix_size * 0.02,
        "#" + utils.DIAMONDS_SYMBOL + "=" + str(diamonds - np.count_nonzero(matrix == 4)),
        fontsize=font_size
    )
    pl.text(0.55, 0.5 - text_size / plot_height - matrix_size * 0.02, "Total", fontsize=font_size)
    pl.text(
        0.55,
        0.5 - text_size * 2 / plot_height - 0.015 - matrix_size * 0.02,
        "#" + utils.HEARTS_SYMBOL + "=" + str(hearts),
        fontsize=font_size
    )
    pl.text(
        0.55,
        0.5 - text_size * 3 / plot_height - 0.045 - matrix_size * 0.02,
        "#" + utils.CLUBS_SYMBOL + "=" + str(clubs),
        fontsize=font_size
    )
    pl.text(
        0.55,
        0.5 - text_size * 4 / plot_height - 0.075 - matrix_size * 0.02,
        "#" + utils.SPADES_SYMBOL + "=" + str(spades),
        fontsize=font_size
    )
    pl.text(
        0.55,
        0.5 - text_size * 5 / plot_height - 0.105 - matrix_size * 0.02,
        "#" + utils.DIAMONDS_SYMBOL + "=" + str(diamonds),
        fontsize=font_size
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
            0.5 - text_size * 5 / plot_height - 0.155 - matrix_size * 0.02,
            "Score = " + str(score),
            fontsize=font_size,
            fontweight=fontweight,
            color=color
        )
    if execution_time is not None:
        pl.text(
            0.025,
            0.5 - text_size * 5 / plot_height - 0.205 - matrix_size * 0.02,
            "Exec. time = " + str(execution_time),
            fontsize=font_size
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
    for file in utils.open_results():
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

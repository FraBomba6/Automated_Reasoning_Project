import numpy as np
import math
import tkinter as tk
from tkinter import filedialog


def open_results():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilenames(initialdir='../results', filetypes=[("JSON files", "*.json")])


HEARTS_SYMBOL = u"\u2661"
CLUBS_SYMBOL = u"\u2663"
SPADES_SYMBOL = u"\u2660"
DIAMONDS_SYMBOL = u"\u2662"
BLOCKED_SYMBOL = u"\u2610"


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

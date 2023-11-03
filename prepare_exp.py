#!/usr/bin/env python
# -*- coding: utf8 -*

import random
import numpy as np
from psychopy import visual
import copy

stim_text = {'CZERWONY': 'red', 'NIEBIESKI': '#5e75d9', 'BRAZOWY': '#574400', 'ZIELONY': 'green'}  # text: color
#stim_neutral = "HHHHHHHH"
stim_distractor_adjective = ['WYSOKA', 'UKRYTA', u'GŁĘBOKA', 'DALEKA']
stim_distractor_color = ['RÓŻOWY', 'BORDOWY', 'ZŁOCISTY', 'KREMOWY']

colors_text = list(stim_text.keys())
random.shuffle(colors_text)
colors_names = [stim_text[color] for color in colors_text]
left_hand = colors_text[:2]
right_hand = colors_text[2:]

last_text = None
last_text_2 = None
last_color = None


def prepare_trial(trial_type, win, text_height, words_dist):
    global last_color, last_text, last_text_2
    text = None
    stim_distr = None

    if trial_type == 'neu_neu':
        possible_text = stim_distractor_adjective[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text)
        words = [text, text]
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

    elif trial_type == 'neu1_neu2':
        possible_text = stim_distractor_adjective[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text, 2, replace=False)
        words = [text[0], text[1]]
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

    elif trial_type == 'col_col':
        possible_text = stim_distractor_color[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text)
        words = [text, text]
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

    elif trial_type == 'col1_col2':
        possible_text = stim_distractor_color[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text, 2, replace=False)
        words = [text[0], text[1]]
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

    else:
        raise Exception('Wrong trigger type')

    random.shuffle(words)
    last_color = color
    last_text = text if len(text) == 2 else [text]
    last_text_2 = stim_distr

    print({'trial_type': trial_type, 'text': words, 'color': color})

    stim1 = visual.TextStim(win, color=color, text=words[0], height=text_height, pos=(0, words_dist/2))
    stim2 = visual.TextStim(win, color=color, text=words[1], height=text_height, pos=(0, -words_dist/2))
    return {'trial_type': trial_type, 'text': words, 'color': color, 'stim': [stim1, stim2]}


def prepare_part(trials_col_col, trials_col1_col2, trials_neu_neu, trials_neu1_neu2, win, text_height, words_dist):
    trials = ['col_col'] * trials_col_col + \
             ['col1_col2'] * trials_col1_col2 + \
             ['neu_neu'] * trials_neu_neu + \
             ['neu1_neu2'] * trials_neu1_neu2
    random.shuffle(trials)
    return [prepare_trial(trial_type, win, text_height, words_dist) for trial_type in trials]


def prepare_exp(data, win, text_size, words_dist):
    text_height = 1.5 * text_size
    training1_trials = prepare_part(data['Training1_trials_col_col'],
                                    data['Training1_trials_col1_col2'],
                                    data['Training1_trials_neu_neu'],
                                    data['Training1_trials_neu1_neu2'], win, text_height, words_dist)

    training2_trials = prepare_part(data['Training2_trials_col_col'],
                                    data['Training2_trials_col1_col2'],
                                    data['Training2_trials_neu_neu'],
                                    data['Training2_trials_neu1_neu2'],  win, text_height, words_dist)

    experiment_trials = prepare_part(data['Experiment_trials_col_col'],
                                    data['Experiment_trials_col1_col2'],
                                    data['Experiment_trials_neu_neu'],
                                    data['Experiment_trials_neu1_neu2'],  win, text_height, words_dist)

    return [training1_trials, training2_trials], experiment_trials, colors_text, colors_names

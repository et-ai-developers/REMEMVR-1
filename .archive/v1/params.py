# params.py

# 0.0 = 00
# 0.1 = 1A
# 0.2 = 33
# 0.3 = 4D
# 0.4 = 66
# 0.5 = 80
# 0.6 = 99
# 0.7 = B3
# 0.8 = CC
# 0.9 = E6
# 1.0 = FF

# blue = '#3333cc'
# red = '#cc3333'
# green = '#33cc33'
# black = '#000000'

# orange = '#cc6633'
# cyan = '#33cccc'
# magenta = '#cc33cc'

blue    = '#1f77b4'
orange  = '#ff7f0e'
green   = '#2ca02c'
red     = '#d62728'
purple  = '#9467bd'
brown   = '#8c564b'
pink    = '#e377c2'
grey    = '#7f7f7f'
mustard = '#bcbd22'
cyan    = '#17becf'
black   = '#000000'

COLORS_TQ = [
    blue,
    orange,
    green,
    brown
]
COLORS_TC = [
    red,
    purple,
    cyan,
    grey
]

PLOTS_SCORES = {
        'ctt_regression': {
            'title': 'CTT Trajectories Over Time',
            'x_axis': {
                'label': 'Days Since Encoding',
                'range': [0, 6],
                'tick_gap': 1,
            },
            'y_axis': {
                'label': 'Mean Score',
                'range': [0, 1],
                'tick_gap': 1,
            },
            'legend': {
                'show': True,
                'location': 'upper right',
                'title': None,
                'fontsize': 'small',
                'framealpha': 0.8,  # Transparency of the legend frame
            },
            'output': {
                'show': True,  # Show the plot interactively
                'save': True,  # Save the plot to disk
                'dpi': 300,  # DPI for saved plots
                'filename': 'ctt.png',
            }
        }, 
        'item_difficulty': {
            'title': 'Item Difficulty Distribution',
            'clip': [],
            'x_axis': {
                'label': 'Item Difficulty (b)',
                'range': [],
                'tick_gap': None,
            },
            'y_axis': {
                'label': 'Frequency',
                'range': [],
                'tick_gap': None,
            },
            'legend': {
                'show': True,
                'location': 'upper right',
                'title': None,
                'fontsize': 'small',
                'framealpha': 0.8,  # Transparency of the legend frame
            },
            'output': {
                'show': True,  # Show the plot interactively
                'save': True,  # Save the plot to disk
                'dpi': 300,  # DPI for saved plots
                'filename': 'item_difficulty.png',
            }
        },

        'lmm_diagnostics': {
            'title': 'Diagnostic Plots for LMM',
            'colors': [
                '#1f77b4',  # Blue
                '#ff7f0e',  # Orange
                '#2ca02c',  # Green
                '#d62728',  # Red
                '#9467bd',  # Purple
                '#8c564b',  # Brown
            ],
            'output': {
                'show': True,  # Show the plot interactively
                'save': True,  # Save the plot to disk
                'dpi': 300,  # DPI for saved plots
                'filename': 'diagnostics.png'
            }
        },

        'lmm_trajectory': {
            'title': 'LMM Trajectories Over Time',
            'x_axis': {
                'label': 'Days Since Encoding',
                'range': [0, 6],
                'tick_gap': 1,
            },
            'y_axis': {
                'label': 'Predicted Score Ability (θ)',
                'range': [-1, 1],
                'tick_gap': 1,
            },
            'legend': {
                'show': True,
                'location': 'upper right',
                'title': None,
                'fontsize': 'small',
                'framealpha': 0.8,  # Transparency of the legend frame
            },
            'output': {
                'show': True,  # Show the plot interactively
                'save': True,  # Save the plot to disk
                'dpi': 300,  # DPI for saved plots
                'filename': 'ability.png',
            }
        },

        'predicted_probabilities': {
            'title': 'Predicted Probability of Correct Response over Time',
            'x_axis': {
                'label': 'Days Since Encoding',
                'range': [0, 6],
                'tick_gap': 1,
            },
            'y_axis': {
                'label': 'Probability of Correct Response',
                'range': [0, 1],
                'tick_gap': 0.2,
            },
            'legend': {
                'show': True,
                'location': 'upper right',
                'title': None,
                'fontsize': 'small',
                'framealpha': 0.8,  # Transparency of the legend frame
            },
            'output': {
                'show': True,  # Show the plot interactively
                'save': True,  # Save the plot to disk
                'dpi': 300,  # DPI for saved plots
                'filename': 'probability.png',
            }
        },

        'model_evolution': {
            'title': 'Model Evolution Over Passes',
            'x_axis': {
                'label': 'Days Since Encoding',
                'range': [0, 6],
                'tick_gap': 1,
            },
            'y_axis': {
                'label': 'Predicted Ability (θ)',
                'range': [-1, 1],
                'tick_gap': 1,
            },
            'legend': {
                'show': True,
                'location': 'upper right',
                'title': None,
                'fontsize': 'small',
                'framealpha': 0.8,  # Transparency of the legend frame
            },
            'output': {
                'show': True,  # Show the plot interactively
                'save': True,  # Save the plot to disk
                'dpi': 300,  # DPI for saved plots
                'filename': 'model_evolution.png',
            }
        },
} 

PLOTS_CONFIDENCE = {
    'ctt_regression': {
        'title': 'CTT Trajectories Over Time',
        'x_axis': {
            'label': 'Days Since Encoding',
            'range': [0, 6],
            'tick_gap': 1,
        },
        'y_axis': {
            'label': 'Mean Confidence',
            'range': [0, 1],
            'tick_gap': 1,
        },
        'legend': {
            'show': True,
            'location': 'upper right',
            'title': None,
            'fontsize': 'small',
            'framealpha': 0.8,  # Transparency of the legend frame
        },
        'output': {
            'show': True,  # Show the plot interactively
            'save': True,  # Save the plot to disk
            'dpi': 300,  # DPI for saved plots
            'filename': 'ctt.png',
        }
    }, 
    'item_difficulty': {
        'title': 'Item Difficulty Distribution (Confidence Model)',
        'clip': [],
        'x_axis': {
            'label': 'Item Difficulty (b)',
            'range': [],
            'tick_gap': None,
        },
        'y_axis': {
            'label': 'Frequency',
            'range': [],
            'tick_gap': None,
        },
        'legend': {
            'show': True,
            'location': 'upper right',
            'title': None,
            'fontsize': 'small',
            'framealpha': 0.8,
        },
        'output': {
            'show': True,
            'save': True,
            'dpi': 300,
            'filename': 'item_difficulty.png',
        }
    },

    'lmm_diagnostics': {
        'title': 'Diagnostic Plots for Confidence LMM',
        'colors': [
            '#1f77b4', '#ff7f0e', '#2ca02c',
            '#d62728', '#9467bd', '#8c564b',
        ],
        'output': {
            'show': True,
            'save': True,
            'dpi': 300,
            'filename': 'diagnostics.png'
        }
    },

    'lmm_trajectory': {
        'title': 'LMM Trajectories of Confidence Over Time',
        'x_axis': {
            'label': 'Days Since Encoding',
            'range': [0, 6],
            'tick_gap': 1,
        },
        'y_axis': {
            'label': 'Predicted Confidence Ability (θ)',
            'range': [-1, 1],
            'tick_gap': 1,
        },
        'legend': {
            'show': True,
            'location': 'upper right',
            'title': None,
            'fontsize': 'small',
            'framealpha': 0.8,
        },
        'output': {
            'show': True,
            'save': True,
            'dpi': 300,
            'filename': 'ability.png',
        }
    },

    'predicted_probabilities': {
        'title': 'Predicted Probability of High Confidence Over Time',
        'x_axis': {
            'label': 'Days Since Encoding',
            'range': [0, 6],
            'tick_gap': 1,
        },
        'y_axis': {
            'label': 'Probability of High Confidence',
            'range': [0, 1],
            'tick_gap': 0.2,
        },
        'legend': {
            'show': True,
            'location': 'upper right',
            'title': None,
            'fontsize': 'small',
            'framealpha': 0.8,
        },
        'output': {
            'show': True,
            'save': True,
            'dpi': 300,
            'filename': 'probability.png',
        }
    },

    'model_evolution': {
        'title': 'Model Evolution Over Passes (Confidence)',
        'x_axis': {
            'label': 'Days Since Encoding',
            'range': [0, 6],
            'tick_gap': 1,
        },
        'y_axis': {
            'label': 'Predicted Confidence Ability (θ_conf)',
            'range': [-1, 1],
            'tick_gap': 1,
        },
        'legend': {
            'show': True,
            'location': 'upper right',
            'title': None,
            'fontsize': 'small',
            'framealpha': 0.8,
        },
        'output': {
            'show': True,
            'save': True,
            'dpi': 300,
            'filename': 'model_evolution.png',
        }
    },
}

LINE_STYLES = {
    'ctt': 'solid',  # Solid line for CTT
    'lmm': 'dashed',  # Dashed line for LMM
    'prob': 'dotted',  # Dotted line for probabilities
}

ANALYSIS_LIST = [
    {
        "label": "All",
        "tag_types": ["TC", "TQ"],
        "correlated_factors": [False], # Redundant when there is only one group(factor)
        "specify_room": [False, True],
        "groups": {
            'All': ['RFR', 'IFR',  'TCR', 'ICR', 'RRE', 'IRE'],
        }
    },
    {
        "label": "All Items",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [False], # Redundant when there is only one group(factor)
        "specify_room": [False, True],
        "groups": {
            'All Items': ['IFR', 'ICR', 'IRE'],
        }
    },
    {
        "label": "All by Paradigm",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'All Free Recall': ['RFR', 'IFR'],
            'All Cued Recall': ['TCR', 'ICR'],
            'All Recognition': ['RRE', 'IRE'],
        }
    },
    {
        "label": "All by Domain",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'All What':     ['-N'],
            'All Where':    ['-L-', '-U-', '-D-'],
            'All When':     ['-O-'],   
        }
    },
    {
        "label": "Items by Paradigm",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'Items Free Recall': ['IFR'],
            'Items Cued Recall': ['ICR'],
            'Items Recognition': ['IRE'],    
        }
    },
    {
        "label": "Items by Domain",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'Items What':       ['IFR-N-', 'ICR-N-', 'IRE-N-'],
            'Items Where':      ['IFR-U-', 'ICR-U-', 'IRE-U-', 'IFR-D-', 'ICR-D-', 'IRE-D-'],
            'Items When':       ['IFR-O-', 'ICR-O-', 'IRE-O-'],
        }
    },
    {
        "label": "Items Up v Down",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'Items Pick Up':    ['IFR-U-', 'ICR-U-', 'IRE-U-'],
            'Items Put Down':   ['IFR-D-', 'ICR-D-', 'IRE-D-'],
        }
    },
    {
        "label": "Items by Congruence",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'Items Common':         ['-i1', '-i2'],
            'Items Congruent':      ['-i3', '-i4'],
            'Items Incongruent':    ['-i5', '-i6'],
        }
    },
    {
        "label": "Interaction vs Observation",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'Interaction':  ['IFR', 'ICR', 'IRE'],
            'Observation':  ['RFR', 'TCR', 'RRE'],
        }
    },
    {
        "label": "Portraits vs Landscapes",
        "tag_types": ["TQ", "TC"],
        "correlated_factors": [True, False],
        "specify_room": [False],
        "groups": {
            'Portraits':    ['-PORT'],
            'Landscapes':   ['-LAND'],
        }
    }
    # {
    #     "label": "Portraits vs Landscapes by Domain",
    #     "tag_types": ["TQ", "TC"],
    #     "correlated_factors": [True, False],
    #     "specify_room": [False],
    #     "groups": {
    #         'Portraits What':   ['-N-PORT'],
    #         'Landscapes What':  ['-N-LAND'],
    #         'Portraits Where':  ['-L-PORT'],
    #         'Landscapes Where': ['-L-LAND'],
    #     }
    # }
]

params_list = []

for analysis in ANALYSIS_LIST:

    for tag_type in analysis['tag_types']:

        if tag_type == 'TQ':

            categories_list = [
                {
                    0: [-1.00,  0.98],
                    1: [0.99,   2.00]
                },
                # Removed three categories because analysis sucked and there are confounds in guessing
                # {
                #     0: [-1.00,  0.48],
                #     1: [0.49,   0.98],
                #     2: [0.99,   2.00]
                # }
            ]

            plots = PLOTS_SCORES

        elif tag_type == 'TC':

            categories_list = [
                {
                    0: [0.1, 0.3],
                    1: [0.3, 0.5],
                    2: [0.5, 0.7],
                    3: [0.7, 0.9],
                    4: [0.9, 1.1]
                }
            ]

            plots = PLOTS_CONFIDENCE

        for correlated_factors in analysis['correlated_factors']:

            for specify_room in analysis['specify_room']:

                for categories in categories_list:

                    params_temp = {
                        'general': {
                            'save_folder': f'results/{analysis["label"]}',
                            'file_header': f'{tag_type}_{"corr" if correlated_factors else "uncorr"}_{"room" if specify_room else "noroom"}_{len(categories)}cats_',
                            'log_file': 'log.txt',
                        },
                        'px': {
                            'exclude': [],
                            'age_range': [0, 100]
                        },    
                        'data': {
                            'tests': [1, 2, 3, 4],
                            'all_tags_keys': [f'{tag_type}_'],
                            'all_tags': [],
                            'groups': analysis['groups'],
                            'line_styles': LINE_STYLES,
                            'colors': COLORS_TQ if tag_type == 'TQ' else COLORS_TC,
                            'categories': categories
                        },
                        'analysis': {
                            
                            'iterations': [
                                # {
                                #     "label": "low",
                                #     "model_fit": {
                                #         "batch_size": 32,
                                #         "iw_samples": 10,
                                #         "mc_samples": 1,
                                #     },
                                #     "model_scores" : {
                                #         'scoring_batch_size': 32,
                                #         'iw_samples': 10,
                                #         'mc_samples': 1,
                                #     },
                                #     'min_discrim_threshold': 0.5,
                                #     'max_discrim_threshold': 4.0,
                                # },
                                {
                                    "label": "med",
                                    "model_fit": {
                                        "batch_size": 2048,
                                        "iw_samples": 100,
                                        "mc_samples": 1,
                                    },
                                    "model_scores" : {
                                        'scoring_batch_size': 2048,
                                        'iw_samples': 100,
                                        'mc_samples': 100,
                                    },
                                    'min_discrim_threshold': 0.5,
                                    'max_discrim_threshold': 4.0,
                                },
                                # Removed high because it needs to be recomputed with the relaxed discrimination thresholds (0.25, 4.0)
                                # {
                                #     "label": "high",
                                #     "model_fit": {
                                #         "batch_size": 4096,
                                #         "iw_samples": 200,
                                #         "mc_samples": 1,
                                #     },
                                #     "model_scores" : {
                                #         'scoring_batch_size': 4096,
                                #         'iw_samples': 200,
                                #         'mc_samples': 200,
                                #     },
                                #     'min_discrim_threshold': 0,
                                #     'max_discrim_threshold': 10,
                                # }
                            ],

                            'lmm_reference_group': None,    # Reference group for LMM (None means no reference group)
                            'specify_room': specify_room,   # Whether to specify room in the analysis
                            'correlated_factors': correlated_factors,  # Whether to include correlated factors in the analysis
                        },
                        'plots': plots
                    }

                    params_list.append(params_temp)


""" Simple GUI for entering acquisition time metadata
 and a top level comment to satisfy interrogate coverage
"""

import PySimpleGUI as sg
# from aind_data_schema.imaging import instrument as inst
from aind_data_schema.imaging import acquisition as acq
# from aind_data_schema import data_description
from aind_data_schema.subject import Species
import datetime
from pathlib import Path
import json


default_instrument_file = Path(
    "D://SmartSPIM_Data/Calibrations/instrument.json"
)

species = [i.name for i in Species]

immersions = ['Cargille 1.522', 'Cargille 1.53', 'EasyIndex']

orientation_image_paths = {
    'regular': Path(__file__).parent.parent.parent.parent.joinpath(
        'img', 'reg_656346.png'
    ),
    'inverted': Path(__file__).parent.parent.parent.parent.joinpath(
        'img', 'inv_656346.png'
    )
}

orientation_image_subsample = 6

orientation_translator = {
    'regular': [
        acq.Direction("Superior_to_inferior"),
        acq.Direction("Posterior_to_anterior"),
        acq.Direction("Right_to_left")
    ],
    'inverted': [
        acq.Direction("Superior_to_inferior"),
        acq.Direction("Anterior_to_posterior"),
        acq.Direction("Left_to_right")
    ]
}


def make_acq_dict(values, orientation):
    """ Make a dictionary of acquisition related values """
    operator = values.get('-operator-', None)
    specimen_id = values.get('-subject_id-', None)
    instrument_id = values.get('-instrument-', None)
    chamber_immersion = acq.Immersion(
        medium=values.get('-chamber_immersion-', None),
        refractive_index=values.get('-ch_RI-', None)
    )
    sample_immsersion = acq.Immersion(
        medium=values.get('-sample_immersion-', None),
        refractive_index=values.get('-sa_RI-', None)
    )
    sample_orientation = orientation_translator[orientation]

    acq_dict = {
        "experimenter_full_name": operator,
        "specimen_id": specimen_id,
        "instrument_id": instrument_id,
        "chamber_immersion": chamber_immersion,
        "sample_immersion": sample_immsersion,
        "sample_orientation": sample_orientation
    }
    return acq_dict


def update_out_preview(window, data_dict={}, acq_dict={},):
    """ Show current values in preview
    """
    acq_dict = jsonify(acq_dict)
    text = json.dumps(acq_dict, indent=3)
    window['-preview-'].update(text)


def jsonify(obj_dict):
    """ Turn objects into serializable ones """
    result = {}
    for i, j in obj_dict.items():
        if hasattr(j, 'json'):
            result[i] = j.json(indent=3)
        elif i == 'sample_orientation':
            result[i] = [k.value for k in j]
        else:
            result[i] = j
    return result


def saveout_runplan(metadatas, folder):
    """ Save serialized calibrations to a JSON with datetime in name
    """
    data_dict = jsonify(metadatas[0])
    acq_dict = jsonify(metadatas[1])

    filename = f"somedumbfileprefix_\
        {acq_dict['specimen_id']}_\
        {datetime.datetime.now().strftime(format='%Y_%m_%d_%H_%M')}.json"
    if folder is None:
        # Handle "Cancel" button
        return
    elif not folder.exists():
        folder.mkdir(parents=True,)
    text_out = [data_dict, acq_dict]
    with open(folder.joinpath(filename), 'w') as file:
        json.dump(text_out, file, indent=3)


def update_orientation_choice(window, orientation):
    """ Update the orientation when a button is pressed """
    img = orientation_image_paths[orientation]
    window['-orientation_choice-'].update(
        filename=img,
        subsample=orientation_image_subsample
    )


def main():
    """ Launch the GUI """
    sg.theme('BluePurple')
    acq_dict = {}
    data_dict = {}
    orientation = 'regular'

    menu_def = [
        [
            'File', [
                'Load instrument config file',
                'Save runplan file',
                'Exit',
            ]
        ],
    ]

    layout = [
        [sg.Menu(menu_definition=menu_def)],

        # [sg.Button('Load default file')],

        [
            sg.Text("Operator full name:"),
            sg.Input(
                key='-operator-',
            ),
        ],
        [
            sg.Text("Specimen id:"),
            sg.Input(
                key="-specimen_id-"
            ),
        ],

        [
            sg.Text("Species:"),
            sg.Combo(
                species,
                default_value="MUS_MUSCULUS",
                key='-species-'
            )
        ],

        [
            sg.Text("Chamber immersion name and index"),
            sg.Combo(
                immersions,
                key='-chamber_immersion-'
            ),
            sg.Input(key='-ch_RI-')
        ],

        [
            sg.Text("Sample immersion name and index"),
            sg.Combo(
                immersions,
                key='-sample_immersion-'
            ),
            sg.Input(key='-sa_RI-')
        ],

        # [
        #    sg.Text('Project code:'),
        #    sg.Input(key='-project_code-'),
        # ],
        [
            sg.Text("Orientation choices:")
        ],
        [
            sg.Button(
                '',
                image_filename=orientation_image_paths['regular'],
                image_subsample=6,
                key='-orientation_regular-'
            ),
            sg.Button(
                '',
                image_filename=orientation_image_paths['inverted'],
                image_subsample=6,
                key='-orientation_inv-'
            ),
        ],
        [
            sg.Button('Add metadata'),
            sg.Button('Clear'),
            sg.Button('Save runplan file'),
            sg.Button('Exit')
        ],

        [
            sg.Text("Metadata Preview"),
            sg.Text(
                "Orientation Selected:",
                expand_x=True,
                justification='center'
            )
        ],
        [
            sg.Multiline(
                default_text="",
                size=(50, 25),
                key='-preview-',
                write_only=True,
            ),
            sg.Image(
                filename=orientation_image_paths[orientation],
                subsample=6,
                key='-orientation_choice-',
                expand_x=True,
            )
        ]
    ]

    window = sg.Window('SmartSPIM pre-flight', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Add metadata':
            acq_dict = make_acq_dict(values, orientation)
            update_out_preview(window, data_dict=data_dict, acq_dict=acq_dict,)
        elif event == '-orientation_regular-':
            orientation = 'regular'
            update_orientation_choice(window, orientation)
        elif event == '-orientation_inv-':
            orientation = 'inverted'
            update_orientation_choice(window, orientation)
        elif event == 'Clear':
            acq_dict = {}
            update_out_preview(window, data_dict, acq_dict)
        elif event == 'Save runplan file':
            folder = sg.popup_get_folder(
                "output folder",
                default_path="D://SmartSPIM_Data/Calibrations"
            )
            if folder is not None:
                folder = Path(folder)
                saveout_runplan([data_dict, acq_dict], folder)


if __name__ == "__main__":
    main()

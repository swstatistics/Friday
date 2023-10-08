from pathlib import Path
from typing import Final


# add the projectfolder as 
project_path = Path(__file__).parent.parent.parent.resolve()

# path to a specific Data set (since there is only one, this is a valid way to do it, usually there should be a file-manager)
data_path = project_path / Path('data/FRIDAY_Dataset.xlsx')

# path to the ruleset for the one-hot-encoding for thgis data
ruleset_path = project_path / 'src/pipelines/one_hot_encoder_rules.json'



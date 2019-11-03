from datetime import datetime
from typing import NewType, List, Dict, Union

Datetime = NewType("Datetime", datetime)
Diffs = NewType("Diffs", Dict[str, List[str]])
Stamps = NewType("Stamps", Dict[str, List[str]])

Config = NewType("Config", Dict[str, Union[str, List[str]]])
Shorthand = NewType("Shorthand", Dict[str, Union[str, str]])
ConfigBackup = NewType("ConfigBackup", Dict[str, Config])

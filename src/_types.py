import os
from typing import Union

# for type hint
StrOrBytesPath = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]

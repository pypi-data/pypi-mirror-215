from file_finder.utils import find_by_ext
from file_finder.utils import find_by_name
from file_finder.utils import find_by_mod


# fmt: off
SEARCH_MAPPING = {
    "name": find_by_name, 
    "ext": find_by_ext, 
    "mod": find_by_mod
}

# fmt: on
TABLE_HEADERS = ["Nome", "Criação", "Modificação", "Localização"]

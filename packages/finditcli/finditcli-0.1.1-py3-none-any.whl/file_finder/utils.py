from datetime import datetime
import platform
from file_finder.exceptions import InvalidInputError


def get_folders(path):
    """Obtém os subdiretórios no diretório pesquisado.

    Args:
        path (str): um objeto Path() que representa o diretório.

    Returns:
        list: Uma lista contendo os arquivos encontrados no diretório.
    """
    return [item for item in path.iterdir() if item.is_dir()]


def get_files(path):
    """Obtém os arquivos no diretório pesquisado.

    Args:
        path (str): O diretório a ser pesquisado.

    Returns:
        list: Uma lista contendo os arquivos encontrados no diretório.
    """
    return [item for item in path.iterdir() if item.is_file()]


def find_by_name(path, value):
    """Obtém todos os arquivos no diretório pesquisado que tenham um nome igual a `value` (independente da extensão.)

    Args:
        path (Path): Um objeto Path() que representa o diretório
        value (str): que representa o nome que os arquivos podem ter.

    Returns:
        list: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com um nome igual a `value`.
    """
    return [file for file in get_files(path) if file.stem == value]


def find_by_ext(path, value):
    """Obtém todos os arquivos no diretório pesquisado que tenham a extensão igual a `value` (independente do nome).

    Args:
        path (Path): Um objeto Path() que representa o diretório
        value (str): str que representa a ext. que os arquivos podem ter.

    Returns:
        list: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com uma extensão igual a `value`.
    """
    return [file for file in get_files(path) if file.suffix == value]


def find_by_mod(path, value):
    """Obtém todos os arquivos no diretório pesquisado que tenham uma data de modificação maior ou igual ao parametro informado.

    Args:
        path (Path): Um objeto Path() que representa o diretório
        value (str): str que representa a menor data de modificação que os
    arquivos podem ter.

    Returns:
        list: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com a data de modificação maior ou igual a `value`.
    """
    # input: dd/mm/aaaa
    try:
        datetime_obj = datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise InvalidInputError(f"{value} não é uma data válida no formato dd/mm/aaaa")

    return [
        file
        for file in get_files(path)
        if datetime.fromtimestamp(file.stat().st_mtime) >= datetime_obj
    ]


def timestamp_to_string(system_timestamp):
    datetime_obj = datetime.fromtimestamp(system_timestamp)
    return datetime_obj.strftime("%d/%m/%Y - %H:%M:%S:%f")


def get_files_details(files):
    """Obtém uma lista de listas contendo os detalhes dos arquivos representados em `files`.

    Args:
        files (files): uma lista de objetos Path() que representam os arquivos.

    Returns:
        list: uma lista de listas em que cada elemento será uma lista contendo: nome, data de criação, data de modificação e localização do arquivo em `files`.
    """
    files_details = []

    for file in files:
        stat = file.stat()
        details = [
            file.name,
            timestamp_to_string(get_created_timestamp(stat)),
            timestamp_to_string(stat.st_mtime),
            file.absolute(),
        ]
        files_details.append(details)
    return files_details


def get_created_timestamp(stat):
    if platform.system() == "Darwin":
        return stat.st_birthtime
    return stat.st_ctime

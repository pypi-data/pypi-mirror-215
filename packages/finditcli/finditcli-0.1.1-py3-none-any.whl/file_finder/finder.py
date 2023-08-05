import click
import shutil
from tabulate import tabulate
from pathlib import Path
from datetime import datetime
from file_finder.utils import get_folders
from file_finder.utils import get_files_details
from file_finder.constants import SEARCH_MAPPING
from file_finder.constants import TABLE_HEADERS
from file_finder.exceptions import FileFinderError
from file_finder.exceptions import InvalidInputError
from file_finder.exceptions import ZeroFilesFoundError


def process_search(path, key, value, recursive):
    """Detém toda lógica necessária para realizar a pesquisa
    conforme os inputs do usuário

    Args:
        path (_type_): Um objeto Path() que representa o diretório
        key (_type_): str que representa a chave de pesquisa.
        value (_type_): str que representa o nome que os arquivos podem ter.
        recursive (_type_): boolean que determina se a pesquisa deve percorrer
    os subdiretórios ou não.

    Returns:
        _type_: Uma lista de objetos Path(), cada um representando um arquivo encontrado pela pesquisa
    """
    files = SEARCH_MAPPING[key](path, value)

    if recursive:
        subdirs = get_folders(path)
        for subdir in subdirs:
            files += process_search(subdir, key, value, recursive)

    return files


def process_results(files, key, value):
    """Processa os resultados da pesquisa, exibindo-os na tela em formato
    de tabela.

    Args:
        files (_type_): Uma lista de objetos Path(), cada um representando um
     arquivo encontrado pela pesquisa
        key (_type_): str que representa a chave de pesquisa.
        value (_type_): str que representa o nome que os arquivos podem ter.

    Returns:
        _type_: A string que representa os resultados tabulados.
    """
    if not files:
        raise ZeroFilesFoundError(f"Nenhum arquivo com {key} {value} encontrado")

    table_data = get_files_details(files)
    tabulated_data = tabulate(table_data, headers=TABLE_HEADERS, tablefmt="pipe")
    click.echo(tabulated_data)

    return tabulated_data


def save_report(save, report, root):
    """Determina se o report deve ser ou nao salvo em um arquivo.
    Se sim, cria um arquivo no diretório 'root' com nome
    'finder_report_<timestamp>.txt' contendo os resultados em formato
    tabular.

    Args:
        save (_type_): boolean que diz se um arquivo com o report deve ser
    criado ou nao
        report (_type_): string que representa os resultados tabulados.
        root (_type_): Path() que aponta para o diretorio da pesquisa.
    """
    if save and report:
        report_file_path = (
            root / f"finder_report_{datetime.now().strftime('%d%m%Y%H%M%S%f')}.txt"
        )
        with open(report_file_path.absolute(), mode="w") as report_file:
            report_file.write(report)


def copy_files(copy_to, files):
    """Copia arquivos encontrados na pesquisa para um diretorio
    especifico.

    Args:
        copy_to (str): str que informa o nome do diretorio para onde
    os arquivos representados em 'files' devem ser copiados.
        files (list): uma lista de objetos Path() representando cada um
    dos arquivos encontrados na busca
    """
    if copy_to:
        copy_path = Path(copy_to)
        if not copy_path.is_dir():
            copy_path.mkdir(parents=True)

            # arquivos/encontrados/[...]
            for file in files:
                dst_file = copy_path / file.name

                if dst_file.is_file():
                    dst_file = (
                        copy_path
                        / f"{file.stem}{datetime.now().strftime('%d%m%Y%H%M%S%f')}{file.suffix}"
                    )
                shutil.copy(src=file.absolute(), dst=dst_file)


@click.command()
@click.argument("path", default="")
@click.option(
    "-k",
    "--key",
    required=True,
    type=click.Choice(SEARCH_MAPPING.keys()),
    help="Define a cave de pesquisa. Pode ser 'name', 'ext' ou qualquer outra string para pesquisar por data de modificação.",
)
@click.option(
    "-v", "--value", required=True, help="Define o valor da chave de pesquisa."
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
    help="Define se a pesquisa deve ser recursiva.",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    default=False,
    help="Define se o resultado da pesquisa deve ser salvo em um arquivo.",
)
@click.option(
    "-c",
    "--copy-to",
    help="Define o diretório para onde os arquivos encontrados devem ser copiados.",
)
def finder(path, key, value, recursive, copy_to, save):
    """Um programa que realiza busca de arquivos atraves de uma chave (-k|--key) a partir do diretorio PATH.

    Args:
        path (str): define o diretorio onde a pesquisa inicia. Se nao informado, assume o diretorio atual.
        key (str): Chave de pesquisa. Pode ser 'name' para pesquisar por nome de arquivo, 'ext' para pesquisar por extensão de arquivo ou qualquer outra string para pesquisar por data de modificação.
        value (str): Valor de pesquisa correspondente à chave. Para 'name', é o nome do arquivo a ser pesquisado. Para 'ext', é a extensão do arquivo a ser pesquisado. Para pesquisa por data de modificação, é a data no formato 'dd/mm/yyyy'.

    Raises:
        Exception: Lança uma exceção se o diretório especificado não existir.
    """
    root = Path(path)

    if not root.is_dir():
        raise InvalidInputError(f"O caminho {path} não é um diretório válido")

    click.echo(f"O diretório selecionado foi {root.absolute()}")

    files = process_search(path=root, key=key, value=value, recursive=recursive)
    report = process_results(files=files, key=key, value=value)

    save_report(save=save, report=report, root=root)
    copy_files(copy_to=copy_to, files=files)


if __name__ == "__main__":
    try:
        finder()
    except FileFinderError as err:
        click.echo(click.style(f"❌ {err}", bg="black", fg="red", italic=True))

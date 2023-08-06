class FileFinderError(Exception):
    """Classe mãe para tratar todas as exceções do programa."""

    pass


class InvalidInputError(FileFinderError):
    """Classe para tratar exceções de entrada inválida."""

    pass


class ZeroFilesFoundError(FileFinderError):
    """Classe específica para quando nenhum arquivo é encontrado na busca."""

    pass

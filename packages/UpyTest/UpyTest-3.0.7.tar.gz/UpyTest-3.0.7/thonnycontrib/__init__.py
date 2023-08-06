from .outlines import Outliner

# Ceci est une implémentation de création d'un singleton pour OutlineParser
_outliner = None

def get_outliner() -> Outliner:
    """
    Retourne une instance de `OutlineParser` en tant que singleton.
    """
    return Outliner() if not _outliner else _outliner
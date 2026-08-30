"""Utilidades transversales del servicio."""


import functools

def con_registro(func):
    """Registra la llamada y propaga errores sin ocultarlos."""
    @functools.wraps(func)   # ← Preserva nombre y docstring
    def envoltura(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            print(f"[registro] {func.__name__} falló: {exc}")
            raise  # ← Propaga la excepción en lugar de devolver None
    return envoltura

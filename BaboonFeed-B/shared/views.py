from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Clase de paginación para los posts.
    Permite paginar los resultados con un límite y un desplazamiento.
    """
    default_limit = 10
    max_limit = 100
from .ambito_repository import AmbitoRepository
from .area_repository import AreaRepository
from .caserio_repository import CaserioRepository
from .categoria_documento_repository import CategoriaDocumentoRepository
from .usuario_repository import UsuarioRepository
from .centro_poblado_repository import CentroPobladoRepository
from .comunicacion_area_repository import ComunicacionAreaRepository
from .derivacion_repository import DerivacionRepository
from .detalle_derivacion_repository import DetalleDerivacionRepository
from .documento_repository import DocumentoRepository
from .remitente_repository import RemitenteRepository

__all__ = ["AmbitoRepository", "AreaRepository", "CaserioRepository", "CategoriaDocumentoRepository",
           "UsuarioRepository", "CentroPobladoRepository", "ComunicacionAreaRepository", "DerivacionRepository",
           "DetalleDerivacionRepository", "DocumentoRepository", "RemitenteRepository"]
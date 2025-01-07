from enum import Enum

class EstadoDerivacionEnum(Enum):
    iniciada = "Iniciada"
    recepcionada = "Recepcionada"
    en_progreso = "En progreso"
    finalizada = "Finalizada"
    rechazada = "Rechazada"
    reasignada = "Reasignada"
    archivado = "Archivado"
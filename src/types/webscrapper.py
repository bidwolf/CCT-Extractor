"""This module is responsible for defining the interface for WebscrapperCCT"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class Agreements(Enum):
    """Enum for agreements or TipoRequerimento"""

    CONVENCAO = "convencao"
    TERMO_ADITIVO_CONVENCAO = "termoAditivoConvecao"
    TERMO_ADITIVO_ACORDO = "termoAditivoAcordo"


class Scopes(Enum):
    """Enum for Scopes or Abrangencia"""

    TODOS = "Todos os tipos"
    NACIONAL = "Nacional"
    ESTADUAL = "Estadual"
    MUNICIPAL = "Municipal"
    INTERMUNICIPAL = "Intermunicipal"


class Validity(Enum):
    """Enum for Validity or Vigencia"""

    TODOS = "2"
    VIGENTES = "1"
    NAO_VIGENTES = "0"


class CCTPayload(BaseModel):
    """Payload for CCT"""

    tpRequerimento: Agreements = Agreements.CONVENCAO
    dsTipoAbrangencia: Scopes = Scopes.TODOS
    nrCnpj: str | None = None
    nrCei: str | None = None
    noRazaoSocial: str | None = None
    dsCategoria: str | None = None
    tpVigencia: Validity = Validity.VIGENTES
    sgUfDeRegistro: str | None = None
    dtInicioRegistro: datetime | None = None
    dtFimRegistro: datetime | None = None
    dtInicioVigenciaInstrumentoColetivo: datetime | None = None
    dtFimVigenciaInstrumentoColetivo: datetime | None = None
    tpAbrangencia: str | None = None
    ufsAbrangidasTotalmente: str | None = None
    cdMunicipiosAbrangidos: str | None = None
    cdGrupo: str | None = None
    cdSubGrupo: str | None = None
    noTituloClausula: str | None = None
    dsAbrangenciaTerritorial: str | None = None
    utilizarSiracc: str | None = None
    excel: bool = False
    pagina: str | int = "1"
    qtdTotalRegistro: str | int = "-1"


class WebscrapperCCTInterface(ABC):
    """Interface for WebscrapperCCT"""

    @abstractmethod
    async def get_json_data(self):
        """Responsible for stract data as json from the Public website"""

    @abstractmethod
    async def get_cct_download(self, req_code: str):
        """Search for a specific CCT on the Public website"""

    @abstractmethod
    async def search_cct(self, employer_id: str, labor_union_id: str):
        """
        Search for a specific CCT on the Public website
        that is related to the employer and labor union
        """

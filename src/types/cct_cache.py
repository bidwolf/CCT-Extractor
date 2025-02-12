from pydantic import BaseModel


class CCTCacheFunctionParams(BaseModel):
    vigencia: str | None = None
    clausula_vigencia: str | None = None
    categoria_profissional: str | None = None
    abrangencia_territorial: str | None = None
    clausula_abrangencia: str | None = None
    data_base: str | None = None
    coberturas: list[str] = []
    clausula_seguro: str | None = None

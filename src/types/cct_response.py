from pydantic import BaseModel


class CCTResponse(BaseModel):
    """Response model for the CCT assistant."""

    erro: str | None = None
    resumo: str | None = None
    vigencia: str | None = None
    abrangencia_territorial: str | None = None
    categoria_profissional: str | None = None
    data_base: str | None = None

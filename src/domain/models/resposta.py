from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RespostaExecucao:
    sucesso: bool
    mensagem: str
    dados: Optional[Any] = None
    erro: Optional[str] = None 
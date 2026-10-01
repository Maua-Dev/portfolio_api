"""Convenções de chaves Dynamo (tabela base, sem GSI).

Tabela base (alinhada a iac/components/dynamo_construct.py):
  pk = USER | PROJECT
  sk = USER#<uuid> | PROJECT#<uuid>

Uso no repository Dynamo (exemplo)::

    from boto3.dynamodb.conditions import Key
    from src.shared.infra.external.dynamo.dynamo_keys import (
        EntityKind, PK_ATTR, partition_key,
    )

    resp = self.dynamo.query(
        KeyConditionExpression=Key(PK_ATTR).eq(partition_key(EntityKind.USER)),
    )
"""

from enum import Enum
from typing import Any
from uuid import UUID

# Nomes dos atributos da tabela base (alinhados ao CDK: pk/sk)
PK_ATTR = "pk"
SK_ATTR = "sk"

STORAGE_KEY_ATTRS = (PK_ATTR, SK_ATTR)


class EntityKind(str, Enum):
    USER = "USER"
    PROJECT = "PROJECT"


def partition_key(kind: EntityKind) -> str:
    """PK da tabela base — coleção (se repete para todos os items)."""
    return kind.value


def sort_key(id: UUID, kind: EntityKind) -> str:
    """SK da tabela base — identidade única dentro da coleção."""
    return f"{kind.value}#{id}"


def strip_keys(item: dict[str, Any]) -> dict[str, Any]:
    """Remove atributos de storage (pk/sk) antes do model_validate."""
    return {k: v for k, v in item.items() if k not in STORAGE_KEY_ATTRS}

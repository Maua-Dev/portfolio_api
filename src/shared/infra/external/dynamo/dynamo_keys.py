"""Convenções de chaves Dynamo (tabela base + GSI de user por email).

Tabela base (alinhada a iac/components/dynamo_construct.py):
  pk = USER | PROJECT
  sk = USER#<uuid> | PROJECT#<uuid>

GSI2 (UserEmailIndex) — access pattern secundário "user por email":
  gsi2pk = EMAIL#<email>
  gsi2sk = created_at zero-padded
  denso: email é obrigatório na entidade User

Uso no repository Dynamo (exemplo)::

    from boto3.dynamodb.conditions import Key
    from src.shared.infra.external.dynamo.dynamo_keys import (
        GSI2_NAME, GSI2_PK_ATTR, gsi2_partition_key,
    )

    resp = self.dynamo.query(
        KeyConditionExpression=Key(GSI2_PK_ATTR).eq(gsi2_partition_key(user_email)),
        IndexName=GSI2_NAME,
    )
"""

from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import EmailStr

# Nomes dos atributos da tabela base (alinhados ao CDK: pk/sk)
PK_ATTR = "pk"
SK_ATTR = "sk"

# GSI2 — access pattern: buscar user por email (denso: email sempre presente)
# Alinhado ao padrão do clean_mss_template (UserEmailIndex)
GSI2_NAME = "UserEmailIndex"
GSI2_PK_ATTR = "gsi2pk"
GSI2_SK_ATTR = "gsi2sk"

STORAGE_KEY_ATTRS = (
    PK_ATTR, SK_ATTR,
    GSI2_PK_ATTR, GSI2_SK_ATTR,
)


class EntityKind(str, Enum):
    USER = "USER"
    PROJECT = "PROJECT"


def partition_key(kind: EntityKind) -> str:
    """PK da tabela base — coleção (se repete para todos os items)."""
    return kind.value


def sort_key(id: UUID, kind: EntityKind) -> str:
    """SK da tabela base — identidade única dentro da coleção."""
    return f"{kind.value}#{id}"


def gsi2_partition_key(user_email: EmailStr) -> str:
    """
    PK do GSI2 — agrupa por email.

    Ex.: EMAIL#user@example.com
    """
    return f"EMAIL#{user_email}"


def gsi2_sort_key(created_at: int) -> str:
    """
    SK do GSI2 — ordenação por created_at (string zero-padded).

    Ex.: 0001700000000
    """
    return f"{created_at:013d}"


def build_gsi2_attributes(
    user_email: EmailStr,
    created_at: int,
) -> dict[str, str]:
    """
    GSI denso: email é obrigatório na entidade User, então todo user
    recebe gsi2pk/gsi2sk e entra no UserEmailIndex.
    """
    return {
        GSI2_PK_ATTR: gsi2_partition_key(user_email=user_email),
        GSI2_SK_ATTR: gsi2_sort_key(created_at=created_at),
    }


def strip_keys(item: dict[str, Any]) -> dict[str, Any]:
    """Remove atributos de storage (pk/sk/gsi) antes do model_validate."""
    return {k: v for k, v in item.items() if k not in STORAGE_KEY_ATTRS}

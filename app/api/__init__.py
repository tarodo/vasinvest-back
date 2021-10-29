from enum import Enum

from fastapi import HTTPException


def raise_400(err: Enum):
    raise HTTPException(
        status_code=400, detail={"error": str(err), "error_msg": str(err.value)}
    )

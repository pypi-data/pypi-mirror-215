from bs_common_fastapi.common.config.base import base_settings
from fastapi import Query


async def pagination_parameters(
    skip: int = Query(description=base_settings.APP_DESCRIPTION_SKIP, default=0),
    limit: int = Query(description=base_settings.APP_DESCRIPTION_LIMIT, default=base_settings.APP_MAX_LIMIT_VALUE)
):
    limit = base_settings.APP_MAX_LIMIT_VALUE if limit > base_settings.APP_MAX_LIMIT_VALUE else limit
    return {'skip': skip, 'limit': limit}


async def projection_parameters(
        fields: str | None = Query(description=base_settings.APP_DESCRIPTION_FIELDS, default=None)
):
    return {x.strip(): 1 for x in fields.split(',')} if fields is not None else None

from functools import wraps

from exceptions import S3ClientException


def catch(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)
        if not res.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            raise S3ClientException
        return res

    return wrapper

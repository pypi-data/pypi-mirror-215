from exceptions import S3ClientException


async def catch(func):
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)
        if not res.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            raise S3ClientException
        return res

    return wrapper


def _catch(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        status_code = res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if not isinstance(status_code, int) or status_code != 200:
            raise S3ClientException({"status_code": status_code})
        return res

    return wrapper

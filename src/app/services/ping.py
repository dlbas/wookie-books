from starlette.requests import Request


async def ping_service(request: Request) -> dict[str, bool]:
    return {"ok": True}

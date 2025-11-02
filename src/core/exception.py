# src/core/exception.py
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger


# --------业务异常处理-----------
class NotFoundException(HTTPException):
    """资源未找到异常"""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AlreadyExistsException(HTTPException):
    """资源已存在异常"""

    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnauthorizedException(HTTPException):
    """未授权异常"""

    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    

class ForbiddenException(HTTPException):
    """禁止访问异常"""

    def __init__(self, detail: str = "Access Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


# ------------兜底全局异常处理函数-----------------
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理的异常{request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )


def register_exception_handlers(app: FastAPI):
    """注册全局异常处理器"""
    app.add_exception_handler(Exception, general_exception_handler)
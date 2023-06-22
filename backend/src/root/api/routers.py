from typing import Annotated

from fastapi import APIRouter, Request, Query, Body, Path, HTTPException

from .schemas import SearchResponse, Record

router = APIRouter(tags=['Full text search'])


@router.get("/")
async def root():
    return {"Success": True}


@router.get("/search", response_model=SearchResponse)
async def search_post(request: Request, q: Annotated[str, Query]):
    res = request.app.sync.get_data_by_search(text=q)
    if not res:
        raise HTTPException(status_code=404, detail=f"По запросу '{q}' ничего не найдено")
    return {"query": q, "response": res}


@router.post("/search", response_model=Record)
async def create_post(request: Request, body: Annotated[Record, Body]):
    res = request.app.sync.create_post(body=body)
    return res


@router.put("/search", response_model=Record)
async def update_post(request: Request, body: Annotated[Record, Body]):
    if not request.app.sync.get_post(id_=body.id):
        raise HTTPException(status_code=404, detail=f"Запись с id={body.id} не найдена")

    res = request.app.sync.update_post(body=body)
    return res


@router.delete("/search/{post_id}")
async def delete_post(request: Request, post_id: Annotated[int, Path]):
    if not request.app.sync.get_post(id_=post_id):
        raise HTTPException(status_code=404, detail=f"Запись с id={post_id} не найдена")

    request.app.sync.delete_post(id_=post_id)
    return {"id": post_id, "deleted": True}

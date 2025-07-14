from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = None # optional
    price: float
    tax: float | None = None

# declare query parameters as Pydantic data model
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

# instantiate a FastAPI instance
app = FastAPI()

# define the home route
# GET request to the home route returns "Hello World"
@app.get("/")
async def root():
    return {"message": "Hello World"}

# route dedicated for creating a new Item
# reads the request body as JSON to create the Item
@app.post("/items/create_item")
async def create_item(item: Item):
    item.name.strip()
    
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    return {
        "item_id": item_id,
        "item": item
    }

# path parameter item_id
@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=100)], 
    q: Annotated[str | None, Query(alias="item-query")] = None
): 
    results = {"item_id": item_id}

    if q:
        results.update({"q": q})
    return results

# this won't ever execute, as the route above will catch all cases
@app.get("/items/3")
async def read_item_fixed(): # type hint & data validation: item_id must be an int
    return {"fixed_value": 3}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
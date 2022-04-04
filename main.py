import uvicorn

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(title="TodoMVC", description="A simple TodoMVC API built with fastapi")


# pydantic schema
class Todo(BaseModel):
    task: str

# model
class TodoModel(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
            return "Item not found"

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)

# Add entries
Data = TodoModel()
Data.create({'task': 'Build an API'})
Data.create({'task': 'Second task'})
Data.create({'task': 'Use fastapi'})


@app.get("/", tags=["Todos"])
def list_todos():
    '''List all tasks'''
    return Data.todos

@app.post("/", status_code=201, tags=["Todos"])
def add_todo(todo: Todo):
    '''Create a new task'''
    task = jsonable_encoder(todo)
    return Data.create(task)

@app.get("/{item_id}", tags=["Todos"])
def get_todo(item_id: int):
    '''Fetch a given resource'''
    return Data.get(item_id)

@app.delete("/{item_id}", status_code=204, tags=["Todos"])
def delete_todo(item_id: int):
    '''Delete a task given its identifier'''
    Data.delete(item_id)
    return ""

@app.put("/{item_id}", tags=["Todos"])
def update_todo(todo: Todo, item_id: int):
    '''Update a task given its identifier'''
    task = jsonable_encoder(todo)
    return Data.update(item_id, task)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
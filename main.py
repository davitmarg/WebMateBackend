from fastapi import FastAPI, Request
from fastapi.params import Body
import user_session_manager

from person import Person

app = FastAPI()

@app.post("/send_message")
def send_message(request: Request, user_id: str = Body(...), message: str = Body(...)):
    client_host = request.client.host
    user_id += "@" + client_host
    return {"response": user_session_manager.send_message(user_id, message)}


@app.post("/get_suggestion")
def get_suggestion(request: Request, user_id: str = Body(..., embed=True)):
    client_host = request.client.host
    user_id += "@" + client_host

    if user_session_manager.should_suggest(user_id):
        return {"response": user_session_manager.get_suggestion(user_id), "should_suggest": True}
    else:
        return {"response": "", "should_suggest": False}


@app.post("/add_page")
def add_page(request: Request, user_id: str = Body(...), page: str = Body(...)):
    print(user_id)

    client_host = request.client.host
    user_id += "@" + client_host

    user_session_manager.add_page(user_id, page)
    return {"status": "success"}


@app.post("/update_description")
def update_description(request: Request, user_id: str = Body(...)):

    client_host = request.client.host
    user_id += "@" + client_host

    return {"response": user_session_manager.update_description(user_id)}


@app.patch("/reset")
def reset(request: Request, user_id: str = Body(...)):

    client_host = request.client.host
    user_id += "@" + client_host

    user_session_manager.reset(user_id)
    return {"response": "Person reset"}

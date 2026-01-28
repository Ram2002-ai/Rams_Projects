from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
import json
from datetime import datetime
import os

app = FastAPI(title="Async Scientific Calculator API")

HISTORY_FILE = "history.json"


# ---------- DATA MODEL ----------
class Operation(BaseModel):
    a: float
    b: float | None = None


# ---------- HELPERS ----------
async def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


async def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


async def add_history(expression, result):
    history = await load_history()
    history.append({
        "expression": expression,
        "result": result,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    await save_history(history)


# ---------- API ROUTES ----------
@app.get("/")
def root():
    return {
        "message": "Calculator API is running 🚀",
        "docs": "http://127.0.0.1:8000/docs"
    }

@app.post("/calculate")
async def calculate(operation: str, data: Operation):
    if operation == "add":
        result = data.a + data.b
        await add_history(f"{data.a} + {data.b}", result)

    elif operation == "subtract":
        result = data.a - data.b
        await add_history(f"{data.a} - {data.b}", result)

    elif operation == "multiply":
        result = data.a * data.b
        await add_history(f"{data.a} * {data.b}", result)

    elif operation == "divide":
        if data.b == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = data.a / data.b
        await add_history(f"{data.a} / {data.b}", result)

    elif operation == "power":
        result = data.a ** data.b
        await add_history(f"{data.a} ^ {data.b}", result)

    elif operation == "sqrt":
        if data.a < 0:
            raise HTTPException(status_code=400, detail="Negative number")
        result = math.sqrt(data.a)
        await add_history(f"√{data.a}", result)

    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return {"result": result}


@app.get("/history")
async def history():
    return await load_history()


@app.delete("/history")
async def clear_history():
    await save_history([])
    return {"message": "History cleared"}

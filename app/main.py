from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List, Optional
import json
import os
from urllib.parse import parse_qs
from app.routes import items as items_router

app = FastAPI(title="Items CRUD with File Storage")

app.include_router(items_router.router, prefix="/items", tags=["items"])

DATA_FILE = "items.json"


# ---------------------------
# Helper Functions
# ---------------------------

def load_items() -> List[dict]:
    """Load items from JSON file"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_items(items: List[dict]):
    """Save items to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)


# ---------------------------
# Ensure file exists on startup
# ---------------------------

@app.on_event("startup")
def create_file_if_not_exists():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


# ---------------------------
# Home Page
# ---------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    items = load_items()

    html = """
    <html>
    <head>
        <title>Items</title>
        <style>
            table { border-collapse: collapse; width: 60%; margin: 20px auto; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #f4f4f4; }
            body { font-family: Arial; background: #fafafa; }
            .add-btn { 
                display: inline-block; 
                background: #4CAF50; 
                color: white; 
                padding: 10px 15px; 
                text-decoration: none; 
                margin: 20px auto;
                border-radius: 5px;
            }
            .delete-btn {
                background: #f44336;
                color: white;
                padding: 5px 10px;
                text-decoration: none;
                border-radius: 3px;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">Items List</h2>
        <div style="text-align:center;">
            <a href="/add" class="add-btn">➕ Add New Item</a>
        </div>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Is Offer</th>
                <th>Action</th>
            </tr>
    """

    for idx, item in enumerate(items):
        html += f"""
            <tr>
                <td>{idx}</td>
                <td>{item['name']}</td>
                <td>{item['price']}</td>
                <td>{item['is_offer']}</td>
                <td><a href="/delete/{idx}" class="delete-btn" onclick="return confirm('Are you sure?')">Delete</a></td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


# ---------------------------
# Add Item Form (GET)
# ---------------------------

@app.get("/add", response_class=HTMLResponse)
async def add_form():
    return """
    <html>
    <head>
        <title>Add Item</title>
        <style>
            body { font-family: Arial; margin: 50px; }
            .container { max-width: 400px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
            input { margin: 10px 0; padding: 8px; width: 100%; }
            button { background: #4CAF50; color: white; padding: 10px; border: none; cursor: pointer; width: 100%; }
            .back { display: inline-block; margin-top: 10px; text-align: center; width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Add New Item</h2>
            <form action="/add" method="post">
                Name: <input type="text" name="name" required><br>
                Price: <input type="number" name="price" step="0.01" required><br>
                Is Offer: <input type="checkbox" name="is_offer"><br>
                <button type="submit">Add Item</button>
            </form>
            <div class="back">
                <a href="/">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """


# ---------------------------
# Add Item (POST) - بدون python-multipart
# ---------------------------

@app.post("/add")
async def add_item(request: Request):
    body = await request.body()
    data = parse_qs(body.decode())
    
    name = data.get('name', [''])[0]
    price = float(data.get('price', ['0'])[0])
    is_offer = 'is_offer' in data
    
    items = load_items()
    items.append({
        "name": name,
        "price": price,
        "is_offer": is_offer
    })
    save_items(items)
    
    return RedirectResponse(url="/", status_code=303)


# ---------------------------
# Delete Item
# ---------------------------

@app.get("/delete/{item_id}")
async def delete_item(item_id: int):
    items = load_items()
    if 0 <= item_id < len(items):
        items.pop(item_id)
        save_items(items)
    return RedirectResponse(url="/", status_code=303)
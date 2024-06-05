from fastapi import FastAPI,HTTPException
import uvicorn
from inputs import MenuSearch
from scrape_menu import fetch_restaurant_name,run,fetch_menu_from_mongodb
app = FastAPI()


@app.post("/restaurants")
def read_restaurants(term:MenuSearch):
    res=fetch_restaurant_name(term.query)
    if(res==''):
        return {"message":"No restaurant found"}
    else:
        menu=run(res)
        if menu is None:
            raise HTTPException(status_code=404, detail="Blocked by Dineout")
        if "_id" in menu:
            menu["_id"] = str(menu["_id"])
        return menu 
        
    

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
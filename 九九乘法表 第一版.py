from FastAPI import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

def generate_multiplication_table(rows: int, columns: int) -> str:
    if rows < 1 or columns < 1:
        raise HTTPException(status_code=400, detail="Rows and columns must be greater than or equal to 1")
    if rows > 9 or columns > 9:
        raise HTTPException(status_code=400, detail="Rows and columns must be less than or equal to 9")

    table_html = "<table border='1'>"
    for i in range(1, rows + 1):
        table_html += "<tr>"
        for j in range(1, columns + 1):
            table_html += f"<td>{i} x {j} = {i * j}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    return table_html

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return generate_multiplication_table(9, 9)

@app.get("/{rows}x{columns}", response_class=HTMLResponse)
async def read_custom_table(rows: int, columns: int):
    return generate_multiplication_table(rows, columns)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


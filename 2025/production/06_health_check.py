@app.get("/health")
def health():
    return {"status": "ok"}
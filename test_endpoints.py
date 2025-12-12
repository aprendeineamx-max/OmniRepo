from src.engines.endpoint_mapper import EndpointMapper
import os

DUMMY_API = "dummy_api_routes.txt"

CODE = """
# Flask Example
@app.route("/api/v1/login")
def login(): pass

# Express Example
app.post('/auth/register', (req, res) => {});
router.delete("/users/:id", deleteUser);

# Django Example
urlpatterns = [
    path('admin/', admin.site.urls),
]

# FastAPI Example
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
"""

def test_mapper():
    print(f"Creating {DUMMY_API}...")
    with open(DUMMY_API, "w") as f:
        f.write(CODE)
        
    print("Running EndpointMapper...")
    mapper = EndpointMapper()
    endpoints = mapper.scan(DUMMY_API)
    
    if not endpoints:
        print("FAIL: No endpoints found.")
        return

    print("ENDPOINTS MAPPED:")
    mapped_routes = []
    
    for ep in endpoints:
        print(f" - [{ep['framework']}] {ep['method']} {ep['route']} (Line {ep['lineno']})")
        mapped_routes.append(ep['route'])

    # Assertions
    expected = [
        "/api/v1/login", # Flask
        "/auth/register", # Express
        "/users/:id",     # Express
        "admin/",         # Django
        "/items/{item_id}"# FastAPI
    ]
    
    if all(r in mapped_routes for r in expected):
        print("✅ ALL ROUTES DETECTED CORRECTLY")
    else:
        print(f"❌ MISSING ROUTES. Found: {mapped_routes}")

    # Cleanup
    os.remove(DUMMY_API)
    print("Cleanup complete.")

if __name__ == "__main__":
    test_mapper()

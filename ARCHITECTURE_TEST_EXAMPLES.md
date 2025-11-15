# Quick Test Examples

## Test Monolithic Architecture

```bash
curl -X POST http://localhost:8000/api/v1/generate-code \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "iVBORw0KGgo...",
    "description": "Task management app with authentication",
    "tech_stack": {
      "frontend": "React",
      "backend": "FastAPI",
      "database": "PostgreSQL",
      "architecture": "monolithic"
    },
    "project_name": "task-manager"
  }'
```

**Expected Output:**
```
✅ Files generated in monolithic structure:
- src/server/main.py
- src/server/config.py
- src/server/models/task.py
- src/server/routes/tasks.py
- src/client/App.tsx
- src/client/pages/Dashboard.tsx
- src/client/components/TaskCard.tsx
- src/shared/types/Task.ts
```

---

## Test Microservices Architecture

```bash
curl -X POST http://localhost:8000/api/v1/generate-code \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "iVBORw0KGgo...",
    "description": "E-commerce platform with shopping cart",
    "tech_stack": {
      "frontend": "React",
      "backend": "Django",
      "database": "PostgreSQL",
      "architecture": "microservices"
    },
    "project_name": "e-commerce"
  }'
```

**Expected Output:**
```
✅ Files generated in microservices structure:
- backend/manage.py
- backend/settings.py
- backend/models/product.py
- backend/views/product_views.py
- frontend/package.json
- frontend/src/App.tsx
- frontend/src/pages/Products.tsx
- frontend/src/components/ProductCard.tsx
```

---

## Default Behavior (No architecture specified)

```bash
curl -X POST http://localhost:8000/api/v1/generate-code \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "iVBORw0KGgo...",
    "description": "Blog platform",
    "tech_stack": {
      "frontend": "Vue",
      "backend": "Express",
      "database": "MongoDB"
    }
  }'
```

**Expected:** Defaults to **MONOLITHIC** architecture
```
✅ Files generated in monolithic structure (default):
- src/server/app.js
- src/client/App.vue
- src/shared/types/Post.ts
```

---

## Verify Architecture in Logs

Check the logs for architecture instructions:

```bash
tail -f r-net-backend/logs/app.log | grep "ARCHITECTURE"
```

You should see:
```
📁 MONOLITHIC ARCHITECTURE - Single Unified Folder Structure
# or
📁 MICROSERVICES ARCHITECTURE - Separate Backend & Frontend
```

---

## Frontend Extension Test

Update your VS Code extension request:

```typescript
const request = {
  image_data: base64Image,
  description: "User management system",
  tech_stack: {
    frontend: "React",
    backend: "FastAPI",
    database: "PostgreSQL",
    architecture: "monolithic" // Add this line!
  },
  project_name: "user-management"
};
```

---

## Python Script Test

```python
import requests
import base64

with open("mockup.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/v1/generate-code",
    json={
        "image_data": image_data,
        "description": "Social media dashboard",
        "tech_stack": {
            "frontend": "Angular",
            "backend": ".NET",
            "database": "PostgreSQL",
            "architecture": "monolithic"  # Single folder structure
        },
        "project_name": "social-dashboard"
    }
)

print("Generated files:")
for file in response.json()["files"]:
    print(f"  - {file['path']}")
```

---

## Compare Outputs

### Monolithic Output Example:
```
src/server/main.py
src/server/models/user.py
src/client/App.tsx
src/client/pages/Dashboard.tsx
src/shared/types/User.ts
```

### Microservices Output Example:
```
backend/main.py
backend/models/user.py
frontend/src/App.tsx
frontend/src/pages/Dashboard.tsx
```

**Key Difference:** `src/server/` + `src/client/` vs `backend/` + `frontend/`

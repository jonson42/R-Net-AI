# Chained vs Single Prompt - Quick Reference

## Visual Comparison

### Single Prompt Approach (`/generate`)

```
┌─────────────────────────────────────────────┐
│          ONE BIG PROMPT                     │
│                                             │
│  "Generate complete full-stack app with:   │
│   - Frontend (React)                        │
│   - Backend (FastAPI)                       │
│   - Database (PostgreSQL)                   │
│   - Authentication                          │
│   - All pages and components"               │
│                                             │
└──────────────────┬──────────────────────────┘
                   │
                   │ Single API Call
                   │ ~15 seconds
                   ▼
┌─────────────────────────────────────────────┐
│        COMPLETE CODE (15-20 files)          │
└─────────────────────────────────────────────┘
```

**Pros**: Fast, simple
**Cons**: Generic, less integrated

---

### Chained Prompt Approach (`/generate/chained`)

```
┌──────────────────────────────────────┐
│  STEP 1: Analyze Architecture        │
│  "What pages? What APIs? Tables?"    │
└─────────────┬────────────────────────┘
              │ Context: UI mockup
              ▼
         Architecture Plan
              │
              ▼
┌──────────────────────────────────────┐
│  STEP 2: Generate Database           │
│  "Create schema for these tables"    │
└─────────────┬────────────────────────┘
              │ Context: Table list
              ▼
        Database Files
              │
              ▼
┌──────────────────────────────────────┐
│  STEP 3: Generate Backend API        │
│  "Create API for these endpoints"    │
└─────────────┬────────────────────────┘
              │ Context: Database schema
              ▼
         Backend Files
              │
              ▼
┌──────────────────────────────────────┐
│  STEP 4: Generate Frontend           │
│  "Create UI matching mockup"         │
└─────────────┬────────────────────────┘
              │ Context: Backend API
              ▼
        Frontend Files
              │
              ▼
┌──────────────────────────────────────┐
│  STEP 5: Generate Configs            │
│  "Add Docker, README, deps"          │
└─────────────┬────────────────────────┘
              │ Context: Everything
              ▼
         Config Files
              │
              ▼
┌──────────────────────────────────────┐
│    COMBINED RESULT (20-30 files)     │
│        Everything integrated         │
└──────────────────────────────────────┘
```

**Pros**: Integrated, high quality
**Cons**: Slower, more API calls

---

## Side-by-Side Comparison

| Feature | `/generate` | `/generate/chained` |
|---------|-------------|---------------------|
| **Speed** | ⚡⚡⚡ 10-20s | ⚡ 40-60s |
| **API Calls** | 1 | 5 |
| **Cost** | $ 0.08 | $ 0.20 |
| **Quality** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Integration** | Basic | Excellent |
| **File Count** | 10-15 | 20-30 |
| **Context Aware** | ❌ No | ✅ Yes |
| **Best For** | Prototypes | Production |

---

## Real Example Output Comparison

### Same Request - Different Approaches

**Request**: "E-commerce app with cart and checkout"

### Single Prompt Output:
```
frontend/
  ├── App.jsx               # Generic cart component
  └── Cart.jsx              # Hardcoded API calls

backend/
  ├── main.py               # Basic endpoints
  └── models.py             # Simple models

❌ Frontend doesn't know backend structure
❌ Hardcoded API URLs
❌ Generic implementations
```

### Chained Prompt Output:
```
Step 1: Plans architecture
  - Identifies: Cart, Checkout, Payment pages
  - Plans: /api/cart, /api/checkout endpoints
  - Tables: products, cart_items, orders

Step 2: Creates database
  - Products table with proper fields
  - Cart relationships
  - Order tracking

Step 3: Generates backend
  - Implements exact endpoints from plan
  - Uses database structure from Step 2
  - Adds cart logic

Step 4: Generates frontend
  - Cart component calls exact API from Step 3
  - Knows API response structure
  - Proper state management

Step 5: Adds configs
  - README with full setup
  - Docker with all services
  - Complete dependencies

✅ Frontend knows exact backend API
✅ Correct API integration
✅ Database-aware backend
✅ Everything cross-referenced
```

---

## When to Use Which?

### Use `/generate` (Single Prompt) if:
```
✓ Building a quick prototype
✓ Simple app (< 10 files)
✓ Testing an idea
✓ Time is critical
✓ Learning/experimenting
✓ Single-page application
```

### Use `/generate/chained` (Multi-Step) if:
```
✓ Production application
✓ Complex features (auth, payments)
✓ Multiple pages/routes
✓ Need API integration
✓ Team collaboration
✓ Quality over speed
✓ Real business application
```

---

## Code Quality Difference

### Single Prompt - Generic Code
```javascript
// frontend/Cart.jsx - Generic
function Cart() {
  const [items, setItems] = useState([]);
  
  // Hardcoded URL
  fetch('http://localhost:8000/api/cart')
    .then(res => res.json())
    .then(data => setItems(data));
    
  // Generic structure
}
```

### Chained Prompt - Context-Aware Code
```javascript
// frontend/Cart.jsx - Knows exact API structure
import { getCartItems, updateQuantity } from '../services/api';

function Cart() {
  const [items, setItems] = useState([]);
  
  useEffect(() => {
    // Uses actual API service from Step 3
    getCartItems()
      .then(data => setItems(data.items))
      .catch(handleError);
  }, []);
  
  // Knows exact response structure:
  // { items: [], total: 0, tax: 0 }
  // from backend generation step
}
```

---

## Decision Tree

```
Start
  │
  ├─ Need it fast? ─────────────────────────► Use /generate
  │
  ├─ Simple app (< 10 files)? ──────────────► Use /generate
  │
  ├─ Just prototyping? ─────────────────────► Use /generate
  │
  ├─ Multiple pages? ───────────────────────► Use /generate/chained
  │
  ├─ Need authentication? ──────────────────► Use /generate/chained
  │
  ├─ Production app? ───────────────────────► Use /generate/chained
  │
  └─ Complex features? ─────────────────────► Use /generate/chained
```

---

## Summary

**Single Prompt**: Fast food - quick, convenient, good enough ⚡
**Chained Prompt**: Fine dining - takes time, high quality 🍽️

Both are available in your R-Net AI backend! Choose based on your needs.

Try them:
- `POST /generate` - Single prompt
- `POST /generate/chained` - Multi-step chained

See `CHAINED_GENERATION_GUIDE.md` for detailed documentation.

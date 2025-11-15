# 🎯 Architecture Quick Reference

## TL;DR

**Default:** Monolithic (single `src/` folder)
**Alternative:** Microservices (separate `backend/` and `frontend/` folders)

---

## 🏗️ Monolithic (Default)

```
src/
├── server/       # Backend
├── client/       # Frontend
└── shared/       # Shared code
```

**Use when:**
- Single team
- Same language (TypeScript full-stack)
- Need to share types/code
- Simple deployment

---

## 🔧 Microservices

```
backend/          # Backend service
frontend/         # Frontend service
```

**Use when:**
- Multiple teams
- Different languages (Python + React)
- Independent scaling
- Separate deployments

---

## 📝 How to Select

### In VS Code Extension:

Open generator → Select from dropdown:
- 🏗️ **Monolithic (Single Folder)** ← Default
- 🔧 **Microservices (Separate Folders)**

### In API Request:

```json
{
  "tech_stack": {
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "architecture": "monolithic"  // or "microservices"
  }
}
```

**Omit `architecture`** → Defaults to `monolithic`

---

## ✅ What Changed

**Before:** Always generated `backend/` and `frontend/`
**After:** Defaults to `src/server/` and `src/client/`

---

## 📦 Generated Files Example

### Monolithic:
```
✓ src/server/main.py
✓ src/server/models/user.py
✓ src/client/App.tsx
✓ src/client/pages/Dashboard.tsx
✓ src/shared/types/User.ts
```

### Microservices:
```
✓ backend/main.py
✓ backend/models/user.py
✓ frontend/src/App.tsx
✓ frontend/src/pages/Dashboard.tsx
```

---

## 🎨 Framework Recommendations

### Monolithic Works Best With:
- Next.js ⭐
- Remix ⭐
- SvelteKit ⭐
- ASP.NET MVC ⭐
- Django (with templates)

### Microservices Works Best With:
- React + FastAPI ⭐
- Vue + Django REST ⭐
- Angular + Express ⭐
- Any polyglot stack ⭐

---

## 🔍 Quick Comparison

| | Monolithic | Microservices |
|-|------------|---------------|
| **Folders** | `src/` unified | `backend/`, `frontend/` separate |
| **Deployment** | 1 container | 2+ containers |
| **Code Sharing** | ✅ Easy | ❌ Hard |
| **CORS** | ✅ Not needed | ⚠️ Required |
| **Setup Complexity** | ✅ Simple | ⚠️ Complex |
| **Team Size** | 1-5 devs | 5+ devs |

---

## 🚀 Try It Now

1. Open VS Code extension
2. Upload UI mockup
3. **Select "Monolithic"** (default)
4. Choose tech stack
5. Generate!

You'll get a unified folder structure! 🎉

---

## 📚 Full Documentation

- `ARCHITECTURE_GUIDE.md` - Complete guide
- `FOLDER_STRUCTURE_COMPARISON.md` - Visual comparison
- `ARCHITECTURE_TEST_EXAMPLES.md` - Test examples
- `MONOLITHIC_IMPLEMENTATION_SUMMARY.md` - Implementation details

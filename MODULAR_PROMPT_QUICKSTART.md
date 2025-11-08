# Quick Start: Modular Prompt System

## 🚀 TL;DR

The prompt system is now **modular** and **configurable**. Instead of one giant prompt, you can build custom prompts step-by-step.

## Basic Usage

### Option 1: Quick Generation (Minimal Prompt)

```python
from services.prompt_builder import QuickPromptBuilder
from models import TechStack

tech_stack = TechStack(
    frontend="React with TypeScript",
    backend="FastAPI", 
    database="PostgreSQL"
)

# Generates minimal prompt (no styling/testing/docs)
system_prompt, user_prompt = QuickPromptBuilder.minimal(
    tech_stack=tech_stack,
    project_name="my-app",
    description="Todo list with CRUD operations"
)
```

**Use when**: Quick prototypes, demos, learning

### Option 2: Full Production App

```python
# Generates comprehensive prompt with all features
system_prompt, user_prompt = QuickPromptBuilder.full_featured(
    tech_stack=tech_stack,
    project_name="student-portal",
    description="Student management system",
    features=[
        "Student registration",
        "Course enrollment", 
        "Grade management",
        "Analytics dashboard"
    ]
)
```

**Use when**: Production apps, client projects

### Option 3: Custom Configuration

```python
from services.prompt_builder import StepByStepPromptBuilder

# Build with custom options
system_prompt = StepByStepPromptBuilder.build_system_prompt(
    tech_stack=tech_stack,
    project_name="api-service",
    app_type="general",
    include_styling=False,   # No UI needed
    include_testing=True,    # Include tests
    include_docs=True        # Include docs
)

user_prompt = StepByStepPromptBuilder.build_user_prompt(
    description="REST API for data processing",
    tech_stack=tech_stack,
    features=["Data ingestion", "Processing pipeline"],
    styling_emphasis=False   # Backend-only
)
```

**Use when**: Specific requirements, API-only, specialized needs

## What's Different?

### Before (Old System)
```python
from services.prompt_templates import PromptTemplateEngine

# Always generates full prompt (~8,000 tokens)
system_prompt = PromptTemplateEngine.create_enhanced_system_prompt(
    tech_stack=tech_stack,
    project_name=project_name,
    app_type="general"
)
```

### After (New System)
```python
from services.prompt_builder import QuickPromptBuilder

# Flexible: 2,500-8,500 tokens based on needs
system_prompt, user_prompt = QuickPromptBuilder.minimal(...)  # Small
# OR
system_prompt, user_prompt = QuickPromptBuilder.full_featured(...)  # Large
```

## Key Benefits

| Feature | Old System | New System |
|---------|-----------|------------|
| Flexibility | ❌ Fixed prompt | ✅ Configurable |
| Token Usage | 8,000 (always) | 2,500-8,500 |
| Maintainability | ❌ Hard to modify | ✅ Modular sections |
| Performance | Slow | Faster (optimized) |
| Testing | Difficult | Easy (per-section) |

## Common Scenarios

### Scenario 1: Frontend Dashboard with Styling
```python
system_prompt, user_prompt = QuickPromptBuilder.full_featured(
    tech_stack=TechStack(frontend="React", backend="FastAPI", database="PostgreSQL"),
    project_name="analytics-dashboard",
    description="Sales analytics dashboard with charts",
    features=["Data visualization", "Filters", "Export reports"]
)
# ✓ Includes styling (Tailwind config, globals.css)
# ✓ Includes UI components (charts, cards, tables)
# ✓ Includes responsive design
```

### Scenario 2: Backend API (No UI)
```python
system_prompt = StepByStepPromptBuilder.build_system_prompt(
    tech_stack=tech_stack,
    project_name="payment-api",
    include_styling=False,  # ← No styling needed
    include_testing=True,
    include_docs=True
)
# ✓ Saves ~250 tokens (no CSS requirements)
# ✓ Faster generation
# ✓ Focus on API logic
```

### Scenario 3: Quick Prototype (Speed over Quality)
```python
system_prompt, user_prompt = QuickPromptBuilder.minimal(
    tech_stack=tech_stack,
    project_name="prototype",
    description="Quick demo app"
)
# ✓ Minimal prompt (~2,500 tokens)
# ✓ Fast generation (10-15s vs 30-40s)
# ✓ Basic functionality only
```

### Scenario 4: Enterprise App (Everything)
```python
system_prompt, user_prompt = QuickPromptBuilder.full_featured(
    tech_stack=tech_stack,
    project_name="enterprise-crm",
    description="Customer relationship management system",
    features=[
        "Customer management",
        "Sales pipeline",
        "Task automation",
        "Reporting dashboard",
        "Role-based access control"
    ]
)
# ✓ Complete styling
# ✓ Testing included
# ✓ Documentation included
# ✓ Security best practices
# ✓ Production-ready
```

## Configuration Options

### System Prompt Options

```python
StepByStepPromptBuilder.build_system_prompt(
    tech_stack: TechStack,        # Required
    project_name: str,             # Required
    app_type: str = "general",     # "general", "crud", "dashboard", etc.
    include_styling: bool = True,  # CSS/Tailwind requirements
    include_testing: bool = True,  # Test specifications
    include_docs: bool = True      # Documentation requirements
)
```

### User Prompt Options

```python
StepByStepPromptBuilder.build_user_prompt(
    description: str,              # Required: Project description
    tech_stack: TechStack,         # Required
    features: List[str] = None,    # Optional: Feature list
    styling_emphasis: bool = True  # Emphasize UI styling
)
```

## Token Savings

| Configuration | Token Count | Use Case |
|--------------|-------------|----------|
| Minimal (no styling/testing/docs) | ~2,500 | Quick prototypes |
| No styling | ~6,000 | Backend APIs |
| No testing | ~7,200 | Demos, learning |
| Full featured | ~8,500 | Production apps |

## Tips & Tricks

### 1. Provide Clear Features
```python
# ✓ Good
features = [
    "User authentication with JWT",
    "Product CRUD with pagination",
    "Shopping cart with checkout"
]

# ✗ Bad
features = ["make it good", "add stuff"]
```

### 2. Match Styling to Project Type
```python
# Frontend-heavy: Enable styling
styling_emphasis=True  # Dashboard, e-commerce, social app

# Backend-heavy: Disable styling
styling_emphasis=False  # API, data processing, CLI tool
```

### 3. Skip Tests for Prototypes
```python
# Prototype: Skip tests (faster)
include_testing=False

# Production: Include tests (quality)
include_testing=True
```

### 4. Use Appropriate Builder
```python
# Simple app → QuickPromptBuilder.minimal()
# Full app → QuickPromptBuilder.full_featured()
# Custom needs → StepByStepPromptBuilder (manual config)
```

## Troubleshooting

### Generated code has no CSS
**Fix**: Enable styling
```python
user_prompt = StepByStepPromptBuilder.build_user_prompt(
    ...,
    styling_emphasis=True  # ← Set to True
)
```

### Prompt is too long (exceeds token limit)
**Fix**: Disable optional sections
```python
system_prompt = StepByStepPromptBuilder.build_system_prompt(
    ...,
    include_styling=False,
    include_testing=False,
    include_docs=False
)
```

### Missing framework-specific patterns
**Fix**: Check if framework is supported
```python
# Supported frameworks:
# Frontend: React, Vue, Angular, Svelte
# Backend: FastAPI, Express, Django, Flask
```

### Generation is slow
**Fix**: Use minimal prompt
```python
system_prompt, user_prompt = QuickPromptBuilder.minimal(...)
# Reduces generation time by ~50%
```

## Migration from Old System

If you're using the old `PromptTemplateEngine`:

**Before:**
```python
from services.prompt_templates import PromptTemplateEngine

system_prompt = PromptTemplateEngine.create_enhanced_system_prompt(...)
user_prompt = PromptTemplateEngine.create_enhanced_user_prompt(...)
```

**After:**
```python
from services.prompt_builder import QuickPromptBuilder

system_prompt, user_prompt = QuickPromptBuilder.full_featured(...)
```

## Examples in Code

Check these files for real examples:
- `/r-net-backend/services/openai_service.py` - See how it's used in production
- `/r-net-backend/services/prompt_builder.py` - Full implementation
- `/docs/MODULAR_PROMPT_SYSTEM.md` - Detailed documentation

## Need Help?

1. **Read the docs**: `/docs/MODULAR_PROMPT_SYSTEM.md`
2. **Check examples**: Look at `openai_service.py`
3. **Test it**: Use the VS Code extension to generate a sample app
4. **Ask for help**: Open an issue with "prompt-builder" tag

---

**Quick tip**: Start with `QuickPromptBuilder.full_featured()` - it works for 90% of use cases!

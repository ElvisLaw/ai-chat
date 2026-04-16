# Errors Log

Command failures, exceptions, and unexpected behaviors.

---

## 2026-04-16: Pydantic `model_config` naming conflict

**Error:** `TypeError: 'function' object is not iterable`

**Location:** `src/ai_chat/settings.py`

**Cause:** `model_config` is a method name reserved by Pydantic's `BaseModel`. When defining a method with this name in a Settings class that inherits from BaseModel, Pydantic's internal model construction tries to iterate over it as if it were a config dict, causing the error.

**Solution:** Renamed `model_config()` to `get_model_config()`.

**Prevention:** Avoid using Pydantic reserved names as method names. Common reserved names include:
- `model_dump`
- `model_dump_json`
- `model_validate`
- `model_config`
- `model_fields`

---

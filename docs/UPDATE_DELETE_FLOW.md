# 📝 Update & Delete Flow — Detailed Explanation

This document explains the **complete flow** of how Update and Delete operations work in our Django project — from clicking a button in the browser to modifying data in the database.

---

## 📂 Files Involved

| File | Role |
|------|------|
| `urls.py` | Defines URL patterns with **capture groups** (`<str:id>`) |
| `views.py` | Contains `update()` and `delete()` functions |
| `view.html` | Displays the table with **Edit** and **Delete** buttons |
| `update.html` | The form page where user edits an entry |

---

## 🔗 URL Patterns (urls.py)

```python
path('update/<str:id>/', views.update, name='update')
path('delete/<str:id>/', views.delete, name='delete')
```

### What is `<str:id>`?

- It is a **capture group** (also called a URL parameter).
- It tells Django: "Whatever value appears in this part of the URL, capture it as a **string** and name it `id`."

### Example:

| URL Visited | `<str:id>` Captures |
|-------------|---------------------|
| `/update/101/` | `id = '101'` |
| `/update/202/` | `id = '202'` |
| `/delete/305/` | `id = '305'` |

---

## 🔄 UPDATE — Complete Flow

### Scenario: User wants to edit entry with ID=201 (TCS, Developer)

---

### **PHASE 1: Displaying the View Page (Before clicking Edit)**

```
┌──────────────────────────────────────────────────────────────────┐
│  views.py: def view(request)                                     │
│      data = CareerApp.objects.all()                              │
│      return render(request, 'view.html', {'data': data})         │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       │  Passes all entries to the template
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  view.html: {% for i in data %}                                  │
│                                                                  │
│  When i.id = 201:                                                │
│      {{ i.id }}      → displays "201"                            │
│      {{ i.company }} → displays "TCS"                            │
│      {{ i.role }}    → displays "Developer"                      │
│                                                                  │
│      {% url 'update' i.id %} → generates "/update/201/"          │
│      {% url 'delete' i.id %} → generates "/delete/201/"          │
└──────────────────────────────────────────────────────────────────┘
```

### How `{% url 'update' i.id %}` generates `/update/201/`:

```
Step 1: {% url %} tag looks up the name 'update' in urls.py
        → Finds: path('update/<str:id>/', views.update, name='update')

Step 2: Sees the pattern has a placeholder: <str:id>

Step 3: Takes the value passed (i.id = 201) and substitutes it
        → update/<str:id>/  becomes  update/201/

Step 4: Final URL generated: /update/201/
```

The HTML sent to the browser becomes:
```html
<a href="/update/201/">Edit</a>
```

---

### **PHASE 2: User Clicks "Edit" (GET Request)**

```
┌──────────────────────────────────────────────────────────────────┐
│  BROWSER                                                         │
│  User clicks: <a href="/update/201/">Edit</a>                    │
│  Browser sends: GET /update/201/                                 │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  DJANGO URL DISPATCHER (urls.py)                                 │
│                                                                  │
│  Tries to match: /update/201/                                    │
│                                                                  │
│  path('admin/', ...)          → ❌ No match                      │
│  path('', ...)                → ❌ No match                      │
│  path('entry/', ...)          → ❌ No match                      │
│  path('view/', ...)           → ❌ No match                      │
│  path('login/', ...)          → ❌ No match                      │
│  path('logout/', ...)         → ❌ No match                      │
│  path('update/<str:id>/', ..) → ✅ MATCH! Captures id='201'      │
│                                                                  │
│  Django calls: views.update(request, id='201')                   │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       │  Django automatically passes id='201'
                       │  because <str:id> in the URL pattern
                       │  matches the parameter name 'id' in
                       │  the function def update(request, id)
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  views.py: def update(request, id):   # id = '201'              │
│                                                                  │
│  data = CareerApp.objects.get(id=id)                             │
│         ─────────────────────  ─ ──                              │
│         │                      │  │                              │
│         │                      │  └─ Variable (value: '201')     │
│         │                      └──── Database field name         │
│         └────────────────────────── SQL: WHERE id = '201'        │
│                                                                  │
│  Result: data = CareerApp(id=201, company="TCS",                 │
│                           role="Developer", type="TECH",         │
│                           package="5-8LPA", status="APPLIED",    │
│                           date="2026-01-15", notes="Campus")     │
│                                                                  │
│  request.method == 'GET' (user just clicked the link)            │
│  So we skip the POST block                                       │
│                                                                  │
│  return render(request, 'update.html', {'data': data})           │
│  → Sends the form pre-filled with TCS data to the browser        │
└──────────────────────────────────────────────────────────────────┘
```

---

### **PHASE 3: User Edits and Clicks "Save Changes" (POST Request)**

```
┌──────────────────────────────────────────────────────────────────┐
│  BROWSER (update.html form)                                      │
│                                                                  │
│  User changes:                                                   │
│    status: APPLIED → TECHNICAL  (changed!)                       │
│    notes: "Campus" → "Cleared Round 1"  (changed!)               │
│                                                                  │
│  Clicks "Save Changes"                                           │
│  Browser sends: POST /update/201/ with form data:                │
│    company=TCS                                                   │
│    role=Developer                                                │
│    type=TECH                                                     │
│    package=5-8LPA                                                │
│    status=TECHNICAL        ← Changed                             │
│    date=2026-01-15                                               │
│    notes=Cleared Round 1   ← Changed                             │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  DJANGO URL DISPATCHER                                           │
│  Matches /update/201/ → calls views.update(request, id='201')    │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  views.py: def update(request, id):   # id = '201'              │
│                                                                  │
│  data = CareerApp.objects.get(id=id)  # Fetch existing entry     │
│                                                                  │
│  request.method == 'POST'  ← TRUE this time!                    │
│                                                                  │
│  # Update each field from the submitted form data:               │
│  data.company = request.POST.get('company')  # "TCS" (same)     │
│  data.role    = request.POST.get('role')     # "Developer"       │
│  data.type    = request.POST.get('type')     # "TECH"            │
│  data.package = request.POST.get('package')  # "5-8LPA"         │
│  data.status  = request.POST.get('status')   # "TECHNICAL" ←NEW │
│  data.date    = request.POST.get('date')     # "2026-01-15"     │
│  data.notes   = request.POST.get('notes')    # "Cleared.." ←NEW │
│                                                                  │
│  data.save()  # Writes changes to the database                   │
│               # SQL: UPDATE CareerApp SET status='TECHNICAL',    │
│               #      notes='Cleared Round 1' WHERE id=201;       │
│                                                                  │
│  return redirect('view')  # Takes user back to View page         │
└──────────────────────────────────────────────────────────────────┘
```

---

### **UPDATE: Comparison with ENTRY**

Both use the same pattern — but with one key difference:

| | **Entry (Create)** | **Update (Edit)** |
|---|---|---|
| **Creates new object?** | ✅ Yes: `CareerApp(id=id, ...)` | ❌ No |
| **Fetches existing?** | ❌ No | ✅ Yes: `.objects.get(id=id)` |
| **Modifies fields?** | Sets all fields on a new object | Overwrites fields on existing object |
| **Saves?** | `data.save()` → INSERT into DB | `data.save()` → UPDATE in DB |
| **Django knows?** | It's a new object, so it does INSERT | Object already has a primary key, so it does UPDATE |

```python
# ENTRY — Creates NEW row
data = CareerApp(id=id, company=company, ...)  # New object
data.save()  # SQL: INSERT INTO CareerApp ...

# UPDATE — Modifies EXISTING row
data = CareerApp.objects.get(id=id)  # Fetch existing object
data.company = "New Value"           # Change field
data.save()  # SQL: UPDATE CareerApp SET company='New Value' WHERE id=201;
```

---

## ❌ DELETE — Complete Flow

### Scenario: User wants to delete entry with ID=201

```
┌──────────────────────────────────────────────────────────────────┐
│  BROWSER (view.html)                                             │
│                                                                  │
│  User clicks: <a href="/delete/201/"                             │
│     onclick="return confirm('Are you sure?')">Delete</a>         │
│                                                                  │
│  ┌────────────────────────────────────────┐                      │
│  │   ⚠️ JavaScript Popup                  │                      │
│  │                                        │                      │
│  │   Are you sure you want to delete      │                      │
│  │   this entry?                          │                      │
│  │                                        │                      │
│  │       [Cancel]        [OK]             │                      │
│  └────────────────────────────────────────┘                      │
│                                                                  │
│  If "Cancel" → Nothing happens (stays on page)                   │
│  If "OK"     → Browser sends: GET /delete/201/                   │
└──────────────────────┬───────────────────────────────────────────┘
                       │  User clicked "OK"
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  DJANGO URL DISPATCHER                                           │
│                                                                  │
│  Matches: /delete/201/                                           │
│  Pattern: path('delete/<str:id>/', views.delete, name='delete')  │
│  Captures: id = '201'                                            │
│                                                                  │
│  Calls: views.delete(request, id='201')                          │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  views.py: def delete(request, id):    # id = '201'             │
│                                                                  │
│  data = CareerApp.objects.get(id=id)                             │
│  # Fetches: CareerApp(id=201, company="TCS", ...)                │
│                                                                  │
│  data.delete()                                                   │
│  # SQL: DELETE FROM CareerApp WHERE id = 201;                    │
│  # The row is PERMANENTLY removed from the database              │
│                                                                  │
│  return redirect('view')                                         │
│  # Takes user back to View page (entry 201 is now GONE)          │
└──────────────────────────────────────────────────────────────────┘
```

### How `onclick="return confirm(...)"` works:

```
1. User clicks "Delete" link
2. JavaScript runs: confirm('Are you sure you want to delete this entry?')
3. A browser popup appears with "OK" and "Cancel"
4. If user clicks "Cancel":
     - confirm() returns false
     - "return false" prevents the link from being followed
     - Nothing happens, user stays on the page
5. If user clicks "OK":
     - confirm() returns true
     - "return true" allows the link to be followed
     - Browser navigates to /delete/201/
```

---

## 🧠 Key Concepts Summary

### 1. Capture Groups (`<str:id>`)
```
URL Pattern:   update/<str:id>/
Actual URL:    update/201/
Captured:      id = '201'
```
The `<str:id>` part acts like a variable placeholder in the URL. Django extracts the value and passes it to the view function.

### 2. Reverse URL Lookup (`{% url 'name' value %}`)
```
Template:      {% url 'update' i.id %}
Looks up:      path('update/<str:id>/', ..., name='update')
Substitutes:   i.id (201) into <str:id>
Generates:     /update/201/
```
The `{% url %}` tag builds URLs dynamically by looking up the pattern name and substituting values.

### 3. Name Matching (URL ↔ Function)
```python
# urls.py
path('update/<str:id>/', views.update, name='update')
#                  ^^                          
#                  This name...               

# views.py
def update(request, id):
#                   ^^
#                   ...must match this name!
```

### 4. `.get(id=id)` — Left vs Right
```python
data = CareerApp.objects.get(id=id)
#                            ↑  ↑
#                            │  └── Python variable (value from URL: '201')
#                            └───── Database column name (model field)
```

---

## 🔁 Side-by-Side: Update vs Delete

| Step | **Update** | **Delete** |
|------|-----------|-----------|
| 1. User clicks | "Edit" on ID=201 | "Delete" on ID=201 |
| 2. Browser sends | `GET /update/201/` | Popup → `GET /delete/201/` |
| 3. Django captures | `id='201'` | `id='201'` |
| 4. Django calls | `update(request, id='201')` | `delete(request, id='201')` |
| 5. Fetches data | `CareerApp.objects.get(id='201')` | `CareerApp.objects.get(id='201')` |
| 6. Action | Shows pre-filled form (GET) | `data.delete()` → row removed |
| 7. On form submit | Updates fields & `data.save()` (POST) | — |
| 8. Redirect | → View Applications page | → View Applications page |
| **Total requests** | **2** (GET form, POST save) | **1** (GET delete) |

---

## 📊 Complete Architecture Diagram

```
     ┌─────────────────────────────────────────────────────────┐
     │                    BROWSER (Client-Side)                 │
     │                                                         │
     │  view.html                                              │
     │  ┌───────────────────────────────────────────────────┐  │
     │  │ ID  │ Company │ Role      │ Actions              │  │
     │  │ 201 │ TCS     │ Developer │ [Edit] [Delete]      │  │
     │  │ 202 │ Google  │ SDE       │ [Edit] [Delete]      │  │
     │  └───────────────────────────────────────────────────┘  │
     │                                                         │
     │  [Edit]   → href="/update/201/"                         │
     │  [Delete] → href="/delete/201/" + confirm() popup       │
     └───────────────┬─────────────────────┬───────────────────┘
                     │                     │
            Click Edit              Click Delete + OK
                     │                     │
                     ▼                     ▼
     ┌─────────────────────────────────────────────────────────┐
     │              DJANGO SERVER (Server-Side)                 │
     │                                                         │
     │  urls.py (URL Dispatcher)                               │
     │  ┌───────────────────────────────────────────────────┐  │
     │  │ /update/201/ → match <str:id> → id='201'         │  │
     │  │ /delete/201/ → match <str:id> → id='201'         │  │
     │  └───────────────────────────────────────────────────┘  │
     │                     │                     │             │
     │                     ▼                     ▼             │
     │  views.py                                               │
     │  ┌─────────────────────┐  ┌─────────────────────────┐  │
     │  │ update(req, id=201) │  │ delete(req, id=201)     │  │
     │  │                     │  │                         │  │
     │  │ GET:                │  │ .get(id=201)            │  │
     │  │  .get(id=201)       │  │ .delete()               │  │
     │  │  render(update.html)│  │ redirect('view')        │  │
     │  │                     │  └─────────────────────────┘  │
     │  │ POST:               │                               │
     │  │  .get(id=201)       │                               │
     │  │  update fields      │                               │
     │  │  .save()            │                               │
     │  │  redirect('view')   │                               │
     │  └─────────────────────┘                               │
     │                     │                                   │
     │                     ▼                                   │
     │  ┌───────────────────────────────────────────────────┐  │
     │  │              DATABASE (db.sqlite3)                │  │
     │  │                                                   │  │
     │  │  UPDATE: SET status='TECHNICAL' WHERE id=201      │  │
     │  │  DELETE: DELETE FROM CareerApp WHERE id=201       │  │
     │  └───────────────────────────────────────────────────┘  │
     └─────────────────────────────────────────────────────────┘
```

---

> **Author:** Anugrah K.  
> **Project:** CareerQuest - Django Job Application Tracker  
> **Last Updated:** Feb 2026

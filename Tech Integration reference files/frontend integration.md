# 🚀 Frontend Implementation Master Guide (FINAL – Production Ready)

---

# 🧠 Project Context

This frontend is for an **AI-powered GST Compliance & Invoice Reconciliation System** used by:

* MSMEs
* Accountants
* Auditors

---

## 🎯 Core Responsibilities

* Upload and process invoices
* Display reconciliation insights
* Provide compliance dashboards
* Show alerts & risks
* Export reports
* Integrate seamlessly with backend APIs

---

# ⚠️ STRICT IMPLEMENTATION RULES (NON-NEGOTIABLE)

1. Use **React (Vite)**
2. Use **functional components ONLY**
3. Use **Tailwind CSS**
4. Use **custom hooks for ALL API calls**
5. NO API calls inside components
6. Maintain strict separation (UI ≠ logic ≠ API)
7. Use reusable components
8. Avoid duplication
9. Follow clean naming conventions
10. Must fully match backend APIs

---

# 🏗 FOLDER STRUCTURE (STRICT)

/src
│
├── components/
│   ├── ui/
│   ├── charts/
│   ├── tables/
│   ├── alerts/
│   ├── upload/
│
├── pages/
├── layouts/
├── services/
├── hooks/
├── context/
├── utils/
├── constants/
├── assets/

---

# ⚙️ ENV CONFIG (MANDATORY)

Create `.env` file:

```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=GST AI Compliance
```

---

# 🔐 AUTHENTICATION FLOW (MANDATORY)

## Must Implement:

* Login Page (`/login`)
* JWT token handling
* Protected routes
* Auth context

---

## Auth Flow

1. User logs in → `/auth/login`
2. Token stored in `localStorage`
3. Axios attaches token automatically
4. Protected routes check token

---

## Required Files

* context/AuthContext.jsx
* hooks/useAuth.js
* utils/PrivateRoute.jsx

---

# 🛣 ROUTING STRUCTURE (STRICT)

Use React Router v6:

```
/login
/dashboard
/upload
/invoices
/reconciliation
/alerts
/reports
/vendors
```

---

# 🎨 DESIGN SYSTEM (FINTECH UI)

## Colors

* Primary: Indigo / Blue
* Success: Green
* Error: Red
* Warning: Yellow
* Background: Light Gray

## UI Rules

* Rounded corners (xl)
* Soft shadows
* Hover effects
* Smooth transitions
* Clean spacing

---

# 🔗 API LAYER (MANDATORY)

## services/api.js

* Axios instance
* Base URL from `.env`
* Interceptors:

  * Attach JWT token
  * Handle errors globally

---

## Services

### invoiceService.js

* uploadInvoice()
* fetchInvoices()

### reconciliationService.js

* runReconciliation()
* fetchReconciliation()

### reportService.js

* fetchReports()
* exportReport()

### alertService.js

* fetchAlerts()

---

# 🔄 BACKEND API CONTRACT (STRICT MATCH)

Frontend MUST use:

* POST /auth/login
* POST /invoice/upload
* GET /invoice/list
* POST /reconcile/run
* GET /reconcile/results
* GET /dashboard/summary
* GET /report/export
* GET /notifications

---

# ⚙️ STATE MANAGEMENT (STRICT)

## Custom Hooks (MANDATORY)

* useAuth()
* useInvoices()
* useUpload()
* useAlerts()
* useReports()
* useReconciliation()

---

## Each Hook MUST Handle:

* API call
* loading state
* error state
* data state

---

# 🔄 DATA FLOW (VERY IMPORTANT)

Component → Hook → Service → API

🚫 NEVER call API inside components

---

# ✨ PREMIUM UX FEATURES

## Animations (Framer Motion)

* Page transitions
* Card hover animations
* Smooth loading

---

## Loaders

* Skeleton loaders (tables/cards/dashboard)
* Spinner for actions

---

## Toast Notifications (React Hot Toast)

* Success → Upload complete
* Error → API failure
* Warning → Mismatch detected

---

# 📄 PAGES (FULL IMPLEMENTATION)

---

## 1. Dashboard (/dashboard)

### KPI Cards

* Total invoices
* Matched
* Mismatched
* Compliance score

### Charts

* Bar chart → match rate
* Line chart → monthly trend

### Sections

* Recent alerts
* Risky vendors

---

## 2. Upload Page (/upload)

### Features

* Drag & drop (React Dropzone)

* File preview list

* Upload progress

* File validation:

  * PDF, JPG, PNG
  * Max 5MB

* Toast feedback

---

## 3. Invoice Page (/invoices)

### Table Columns

* Invoice Number
* GSTIN
* Date
* Amount
* GST
* Status

### Features

* Search
* Filters
* Pagination
* Highlight mismatches (red)

---

## 4. Reconciliation Page (/reconciliation)

### Features

* Side-by-side comparison
* Highlight differences
* Status labels
* Mark as reviewed

---

## 5. Alerts Page (/alerts)

### Features

* Alert cards
* Severity filter
* Dismiss alerts

---

## 6. Reports Page (/reports)

### Features

* Generate reports
* Export CSV/Excel
* Preview table

---

## 7. Vendor Insights (/vendors)

### Features

* Vendor score (progress bar)
* Risk level
* AI insights

---

# 🧩 REUSABLE COMPONENTS (MANDATORY)

* Card
* Button
* Badge
* Table
* SkeletonLoader
* LoaderSpinner
* AlertCard
* FileUpload
* EmptyState

---

# ⚠️ ERROR HANDLING (STRICT)

Handle:

* Invalid file upload
* API failure
* Empty data
* Network issues

## UI Must Show:

* Error message
* Retry button
* Empty state UI

---

# 🧪 MOCK DATA (MANDATORY)

Use for development fallback:

```
{
  "invoice_number": "INV001",
  "gstin": "29ABCDE1234F2Z5",
  "amount": 10000,
  "status": "mismatch"
}
```

---

# 🚀 PERFORMANCE RULES

* Lazy load pages
* Optimize re-renders
* Use memoization where needed

---

# ⚙️ INSTALLATION & RUN

```
npm install
npm run dev
```

---

# 🎯 IMPLEMENTATION ORDER

1. Setup project (Vite + Tailwind)
2. Setup routing
3. Setup Auth (context + protected routes)
4. Build layout
5. Create UI components
6. Setup API layer
7. Create hooks
8. Build pages
9. Integrate APIs
10. Add loaders + animations
11. Handle errors

---

# 🚀 FINAL GOAL

Frontend must be:

✅ Clean
✅ Scalable
✅ Responsive
✅ API-integrated
✅ Visually impressive
✅ Hackathon demo ready

---

# 🔥 FINAL INSTRUCTION FOR AI

DO NOT:

* Skip hooks
* Skip API layer
* Skip auth
* Mix logic in UI

ALWAYS:

* Follow modular architecture
* Match backend EXACTLY
* Write production-ready code

---

# ✅ END OF GUIDE

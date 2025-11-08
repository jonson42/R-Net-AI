# Ready-to-Use Prompt Templates for R-Net AI

## 🎯 Master Template (Copy & Customize)

```
Generate a production-ready full-stack [APPLICATION_TYPE] application.

═══════════════════════════════════════════════════════════════════
CORE REQUIREMENTS
═══════════════════════════════════════════════════════════════════

[DESCRIBE YOUR APPLICATION HERE - BE SPECIFIC]

Example:
- User authentication and authorization
- Dashboard with analytics and charts
- CRUD operations for [ENTITY_NAME]
- Search, filter, and sort functionality
- File upload capabilities
- Email notifications
- Responsive mobile design
- Role-based access control

═══════════════════════════════════════════════════════════════════
KEY ENTITIES & DATA MODEL
═══════════════════════════════════════════════════════════════════

1. [Entity1]: id, name, email, created_at, status
   - Relationships: One-to-many with [Entity2]
   
2. [Entity2]: id, entity1_id (FK), title, description, date
   - Relationships: Many-to-one with [Entity1]
   
3. [Entity3]: id, name, type, value
   - Relationships: Many-to-many with [Entity1] through [JoinTable]

═══════════════════════════════════════════════════════════════════
USER ROLES & PERMISSIONS
═══════════════════════════════════════════════════════════════════

• Admin: Full system access, user management, system configuration
• Manager: [SPECIFIC_PERMISSIONS]
• User: [SPECIFIC_PERMISSIONS]
• Guest: View-only access (if applicable)

═══════════════════════════════════════════════════════════════════
KEY FEATURES & USER FLOWS
═══════════════════════════════════════════════════════════════════

1. Authentication Flow
   - Login with email/password
   - Registration with email verification
   - Password reset via email link
   - JWT token with auto-refresh

2. Main Features
   - [FEATURE_1]: Description and user interaction
   - [FEATURE_2]: Description and user interaction
   - [FEATURE_3]: Description and user interaction

3. Admin Features
   - [ADMIN_FEATURE_1]
   - [ADMIN_FEATURE_2]

═══════════════════════════════════════════════════════════════════
TECHNICAL REQUIREMENTS
═══════════════════════════════════════════════════════════════════

• Responsive design: Mobile-first approach
• Real-time updates: [WHERE_APPLICABLE]
• File uploads: With validation and preview
• Export/Import: CSV/Excel data exchange
• Pagination: Server-side with configurable page size
• Search: Full-text search across [ENTITIES]
• Notifications: In-app and email
• Audit logging: Track all critical actions
• Performance: <2s page load, <500ms API response

═══════════════════════════════════════════════════════════════════
DELIVERABLES REQUIRED
═══════════════════════════════════════════════════════════════════

✓ Complete frontend with all UI components
✓ Backend API with authentication and authorization
✓ Database schema with migrations and seed data
✓ Docker configuration for development and production
✓ Comprehensive README with setup instructions
✓ API documentation (OpenAPI/Swagger)
✓ Unit tests for critical business logic
✓ Integration tests for main API endpoints
✓ Environment configuration with .env.example
✓ Security best practices implemented throughout
```

---

## 📋 Pre-Built Templates by Application Type

### 1. Student Management System

```
Create a comprehensive Student Management System for educational institutions.

CORE FEATURES:
• Student registration with profile management (photo, contact info, emergency contacts)
• Course catalog with enrollment management
• Class scheduling with teacher assignments
• Attendance tracking (daily, per-class)
• Grade management (assignments, quizzes, exams, final grades)
• Transcript generation and GPA calculation
• Parent portal for viewing student progress
• Teacher dashboard for course management
• Admin dashboard with analytics (enrollment trends, grade distributions)
• Notification system (email/SMS for absences, grade updates)
• Report generation (transcripts, progress reports, attendance summaries)

KEY ENTITIES:
1. Student: id, first_name, last_name, email, phone, date_of_birth, enrollment_date, 
   status (active/inactive/graduated), grade_level, parent_contact, photo_url
   
2. Teacher: id, first_name, last_name, email, department, hire_date, subjects_taught, 
   bio, photo_url
   
3. Course: id, code (unique), name, description, credits, capacity, semester, 
   teacher_id (FK), schedule (days/times), status (open/closed/full)
   
4. Enrollment: id, student_id (FK), course_id (FK), enrollment_date, 
   status (enrolled/dropped/completed), final_grade, grade_points
   
5. Attendance: id, enrollment_id (FK), date, status (present/absent/late/excused), 
   notes, marked_by (teacher_id FK)
   
6. Assessment: id, course_id (FK), title, type (quiz/exam/project/homework), 
   max_score, due_date, weight_percentage
   
7. Submission: id, assessment_id (FK), student_id (FK), submitted_at, score, 
   feedback, graded_by (teacher_id FK), late_penalty

USER ROLES:
• Admin: Full system access, user management, system configuration, reports
• Teacher: Manage assigned courses, mark attendance, grade assessments, view rosters
• Student: View schedule, grades, attendance, submit assignments (if applicable)
• Parent: View child's grades, attendance, schedule (read-only)

TECHNICAL FEATURES:
• Bulk student import via CSV
• Automated GPA calculation
• Email notifications for grade posting, absences
• Calendar view of class schedules
• Grade distribution charts
• Attendance heatmaps
• Export transcripts as PDF
• Search students by name, ID, email
• Filter courses by department, semester, teacher
• Responsive dashboard with KPI cards
```

---

### 2. E-Commerce Platform

```
Build a modern e-commerce platform with customer-facing storefront and admin panel.

CUSTOMER FEATURES:
• Product browsing with category navigation and breadcrumbs
• Advanced search with filters (price range, brand, rating, availability)
• Product detail pages with image gallery, reviews, related products
• Shopping cart with quantity adjustment and price calculation
• Checkout process (3 steps: Shipping → Payment → Confirmation)
• Multiple payment methods (credit card, PayPal - mock implementations)
• Order tracking with status updates
• User account management (profile, addresses, payment methods)
• Order history with reorder functionality
• Product reviews and ratings (verified purchase badge)
• Wishlist/favorites
• Guest checkout option

ADMIN FEATURES:
• Product inventory management (CRUD with image upload)
• Category and brand management
• Order processing dashboard (pending, processing, shipped, delivered, cancelled)
• Customer management (view profiles, order history)
• Sales analytics (revenue, top products, conversion rates)
• Discount code generation and management
• Stock alerts for low inventory
• Bulk product import/export (CSV)
• Email template management for order confirmations
• Dashboard with sales charts and KPIs

KEY ENTITIES:
1. Product: id, sku (unique), name, description, price, compare_at_price, 
   cost_price, brand_id (FK), category_id (FK), stock_quantity, 
   low_stock_threshold, images (JSON array), attributes (JSON: color, size, etc.), 
   is_featured, is_active, avg_rating, review_count, created_at

2. Category: id, name, slug (unique), description, parent_id (FK - for subcategories), 
   image_url, sort_order, is_active

3. Brand: id, name, slug (unique), description, logo_url, website

4. Cart: id, user_id (FK - nullable for guest), session_id, items (JSON), 
   subtotal, tax, shipping, total, expires_at

5. Order: id, user_id (FK - nullable for guest), order_number (unique), 
   status (pending/processing/shipped/delivered/cancelled), 
   items (JSON snapshot), subtotal, tax, shipping, discount, total, 
   shipping_address (JSON), billing_address (JSON), payment_method, 
   payment_status, tracking_number, notes, created_at, updated_at

6. Review: id, product_id (FK), user_id (FK), rating (1-5), title, comment, 
   verified_purchase, helpful_count, created_at

7. User: id, email (unique), password_hash, first_name, last_name, phone, 
   default_shipping_address (JSON), default_billing_address (JSON), 
   role (customer/admin), is_active, last_login

TECHNICAL REQUIREMENTS:
• Product image optimization (WebP, lazy loading)
• Shopping cart persistence (localStorage + database sync)
• Real-time stock validation
• Automatic tax calculation based on location
• Shipping cost calculator
• Payment gateway integration (Stripe - test mode)
• Email notifications (order confirmation, shipping updates)
• Responsive product grid (1 col mobile, 2-3 tablet, 4+ desktop)
• Infinite scroll or pagination for product listings
• Search with autocomplete suggestions
• Recently viewed products tracking
• Abandoned cart recovery (save for later)
```

---

### 3. Project Management Tool

```
Develop a Kanban-style project management and team collaboration platform.

CORE FEATURES:
• Project workspace creation and management
• Kanban board with drag-and-drop task cards
• Task creation with rich text description, due dates, priority
• Task assignment to team members
• Task comments and activity timeline
• File attachments (images, documents, PDFs)
• Labels/tags for task categorization
• Sprint planning and management
• Gantt chart timeline view
• Dashboard with project overview and team activity
• Time tracking per task
• Team member management with role assignment
• Notifications for mentions, assignments, due dates
• Search across all projects and tasks
• Calendar view of deadlines and milestones

KEY ENTITIES:
1. Project: id, name, description, key (unique identifier like "PROJ"), 
   owner_id (FK), status (active/archived), visibility (private/team/public), 
   start_date, target_end_date, actual_end_date, created_at

2. Board: id, project_id (FK), name, type (kanban/scrum), columns (JSON array), 
   is_default, sort_order

3. Task: id, project_id (FK), board_id (FK), column_id, title, description (rich text), 
   assignee_id (FK), reporter_id (FK), priority (low/medium/high/critical), 
   status (todo/in_progress/in_review/done), due_date, estimated_hours, 
   actual_hours, parent_task_id (FK - for subtasks), position (for ordering), 
   labels (JSON array), attachments (JSON array), created_at, updated_at

4. Comment: id, task_id (FK), user_id (FK), content (rich text), 
   mentions (JSON array of user_ids), edited_at, created_at

5. Sprint: id, project_id (FK), name, goal, start_date, end_date, 
   status (planning/active/completed), capacity_hours

6. TimeEntry: id, task_id (FK), user_id (FK), hours, description, date, created_at

7. ProjectMember: id, project_id (FK), user_id (FK), role (owner/admin/member/viewer), 
   joined_at

USER ROLES:
• Project Owner: Full project control, member management, delete project
• Project Admin: Edit project, manage tasks, assign members
• Member: Create/edit tasks, comment, log time
• Viewer: Read-only access to project

TECHNICAL FEATURES:
• Drag-and-drop task reordering (within and between columns)
• Real-time collaboration (WebSocket or polling for live updates)
• Markdown support in descriptions and comments
• @mentions with user autocomplete
• File upload with drag-and-drop
• Activity feed showing recent changes
• Email digests for daily activity
• Keyboard shortcuts for power users
• Bulk task operations (move, assign, delete)
• Task filtering (assignee, label, status, due date)
• Export project data (CSV, JSON)
• Dark mode support
• Responsive: Full desktop experience, mobile-optimized task view
```

---

### 4. Healthcare Appointment System

```
Create a comprehensive healthcare appointment scheduling and patient management system.

PATIENT FEATURES:
• Online appointment booking with doctor selection
• Calendar view of available time slots
• Appointment reminders (email/SMS)
• Patient portal (view appointments, medical history, prescriptions)
• Insurance information management
• Upload medical documents (test results, scans)
• Telemedicine support (video consultation links)
• Prescription refill requests
• Bill payment online

DOCTOR/STAFF FEATURES:
• Daily schedule view with appointment list
• Patient chart access with medical history
• Appointment management (confirm, reschedule, cancel)
• Patient notes and diagnosis entry
• Prescription generation
• Lab test ordering
• Availability calendar management
• Patient search and quick access

ADMIN FEATURES:
• Staff and doctor management
• Department and specialization setup
• Appointment slot configuration
• Billing and insurance processing
• Reports (appointments by doctor, revenue, patient visits)
• Patient registration
• Room and resource allocation
• Email/SMS notification templates

KEY ENTITIES:
1. Patient: id, medical_record_number (unique), first_name, last_name, 
   date_of_birth, gender, email, phone, address (JSON), emergency_contact (JSON), 
   insurance_provider, insurance_id, blood_type, allergies (JSON array), 
   chronic_conditions (JSON array), created_at

2. Doctor: id, first_name, last_name, email, phone, specialization, 
   license_number, bio, photo_url, consultation_fee, years_of_experience, 
   rating, review_count, is_available

3. Appointment: id, patient_id (FK), doctor_id (FK), appointment_date, 
   start_time, end_time, type (in_person/telemedicine), status 
   (scheduled/confirmed/completed/cancelled/no_show), reason_for_visit, 
   chief_complaint, notes, diagnosis, prescriptions (JSON), 
   follow_up_required, follow_up_date, created_at

4. MedicalRecord: id, patient_id (FK), doctor_id (FK), visit_date, 
   diagnosis, symptoms (JSON), vitals (JSON: BP, temp, pulse, etc.), 
   treatment_plan, prescriptions (JSON), lab_tests_ordered (JSON), 
   notes, attachments (JSON array), created_at

5. Prescription: id, patient_id (FK), doctor_id (FK), appointment_id (FK), 
   medication_name, dosage, frequency, duration, instructions, 
   refills_allowed, pharmacy_notes, issued_date, expiry_date

6. TimeSlot: id, doctor_id (FK), day_of_week (0-6), start_time, end_time, 
   slot_duration_minutes, max_patients_per_slot, is_available

7. Bill: id, patient_id (FK), appointment_id (FK), consultation_fee, 
   lab_charges, medication_charges, other_charges, subtotal, tax, 
   discount, total_amount, payment_status (pending/paid/refunded), 
   payment_method, payment_date, insurance_claim_amount

TECHNICAL REQUIREMENTS:
• HIPAA compliance considerations (data encryption, audit logging)
• Appointment conflict detection
• Automated reminder system (24h before, 1h before)
• Calendar integration (iCal export)
• SMS gateway integration (Twilio - mock)
• Video call integration (Zoom/Google Meet links)
• E-prescription generation (PDF with QR code)
• Medical document viewer (PDF, DICOM images)
• Search patients by name, MRN, phone
• Appointment statistics dashboard
• Billing and invoice generation
```

---

### 5. Real Estate Listing Platform

```
Build a property listing and real estate marketplace with buyer and agent features.

BUYER FEATURES:
• Property search with map view
• Advanced filters (price, bedrooms, bathrooms, sqft, type, amenities)
• Property detail pages with photo gallery, virtual tour, floor plans
• Save favorite properties
• Schedule property viewings
• Mortgage calculator
• Neighborhood information (schools, transit, amenities)
• Compare properties side-by-side
• Saved searches with email alerts for new listings
• Contact agent through inquiry form
• Buyer registration and profile

AGENT/SELLER FEATURES:
• Property listing management (CRUD with photos)
• Lead management (inquiries, viewing requests)
• Agent profile with listings and reviews
• Calendar for property viewings
• Analytics (listing views, inquiries, favorites)
• Bulk photo upload with reordering
• Featured listing promotion
• Open house scheduling
• Client relationship management
• Commission tracking

ADMIN FEATURES:
• Agent approval and verification
• Property moderation and approval
• User management
• Featured listings management
• Site analytics (traffic, conversions)
• Commission and payment processing
• Email campaign management
• Report generation

KEY ENTITIES:
1. Property: id, listing_id (unique), title, description, property_type 
   (house/condo/townhouse/land), listing_type (sale/rent), price, 
   price_per_sqft, bedrooms, bathrooms, sqft, lot_size, year_built, 
   address (JSON with geocoding), latitude, longitude, amenities (JSON array), 
   features (JSON: parking, pool, etc.), photos (JSON array with order), 
   virtual_tour_url, floor_plan_urls (JSON), agent_id (FK), 
   status (active/pending/sold/rented/archived), views_count, 
   favorites_count, listed_date, last_updated, created_at

2. Agent: id, user_id (FK), license_number, agency_name, bio, photo_url, 
   phone, email, specializations (JSON), areas_served (JSON), 
   rating, review_count, verified, total_sales, years_of_experience, 
   languages_spoken (JSON)

3. User: id, email (unique), password_hash, first_name, last_name, phone, 
   role (buyer/agent/admin), is_verified, created_at

4. Favorite: id, user_id (FK), property_id (FK), created_at

5. Inquiry: id, property_id (FK), user_id (FK - nullable for guests), 
   name, email, phone, message, inquiry_type (viewing/info/offer), 
   preferred_date, preferred_time, status (new/contacted/scheduled/closed), 
   agent_response, created_at, responded_at

6. Viewing: id, property_id (FK), agent_id (FK), buyer_id (FK), 
   scheduled_date, scheduled_time, duration_minutes, 
   status (scheduled/confirmed/completed/cancelled), notes, created_at

7. Review: id, agent_id (FK), reviewer_id (FK), property_id (FK - optional), 
   rating (1-5), title, comment, verified_transaction, created_at

TECHNICAL REQUIREMENTS:
• Map integration (Google Maps or Mapbox) with property markers
• Geocoding for address to coordinates
• Image optimization and thumbnail generation
• Advanced search with Elasticsearch or similar
• Email alerts for saved search criteria
• Virtual tour embedding (Matterport, YouTube 360)
• Mortgage calculator with amortization schedule
• Neighborhood data API integration (schools, crime rates)
• Mobile-responsive with swipeable photo galleries
• SEO optimization for property pages
• Social sharing with Open Graph tags
• Real-time availability updates
```

---

## 🎓 Tips for Maximum Quality

### 1. **Be Specific About Data**
❌ "Store user information"
✅ "Store: first_name, last_name, email (unique, validated), phone (optional), date_of_birth, avatar_url, bio (500 char max), preferences (JSON)"

### 2. **Define Relationships Clearly**
❌ "Users have posts"
✅ "User (1) → (Many) Posts relationship via user_id foreign key. Each post must have exactly one author. Cascade delete posts when user is deleted."

### 3. **Specify User Interactions**
❌ "Users can filter data"
✅ "Add filters for: date range (from/to), status (dropdown), search by name (debounced input), sort by created_at or name (toggle ASC/DESC)"

### 4. **Include Edge Cases**
❌ "Handle errors"
✅ "Handle: network timeout (retry 3x), 404 (show 'not found' page), 401 (redirect to login), duplicate email (show inline error), empty results (show 'no data' illustration)"

### 5. **Provide UI/UX Details**
❌ "Show a form"
✅ "Multi-step form: Step 1 (Basic Info), Step 2 (Details), Step 3 (Review). Show progress bar. Validate on blur. Disable 'Next' until step is valid. Allow 'Back' navigation. Save draft to localStorage."

---

## 🚀 How to Use These Templates

### In VS Code Extension:
1. Copy one of the templates above
2. Customize the placeholders [IN_BRACKETS]
3. Upload your UI mockup image
4. Paste the customized template in the description field
5. Click "Generate"

### Via API:
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "base64_image_here",
    "description": "PASTE_TEMPLATE_HERE",
    "tech_stack": {
      "frontend": "React",
      "backend": "FastAPI",
      "database": "PostgreSQL"
    },
    "project_name": "your-project-name"
  }'
```

---

## 📞 Support

If you need help customizing templates or want to add new ones, please:
1. Check the examples above
2. Review `/docs/PROMPT_ENGINEERING.md`
3. Test with similar existing templates
4. Submit issues/PRs to improve templates

**Happy Generating! 🎉**

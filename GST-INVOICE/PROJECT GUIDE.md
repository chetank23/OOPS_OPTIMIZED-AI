PoC Assignment: Compliance Helper for MSME GST & E-Invoicing

Course: AI Application Development (6th Semester, Computer Science)
Team Size: 6 members
Duration: 6 weeks (Project-based PoC)

1. Project Summary

Build a proof-of-concept AI system that assists Micro, Small, and Medium Enterprises (MSMEs) in managing GST compliance and e-invoicing reconciliation.

The system should:

Automatically extract invoice data from PDFs/images

Reconcile them with GST/e-invoice records

Flag mismatches or compliance risks for review

2. Problem Statement (One Line)

MSMEs struggle with GST compliance due to manual invoice handling, frequent mismatches, and lack of affordable, easy-to-use reconciliation tools.

3. Customers / Stakeholders

MSME owners and finance teams

Chartered Accountants (CAs) and tax consultants

Small manufacturing and trading firms

Accounting service providers

4. Why This is an Open Opportunity

GST systems are mature, but MSMEs still rely on spreadsheets/manual accounting

Existing enterprise tools are:

Expensive

Complex

Indian invoices are often:

Images

Inconsistent PDFs

A lightweight AI-driven compliance helper tailored to MSMEs is still missing

5. MVP Scope (Must Be Completed in 6 Weeks)

The MVP should include:

Upload of GST invoices (PDF or image formats)

OCR-based extraction of invoice fields:

GSTIN

Invoice number

Date

Taxable value

Tax amounts

Validation of extracted fields against expected GST rules

Reconciliation logic to match purchase and sales invoices

Flagging of:

Mismatches

Missing invoices

Potential compliance issues

Exportable reconciliation report (CSV/Excel)

6. Suggested Technical Architecture

Frontend:

Web UI using React or Streamlit

Target users: Accountants and MSME users

Backend:

FastAPI or Flask

Handles:

Document processing

Reconciliation logic

OCR:

Tesseract OCR or cloud OCR (for PoC)

AI / ML:

Rule-based validation

ML-based invoice field classification

Data Storage:

SQLite / PostgreSQL

Stores invoices and reconciliation results

Optional:

Mock GST/e-invoice API integration for validation

7. Data & Ethical Considerations

Use anonymized or synthetic invoice data during development

Avoid storing sensitive financial data beyond PoC needs

Clearly indicate:

Limitations

Confidence of extracted values

Treat outputs as:

Compliance assistance

NOT legal advice

8. Deliverables (End of 6 Weeks)

Functional GST compliance helper PoC

Dashboard showing:

Reconciliation status

Issues

Demo video (4–6 minutes)

Technical report (2–4 pages)

Source code repository with setup instructions

9. Week-by-Week Execution Plan

Week 1:

Understand GST workflow

Collect sample invoices

Define validation rules

Week 2:

Implement invoice upload

OCR extraction

Week 3:

Field validation

Rule-based checks

Week 4:

Reconciliation logic

Dashboard

Week 5:

Testing with:

Varied invoice formats

Edge cases

Week 6:

Final demo

Documentation

Evaluation

10. Evaluation Rubric (100 Points)

Problem understanding & domain clarity – 20 points

Invoice extraction accuracy – 25 points

Reconciliation & rule logic – 20 points

Usability & reporting – 15 points

Documentation & demo – 20 points

11. Demo Scenario

Upload a batch of GST invoices

Demonstrate automatic extraction

Show:

Matched invoices

Mismatched invoices

Generate reconciliation report

12. Stretch Goals (Optional)

Support e-invoice JSON ingestion

Add GST return form suggestions (GSTR-1, GSTR-2B mapping)

Multi-language invoice OCR

Risk scoring for compliance issues

Prepared by:
AI Application Development Course Instructor
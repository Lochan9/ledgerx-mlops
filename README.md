<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python">
  <img src="https://img.shields.io/badge/DVC-Data%20Version%20Control-green?logo=dvc">
  <img src="https://img.shields.io/badge/Pytest-Tests%20Passing-brightgreen?logo=pytest">
  <img src="https://img.shields.io/badge/License-MIT-black?logo=open-source-initiative">
</p>

<h1 align="center">🧾 LedgerX – AI-Powered Invoice & Receipt Intelligence Platform</h1>
<h3 align="center">Milestone 1 · SROIE 2019 Receipt Pipeline · DVC + Pytest · Reproducible MLOps Workflow</h3>

---

## 📘 Overview
*LedgerX* is an *AI-driven financial-document understanding platform* that automates how invoices, receipts, and credit notes are read, cleaned, and analyzed.  
This repository covers *Milestone 1, where a **reproducible, version-controlled data pipeline* is implemented using the *SROIE 2019 (Task 2)* dataset.

*Milestone 1 objectives*
- Parse raw SROIE JSON annotations  
- Clean and normalize company, date, total fields  
- Create train/val/test splits  
- Version all artifacts with *DVC*  
- Validate pipeline with *Pytest*

---

## 🧠 Business Context
LedgerX processes:
| Document Type | Examples | Goal |
|----------------|-----------|------|
| *Invoices* | Vendor purchase orders | Record payables |
| *Receipts* | Grocery, electronics, restaurant | Record expenses |
| *Credit Notes* | Refunds / adjustments | Reverse liabilities |

Milestone 1 focuses on *Receipts* (retail bills) using SROIE Task 2.

---

## 🧩 Dataset – SROIE 2019
*Scanned Receipts OCR and Information Extraction (ICDAR 2019)*  
626 receipts, each with one JSON label file.

*Example*
```json
{
  "company": "BOOK TA (TAMAN DAYA) SDN BHD",
  "date": "25/12/2018",
  "address": "NO.53 55,57 & 59, JALAN SAGU 18, TAMAN DAYA, JOHOR.",
  "total": "9.00"
}
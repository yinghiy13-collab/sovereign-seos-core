# 🛡️ Sovereign SEOS Core: Fail-Closed Evidence-Gated Pipeline

[![SEOS Pipeline](https://github.com/yinghiy13-collab/sovereign-seos-core/actions/workflows/seos-pipeline.yml/badge.svg)](https://github.com/yinghiy13-collab/sovereign-seos-core/actions/workflows/seos-pipeline.yml)
[![Status](https://img.shields.io/badge/Status-PROPOSED-orange.svg)](#)
[![Security](https://img.shields.io/badge/Security-Fail--Closed-red.svg)](#)
[![Ed25519](https://img.shields.io/badge/Crypto-Ed25519-blue.svg)](#)

**Sovereign SEOS Core** คือระบบ CI/CD Pipeline ระดับ Enterprise ที่ออกแบบภายใต้ปรัชญา **Zero-Trust** และ **Fail-Closed** (ไม่มีหลักฐาน = ไม่มีการปล่อยผ่าน) โดยใช้สถาปัตยกรรม L1-L7 เพื่อตรวจสอบความสมบูรณ์ของซอฟต์แวร์ตั้งแต่ระดับ AST ไปจนถึงการลงนามทางดิจิทัล

---

## 🏗️ Architecture: The L1-L7 Pipeline

ระบบจะปฏิเสธการ Release (DENY) ทันทีหาก Layer ใด Layer หนึ่งล้มเหลว:

| Layer | Name | Description | Output Artifact |
|-------|------|-------------|-----------------|
| **L1** | `AST Scan` | ตรวจสอบ Static Code เพื่อหาคำสั่งอันตราย (`eval`, `exec`, forbidden imports) | `l1_ast.json` |
| **L4** | `Rego Policy` | ใช้ Open Policy Agent (OPA) บังคับใช้กฎสถาปัตยกรรมและการตรวจสอบ Metadata | `l4_rego.json` |
| **L5** | `Ed25519 Witness` | สร้างลายเซ็นดิจิทัลแบบ Asymmetric (k-of-n quorum) เพื่อยืนยันความถูกต้อง | `l5_witness.json` |
| **L6** | `Tamper Test` | ทดสอบการโจมตี (Differential Testing) จำลองการแก้ไฟล์/ปลอมลายเซ็น ระบบต้องจับได้ | `l6_tamper.json` |
| **L7** | `Release Gate` | รวบรวม Evidence ทั้งหมด Hash รวมกัน (SHA-256) และตัดสินใจแบบ Default-DENY | `release_decision.json` |

---

## 🚀 Master Console Dashboard

ระบบมีหน้า Dashboard สำหรับให้ Stakeholder หรือ Auditor เข้ามาตรวจสอบสถานะการ Release แบบ Real-time (Interactive Fail-Closed Demo)

👉 **[เปิดดู Master Console ที่นี่](https://yinghiy13-collab.github.io/sovereign-seos-core/)**

---

## 🔒 Security Principles (Zero-Trust)

1.  **No Evidence = No Claim:** ทุกการตัดสินใจต้องมี Artifact รองรับ
2.  **Cryptographic Quorum:** การลงนามต้องมี Ed25519 Signature ครบตาม Threshold (k=2, n=3) ลายเซ็นปลอมหรือการทำซ้ำจะถูกปฏิเสธ
3.  **Immutable Evidence:** ค่า `evidence_digest` ที่ได้จาก L7 ถูก Hash จากทุก Report ย่อย (ถ้ามีการแก้แม้แต่ไบต์เดียว Hash จะเปลี่ยนทันที)
4.  **Default DENY:** ฟังก์ชัน `release_authorization` จะเป็น `DENY` เสมอ ตราบใดที่ยังไม่ผ่านกระบวนการ **Independent Verification** จากบุคคลภายนอก

---

## ⚠️ Current Status: `PROPOSED`

> 🔴 **INDEPENDENT_VERIFICATION = NOT_RUN**
> 🔴 **RELEASE_AUTHORIZATION = DENY**

Repo นี้อยู่ในสถานะ **PROPOSED** ยังไม่ถือว่าเสร็จสมบูรณ์ (FROZEN) จนกว่าจะมีผู้ตรวจสอบที่เป็นอิสระ (Independent Verifier) ซึ่งไม่ใช่ผู้เขียนโค้ด เข้ามารัน Pipeline และเซ็นรับรอง Digest 

*(ดูรายละเอียดเกณฑ์การรับรองได้ที่ `SKILL.md` และ `memory.yaml`)*

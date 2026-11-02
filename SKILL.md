---
name: seos-core-skill
description: Master standard for the Blue Prince repo baseline pipeline. Use when verifying, extending or releasing SEOS-H / Blue Prince artifacts under a fail-closed, evidence-gated policy (AST scan, Rego policy, multi-sig witness, tamper test, release gate).
version: v100
status: PROPOSED
---

# SEOS-Core-SKILL v100 — Blue Prince Master Standard

> สถานะ: **PROPOSED**. คำว่า FROZEN ใช้ได้เมื่อ (1) CI ทุก job เขียวบน commit ที่ระบุ
> (2) บันทึก digest ลง `evidence_manifest.json` (3) มี Independent Verification จริง
> ปัจจุบัน `INDEPENDENT_VERIFICATION = NOT_RUN`, `RELEASE_AUTHORIZATION = DENY`.

## 1. Purpose
กำหนดมาตรฐานเดียวสำหรับ repo baseline และ pipeline ของ Blue Prince / SEOS-H
โดยใช้หลัก **Preservation-First**: `DISCOVER → UNDERSTAND → PRESERVE → ANALYZE → EVOLVE → VERIFY`
และ **Fail-Closed**: `NO_EVIDENCE → NO_CLAIM → NO_TRUST → NO_RELEASE`

## 2. Invariants
| ID | Rule |
|----|------|
| I-01 | ไม่มีหลักฐาน = ไม่มี claim (ห้ามเขียนว่า "ผ่าน" โดยไม่มี artifact อ้างอิง) |
| I-02 | ค่าเริ่มต้นของทุก gate = DENY; ต้องมีหลักฐานครบจึงเปลี่ยนเป็น ALLOW |
| I-03 | ทุกข้อเรียกร้องแยกเป็น FACT / ASSERTION / INFERENCE / UNKNOWN |
| I-04 | พฤติกรรมเดิมที่ตรวจแล้วต้องไม่ถูกทำลาย (regression ต้องผ่านก่อน merge) |
| I-05 | Rebuild/Replace ต้องมี justification + impact analysis เป็นลายลักษณ์อักษร |
| I-06 | Memory เป็นข้อมูลอ้างอิง ไม่ใช่ความจริง ต้อง re-verify ทุกครั้งที่เปิดงานใหม่ |
| I-07 | ไฟล์ที่ขาด, script ที่ไม่มี, หรือผลลัพธ์ที่อ่านไม่ได้ = FAIL ไม่ใช่ SKIP |

## 3. Pipeline Layers
| Layer | ชื่อ | หน้าที่ | Output | Fail ถ้า |
|-------|------|--------|--------|---------|
| L1 | AST Scan | วิเคราะห์ Static AST: import ต้องห้าม, `eval/exec` | `reports/l1_ast.json` | พบ violation, Parse error, หรือ Empty target |
| L4 | Rego Policy | `opa eval` ตรวจ policy กับ report L1 | `reports/l4_rego.json` | `allow != true` หรือ OPA error |
| L5 | Multi-Sig Witness | จำลอง k-of-n witness ลงนามบน manifest digest | `reports/l5_witness.json` | ลายเซ็น < k หรือ digest ไม่ตรง |
| L6 | Differential Tamper | แก้ไข artifact ตั้งใจ แล้วต้องถูกปฏิเสธ | `reports/l6_tamper.json` | ระบบยัง ALLOW หลังถูก tamper |
| L7 | Release Gate | รวมผลทุก layer; ถ้าไม่ครบ = DENY | `reports/release_decision.json` | ขาด report ใด ๆ |

หมายเหตุ: L5 เป็น **simulation** พิสูจน์ตรรกะเท่านั้น ไม่ใช่ความน่าเชื่อถือเชิงเข้ารหัสในโลกจริง

## 4. Non-goals / ข้อจำกัด
- skill นี้ไม่รับประกันความปลอดภัยของระบบ ใช้ลด false claim และ regression เท่านั้น
- ไม่ใช่การรับรองจากบุคคลที่สามจนกว่าจะมี Independent Verification

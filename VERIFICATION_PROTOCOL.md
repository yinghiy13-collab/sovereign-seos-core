# 🔍 SEOS Independent Verification Protocol (SIVP) v1.0

**Objective:** เพื่อกำหนดมาตรฐานและขั้นตอนการตรวจสอบความถูกต้องของ SEOS Core Pipeline โดยบุคคลภายนอก (Independent Verifier) ที่ไม่ใช่ผู้พัฒนา (Author) เพื่อปลดล็อกเงื่อนไข `INDEPENDENT_VERIFICATION = NOT_RUN` ใน L7 Release Gate

> **Definition of Independent:** ผู้ตรวจสอบต้องไม่ใช่ `yinghiy13-collab` หรือผู้ที่มีสิทธิ์เขียนโค้ด (Write Access) ใน Repository นี้

---

## 🛠️ Prerequisites (เครื่องมือที่ต้องมี)

ผู้ตรวจสอบจำเป็นต้องติดตั้งเครื่องมือต่อไปนี้ในเครื่องของตน:
- [Git](https://git-scm.com/)
- [Python 3.12+](https://www.python.org/)
- [Open Policy Agent (OPA) v0.68.0](https://www.openpolicyagent.org/docs/latest/#running-opa)
- `pip install cryptography`

---

## 📋 Step-by-Step Verification Protocol

### Step 1: Audit the Source Code (ตรวจสอบโค้ดต้นฉบับ)
ผู้ตรวจสอบต้องอ่านและทำความเข้าใจโค้ดหลัก 3 ไฟล์ เพื่อยืนยันว่าไม่มี Backdoor หรือช่องโหว่:
1. `.github/workflows/seos-pipeline.yml` (ตรวจสอบว่าไม่มีการส่งข้อมูลออกภายนอก)
2. `tools/witness_ed25519.py` (ตรวจสอบว่า Logic การเซ็นและตรวจสอบ Quorum ถูกต้อง)
3. `tools/tamper_test.py` (ตรวจสอบว่า Test เคสการโจมตีครอบคลุมจริง)

### Step 2: Reproduce the Pipeline (รัน Pipeline ซ้ำ)
ผู้ตรวจสอบต้องรัน Pipeline ด้วยตนเองจาก Commit ที่ระบุใน Release Artifact:
1. Clone Repository ลงเครื่อง Local
2. สร้าง Virtual Environment และติดตั้ง Dependencies (`pip install cryptography`)
3. รันสคริปต์ L5 (Witness) เพื่อสร้าง Manifest และลายเซ็น Ed25519 ใหม่:
   ```bash
   python tools/witness_ed25519.py --k 2 --n 3 --out reports/l5_witness.json

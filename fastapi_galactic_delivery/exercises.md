# Galactic Delivery API — แบบฝึกหัด FastAPI 30 Levels

แบบฝึกหัดนี้สร้าง API เดียวแบบสะสม ตั้งแต่ endpoint แรกจนถึงระบบพัสดุ ภารกิจ การตรวจความพร้อม และ API Key

## เตรียมโปรเจกต์

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell ใช้คำสั่งเปิด environment:

```powershell
.venv\Scripts\Activate.ps1
```

## วิธีทำ

1. เปิด `student_app.py` และทำ TODO ตามลำดับ
2. เปิด server ด้วย `uvicorn student_app:app --reload`
3. ทดลองผ่าน Swagger UI ที่ `http://127.0.0.1:8000/docs`
4. ตรวจงานทั้งหมดด้วย `pytest -q`
5. ตรวจเฉลยด้วย `APP_MODULE=solution_app pytest -q`

ทำเฉพาะ Level ได้ด้วยตัวอย่าง:

```bash
pytest -q -k level_10
```

> ทุก Level เชื่อมกัน หากฟังก์ชันต้นทางยังไม่สมบูรณ์ test ของ Level หลังอาจไม่ผ่านตามไปด้วย


---

## Level 1: เปิดศูนย์ API

**หัวข้อที่ฝึก:** FastAPI app + GET endpoint

### ภารกิจ

สร้าง endpoint แรก `GET /` สำหรับต้อนรับผู้ใช้ Galactic Delivery API

### ข้อกำหนด

- ใช้ decorator `@app.get("/")`
- สร้างฟังก์ชัน `read_root()`
- คืน dictionary ตามตัวอย่าง

### โค้ดทดสอบ

```python
response = client.get("/")
print(response.status_code)
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'message': 'ยินดีต้อนรับสู่ Galactic Delivery API'}
```

<details>
<summary>💡 คำใบ้</summary>

FastAPI จะแปลง dictionary ที่ return เป็น JSON response

</details>

---

## Level 2: ตรวจสถานะศูนย์

**หัวข้อที่ฝึก:** Global list + GET endpoint

> 🔗 Level นี้ต่อจาก Level 1–1

### ภารกิจ

สร้าง `GET /status` เพื่อรายงานว่าระบบออนไลน์และมีพัสดุกี่ชิ้น

### ข้อกำหนด

- สร้างฟังก์ชัน `get_status()`
- อ่านจำนวนจาก global list `packages`
- คืน key `status` และ `package_count`

### โค้ดทดสอบ

```python
packages.clear()
response = client.get("/status")
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
{'status': 'online', 'package_count': 0}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `len(packages)` เพื่อให้จำนวนเปลี่ยนตามข้อมูลจริง

</details>

---

## Level 3: เครื่องคิดค่าส่ง

**หัวข้อที่ฝึก:** Helper function + operator

> 🔗 Level นี้ต่อจาก Level 1–2

### ภารกิจ

สร้าง helper `calculate_shipping_cost(weight, fragile=False)` คิดกิโลกรัมละ 15 เครดิต และบวก 20 เครดิตเมื่อเป็นของเปราะบาง

### ข้อกำหนด

- รับน้ำหนักและ boolean
- ใช้ condition
- คืนค่าราคา ไม่ต้องสร้าง endpoint ใน Level นี้

### โค้ดทดสอบ

```python
print(calculate_shipping_cost(5))
print(calculate_shipping_cost(5, True))
```

### ผลลัพธ์ที่ต้องการ

```text
75
95
```

<details>
<summary>💡 คำใบ้</summary>

คำนวณราคาพื้นฐานก่อนตรวจ `fragile`

</details>

---

## Level 4: ค่าส่งผ่าน Query Parameter

**หัวข้อที่ฝึก:** Query parameter + validation

> 🔗 Level นี้ต่อจาก Level 1–3

### ภารกิจ

สร้าง `GET /shipping-cost` รับ `weight` และ `fragile` จาก query parameter แล้วเรียก helper จาก Level 3

### ข้อกำหนด

- กำหนด `weight` เป็น float ระหว่าง 0–20
- กำหนด `fragile` เริ่มต้นเป็น `False`
- ต้องเรียก `calculate_shipping_cost()`

### โค้ดทดสอบ

```python
response = client.get("/shipping-cost?weight=5&fragile=true")
print(response.status_code)
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'weight': 5.0, 'fragile': True, 'cost': 95.0}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `Query(gt=0, le=20)` เพื่อให้ FastAPI ตรวจข้อมูล

</details>

---

## Level 5: Checkpoint 1: ค้นหาดาวปลายทาง

**หัวข้อที่ฝึก:** Path parameter + HTTPException

> 🔗 Level นี้ต่อจาก Level 1–4

> 🛟 **Checkpoint:** ทบทวนและรัน test ของ Level ก่อนหน้าก่อนทำต่อ

### ภารกิจ

สร้าง `GET /planets/{planet_name}` เพื่อค้นหาระยะทางจาก `planet_distances`

### ข้อกำหนด

- รับ `planet_name` จาก path
- จัดชื่อด้วย `.strip().title()`
- ถ้าไม่พบให้ raise `HTTPException(404)`

### โค้ดทดสอบ

```python
print(client.get("/planets/Europa").json())
missing = client.get("/planets/Venus")
print(missing.status_code)
print(missing.json())
```

### ผลลัพธ์ที่ต้องการ

```text
{'planet': 'Europa', 'distance': 240}
404
{'detail': 'ไม่พบดาวปลายทาง'}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `if name not in planet_distances` ก่อนอ่านระยะทาง

</details>

---

## Level 6: สร้างแบบฟอร์มพัสดุ

**หัวข้อที่ฝึก:** Pydantic BaseModel + Field

> 🔗 Level นี้ต่อจาก Level 1–5

### ภารกิจ

สร้าง model `PackageCreate` เพื่อกำหนดรูปแบบ JSON ที่ใช้ลงทะเบียนพัสดุ

### ข้อกำหนด

- มี `name`, `weight`, `package_type`, `fragile`
- name ยาวอย่างน้อย 2 ตัวอักษร
- weight มากกว่า 0 และไม่เกิน 20
- fragile เริ่มต้นเป็น False

### โค้ดทดสอบ

```python
item = PackageCreate(
    name="Medicine", weight=5, package_type="Medical", fragile=True
)
print(item.model_dump())
```

### ผลลัพธ์ที่ต้องการ

```text
{'name': 'Medicine', 'weight': 5.0, 'package_type': 'Medical', 'fragile': True}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `Field(min_length=...)` และ `Field(gt=..., le=...)`

</details>

---

## Level 7: ลงทะเบียนพัสดุ

**หัวข้อที่ฝึก:** POST + request body + status code

> 🔗 Level นี้ต่อจาก Level 1–6

### ภารกิจ

สร้าง `POST /packages` รับ `PackageCreate` แล้วบันทึกลง global list

### ข้อกำหนด

- กำหนด status code เป็น 201
- สร้าง id ต่อจากจำนวนข้อมูล
- เรียก `calculate_shipping_cost()`
- เพิ่ม `status` เป็น `registered`

### โค้ดทดสอบ

```python
packages.clear()
response = client.post(
    "/packages",
    json={
        "name": "Medicine", "weight": 5,
        "package_type": "Medical", "fragile": True,
    },
)
print(response.status_code)
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
201
{'name': 'Medicine', 'weight': 5.0, 'package_type': 'Medical', 'fragile': True, 'id': 1, 'cost': 95.0, 'status': 'registered'}
```

<details>
<summary>💡 คำใบ้</summary>

เริ่มจาก `item.model_dump()` แล้วเพิ่ม key ของระบบ

</details>

---

## Level 8: ดูพัสดุทั้งหมด

**หัวข้อที่ฝึก:** GET collection endpoint

> 🔗 Level นี้ต่อจาก Level 1–7

### ภารกิจ

สร้าง `GET /packages` เพื่อคืนรายการพัสดุทั้งหมด

### ข้อกำหนด

- สร้างฟังก์ชัน `list_packages()`
- คืน global list `packages`
- ไม่สร้างข้อมูลตัวอย่างไว้ใน endpoint

### โค้ดทดสอบ

```python
packages.clear()
client.post(
    "/packages",
    json={"name": "Food", "weight": 8, "package_type": "Supply"},
)
response = client.get("/packages")
print(response.status_code)
print(len(response.json()))
print(response.json()[0]["name"])
```

### ผลลัพธ์ที่ต้องการ

```text
200
1
Food
```

<details>
<summary>💡 คำใบ้</summary>

FastAPI สามารถแปลง list of dictionaries เป็น JSON array ได้

</details>

---

## Level 9: ค้นหาพัสดุด้วย ID

**หัวข้อที่ฝึก:** Path parameter + loop + 404

> 🔗 Level นี้ต่อจาก Level 1–8

### ภารกิจ

สร้าง `GET /packages/{package_id}` เพื่อค้นหา dictionary ใน list

### ข้อกำหนด

- กำหนด `package_id` เป็น int
- ใช้ loop ค้นหา
- ถ้าไม่พบให้ตอบ 404

### โค้ดทดสอบ

```python
packages.clear()
client.post(
    "/packages",
    json={"name": "Food", "weight": 8, "package_type": "Supply"},
)
print(client.get("/packages/1").json()["name"])
print(client.get("/packages/99").status_code)
```

### ผลลัพธ์ที่ต้องการ

```text
Food
404
```

<details>
<summary>💡 คำใบ้</summary>

เปรียบเทียบ `package["id"]` กับ path parameter

</details>

---

## Level 10: Checkpoint 2: กรองพัสดุ

**หัวข้อที่ฝึก:** Optional query parameters + loop

> 🔗 Level นี้ต่อจาก Level 1–9

> 🛟 **Checkpoint:** ทบทวนและรัน test ของ Level ก่อนหน้าก่อนทำต่อ

### ภารกิจ

สร้าง `GET /packages-filter` เพื่อกรองด้วยประเภทและน้ำหนักสูงสุด

### ข้อกำหนด

- รับ `package_type` และ `max_weight` แบบ optional
- ใช้ loop และ conditions
- คืน list ใหม่โดยไม่แก้ข้อมูลเดิม

### โค้ดทดสอบ

```python
packages.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
client.post("/packages", json={"name": "Food", "weight": 12, "package_type": "Supply"})
response = client.get("/packages-filter?package_type=Medical&max_weight=10")
print(response.status_code)
print([item["name"] for item in response.json()])
```

### ผลลัพธ์ที่ต้องการ

```text
200
['Medicine']
```

<details>
<summary>💡 คำใบ้</summary>

เริ่ม `results = []` แล้วใช้ `continue` ข้ามรายการที่ไม่ผ่าน

</details>

---

## Level 11: แบบฟอร์มแก้ไขพัสดุ

**หัวข้อที่ฝึก:** Optional fields in Pydantic model

> 🔗 Level นี้ต่อจาก Level 1–10

### ภารกิจ

สร้าง model `PackageUpdate` ให้ทุก field เป็น optional เพื่อรองรับการแก้บางส่วน

### ข้อกำหนด

- มี `name`, `weight`, `package_type`, `fragile`, `status`
- ทุก field มี default เป็น None
- weight ยังต้องมากกว่า 0 และไม่เกิน 20

### โค้ดทดสอบ

```python
update = PackageUpdate(status="inspected")
print(update.model_dump(exclude_none=True))
```

### ผลลัพธ์ที่ต้องการ

```text
{'status': 'inspected'}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `Optional[type] = None` และ Field เฉพาะ weight

</details>

---

## Level 12: แก้ไขพัสดุ

**หัวข้อที่ฝึก:** PATCH + existing endpoint reuse

> 🔗 Level นี้ต่อจาก Level 1–11

### ภารกิจ

สร้าง `PATCH /packages/{package_id}` เพื่อแก้เฉพาะ field ที่ส่งมา

### ข้อกำหนด

- เรียก `get_package()` เพื่อค้นหา
- ใช้ `model_dump(exclude_none=True)`
- คำนวณ cost ใหม่เมื่อ weight หรือ fragile เปลี่ยน

### โค้ดทดสอบ

```python
packages.clear()
client.post("/packages", json={"name": "Food", "weight": 8, "package_type": "Supply"})
response = client.patch("/packages/1", json={"weight": 10, "status": "inspected"})
print(response.status_code)
print(response.json()["weight"])
print(response.json()["cost"])
print(response.json()["status"])
```

### ผลลัพธ์ที่ต้องการ

```text
200
10.0
150.0
inspected
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `.update(changes)` กับ dictionary เดิม

</details>

---

## Level 13: ลบพัสดุ

**หัวข้อที่ฝึก:** DELETE + list mutation

> 🔗 Level นี้ต่อจาก Level 1–12

### ภารกิจ

สร้าง `DELETE /packages/{package_id}` เพื่อลบพัสดุออกจากระบบ

### ข้อกำหนด

- เรียก `get_package()` ก่อนลบ
- ใช้ `packages.remove()`
- คืน id และข้อความยืนยัน

### โค้ดทดสอบ

```python
packages.clear()
client.post("/packages", json={"name": "Food", "weight": 8, "package_type": "Supply"})
response = client.delete("/packages/1")
print(response.json())
print(len(packages))
```

### ผลลัพธ์ที่ต้องการ

```text
{'deleted_id': 1, 'message': 'ลบพัสดุแล้ว'}
0
```

<details>
<summary>💡 คำใบ้</summary>

ถ้าไม่พบ `get_package()` จะสร้าง 404 ให้โดยอัตโนมัติ

</details>

---

## Level 14: สร้างสรุปห้องเก็บของ

**หัวข้อที่ฝึก:** Helper + loop + previous cost data

> 🔗 Level นี้ต่อจาก Level 1–13

### ภารกิจ

สร้าง helper `build_cargo_summary(package_list)` เพื่อรวมจำนวน น้ำหนัก และค่าส่ง

### ข้อกำหนด

- รับ list เป็น parameter
- ใช้ loop รวมน้ำหนักและ cost
- คืน dictionary สรุป

### โค้ดทดสอบ

```python
sample = [
    {"weight": 5, "cost": 95},
    {"weight": 8, "cost": 120},
]
print(build_cargo_summary(sample))
```

### ผลลัพธ์ที่ต้องการ

```text
{'package_count': 2, 'total_weight': 13, 'total_cost': 215}
```

<details>
<summary>💡 คำใบ้</summary>

อ่าน `weight` และ `cost` ที่ถูกสร้างโดย POST endpoint

</details>

---

## Level 15: Checkpoint 3: Cargo Summary API

**หัวข้อที่ฝึก:** Endpoint calls helper

> 🔗 Level นี้ต่อจาก Level 1–14

> 🛟 **Checkpoint:** ทบทวนและรัน test ของ Level ก่อนหน้าก่อนทำต่อ

### ภารกิจ

สร้าง `GET /cargo-summary` เพื่อคืนผลจาก helper Level 14

### ข้อกำหนด

- สร้างฟังก์ชัน `get_cargo_summary()`
- เรียก `build_cargo_summary(packages)`
- ห้ามคำนวณซ้ำใน endpoint

### โค้ดทดสอบ

```python
packages.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical", "fragile": True})
client.post("/packages", json={"name": "Food", "weight": 8, "package_type": "Supply"})
response = client.get("/cargo-summary")
print(response.status_code)
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'package_count': 2, 'total_weight': 13.0, 'total_cost': 215.0}
```

<details>
<summary>💡 คำใบ้</summary>

endpoint นี้มีหน้าที่รับ request และส่งต่อให้ helper

</details>

---

## Level 16: คำนวณเชื้อเพลิงตามดาว

**หัวข้อที่ฝึก:** Helper + dictionary + validation

> 🔗 Level นี้ต่อจาก Level 1–15

### ภารกิจ

สร้าง `calculate_required_fuel(destination)` โดยใช้ระยะทางจาก `planet_distances` และปัดขึ้นทุก 10 ปีแสง

### ข้อกำหนด

- จัดชื่อ destination
- ถ้าไม่พบดาวให้ raise 404
- คืนจำนวนเต็มของเชื้อเพลิง

### โค้ดทดสอบ

```python
print(calculate_required_fuel("Europa"))
print(calculate_required_fuel("Moon"))
```

### ผลลัพธ์ที่ต้องการ

```text
24
4
```

<details>
<summary>💡 คำใบ้</summary>

ใช้สูตร `(distance + 9) // 10`

</details>

---

## Level 17: สร้างแบบฟอร์มภารกิจ

**หัวข้อที่ฝึก:** Nested request data + Pydantic

> 🔗 Level นี้ต่อจาก Level 1–16

### ภารกิจ

สร้าง model `MissionCreate` สำหรับรับปลายทาง งบ เชื้อเพลิง และรายการ package IDs

### ข้อกำหนด

- destination เป็น str
- budget และ fuel มากกว่าหรือเท่ากับ 0
- package_ids เป็น list ของ int

### โค้ดทดสอบ

```python
mission_data = MissionCreate(
    destination="Europa", budget=400, fuel=30, package_ids=[1, 2]
)
print(mission_data.model_dump())
```

### ผลลัพธ์ที่ต้องการ

```text
{'destination': 'Europa', 'budget': 400.0, 'fuel': 30, 'package_ids': [1, 2]}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `Field(ge=0)` สำหรับตัวเลขที่อนุญาตให้เป็นศูนย์

</details>

---

## Level 18: สร้างภารกิจขนส่ง

**หัวข้อที่ฝึก:** POST + validation across resources

> 🔗 Level นี้ต่อจาก Level 1–17

### ภารกิจ

สร้าง `POST /missions` ตรวจดาวและ package IDs ก่อนบันทึกลง `missions`

### ข้อกำหนด

- เรียก `calculate_required_fuel()` เพื่อตรวจดาว
- เรียก `get_package()` ทุก id
- กำหนด status เป็น `planning` และตอบ 201

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
response = client.post(
    "/missions",
    json={"destination": "Europa", "budget": 400, "fuel": 30, "package_ids": [1]},
)
print(response.status_code)
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
201
{'destination': 'Europa', 'budget': 400.0, 'fuel': 30, 'package_ids': [1], 'id': 1, 'status': 'planning'}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ loop ตรวจ package IDs ก่อนสร้าง record

</details>

---

## Level 19: ค้นหาภารกิจ

**หัวข้อที่ฝึก:** GET by ID + reusable endpoint function

> 🔗 Level นี้ต่อจาก Level 1–18

### ภารกิจ

สร้าง `GET /missions/{mission_id}` เพื่อค้นหาภารกิจ

### ข้อกำหนด

- ใช้ loop
- คืนภารกิจเมื่อ id ตรงกัน
- ถ้าไม่พบตอบ 404

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
client.post("/missions", json={"destination": "Europa", "budget": 400, "fuel": 30, "package_ids": [1]})
print(client.get("/missions/1").json()["destination"])
print(client.get("/missions/99").status_code)
```

### ผลลัพธ์ที่ต้องการ

```text
Europa
404
```

<details>
<summary>💡 คำใบ้</summary>

รูปแบบเดียวกับ `get_package()` เพื่อให้ API สม่ำเสมอ

</details>

---

## Level 20: Checkpoint 4: ดึงพัสดุของภารกิจ

**หัวข้อที่ฝึก:** Helper + endpoint reuse + list

> 🔗 Level นี้ต่อจาก Level 1–19

> 🛟 **Checkpoint:** ทบทวนและรัน test ของ Level ก่อนหน้าก่อนทำต่อ

### ภารกิจ

สร้าง `get_mission_packages(mission)` เพื่อแปลง package IDs เป็นรายการ dictionary จริง

### ข้อกำหนด

- ใช้ loop วน `mission["package_ids"]`
- เรียก `get_package()` ทุก id
- คืน list ใหม่

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
client.post("/packages", json={"name": "Food", "weight": 8, "package_type": "Supply"})
client.post("/missions", json={"destination": "Europa", "budget": 400, "fuel": 30, "package_ids": [1, 2]})
mission = get_mission(1)
print([item["name"] for item in get_mission_packages(mission)])
```

### ผลลัพธ์ที่ต้องการ

```text
['Medicine', 'Food']
```

<details>
<summary>💡 คำใบ้</summary>

append ผลจาก `get_package(package_id)` ทีละรายการ

</details>

---

## Level 21: วิเคราะห์เหตุผลที่ยังไม่พร้อม

**หัวข้อที่ฝึก:** Helper orchestrates previous functions

> 🔗 Level นี้ต่อจาก Level 1–20

### ภารกิจ

สร้าง `mission_reasons(mission)` คืน list ของสาเหตุเมื่อของหนักเกิน งบไม่พอ หรือเชื้อเพลิงไม่พอ

### ข้อกำหนด

- เรียก `get_mission_packages()`
- เรียก `build_cargo_summary()`
- เรียก `calculate_required_fuel()`
- จำกัดน้ำหนักรวมไม่เกิน 60

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical", "fragile": True})
client.post("/missions", json={"destination": "Europa", "budget": 50, "fuel": 10, "package_ids": [1]})
print(mission_reasons(get_mission(1)))
```

### ผลลัพธ์ที่ต้องการ

```text
['งบประมาณไม่เพียงพอ', 'เชื้อเพลิงไม่เพียงพอ']
```

<details>
<summary>💡 คำใบ้</summary>

คำนวณ summary และ required fuel ครั้งเดียว แล้วตรวจแต่ละเงื่อนไข

</details>

---

## Level 22: Readiness Endpoint

**หัวข้อที่ฝึก:** Nested path + helper response

> 🔗 Level นี้ต่อจาก Level 1–21

### ภารกิจ

สร้าง `GET /missions/{mission_id}/readiness` เพื่อแสดงว่าภารกิจพร้อมหรือไม่

### ข้อกำหนด

- เรียก `get_mission()`
- เรียก `mission_reasons()`
- ready เป็น True เมื่อ reasons ว่าง

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
client.post("/missions", json={"destination": "Europa", "budget": 400, "fuel": 30, "package_ids": [1]})
response = client.get("/missions/1/readiness")
print(response.status_code)
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'mission_id': 1, 'ready': True, 'reasons': []}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `len(reasons) == 0`

</details>

---

## Level 23: บัญชีพัสดุแบบแบ่งหน้า

**หัวข้อที่ฝึก:** Pagination query parameters

> 🔗 Level นี้ต่อจาก Level 1–22

### ภารกิจ

สร้าง `GET /manifest` รับ `skip` และ `limit` เพื่อแบ่งหน้ารายการพัสดุ

### ข้อกำหนด

- skip เริ่มที่ 0 และห้ามติดลบ
- limit เริ่มที่ 10 อยู่ระหว่าง 1–20
- ใช้ list slicing

### โค้ดทดสอบ

```python
packages.clear()
for number in range(1, 4):
    client.post("/packages", json={"name": f"Box {number}", "weight": number, "package_type": "Supply"})
response = client.get("/manifest?skip=1&limit=1")
print(response.status_code)
print([item["name"] for item in response.json()["items"]])
```

### ผลลัพธ์ที่ต้องการ

```text
200
['Box 2']
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `packages[skip : skip + limit]`

</details>

---

## Level 24: ปล่อยยานออกเดินทาง

**หัวข้อที่ฝึก:** POST action + state mutation

> 🔗 Level นี้ต่อจาก Level 1–23

### ภารกิจ

สร้าง `POST /missions/{mission_id}/launch` ตรวจ readiness แล้วอัปเดต mission และพัสดุ

### ข้อกำหนด

- เรียก `get_mission()` และ `mission_reasons()`
- ถ้าไม่พร้อมตอบ 400
- หัก fuel และเปลี่ยน mission status
- อัปเดตพัสดุเป็น `in_transit`

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
client.post("/missions", json={"destination": "Europa", "budget": 400, "fuel": 30, "package_ids": [1]})
response = client.post("/missions/1/launch")
print(response.status_code)
print(response.json())
print(client.get("/packages/1").json()["status"])
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'mission_id': 1, 'status': 'launched', 'fuel_left': 6}
in_transit
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ `get_mission_packages()` เพื่ออัปเดตพัสดุของภารกิจเท่านั้น

</details>

---

## Level 25: Checkpoint 5: Mission Control

**หัวข้อที่ฝึก:** Integrated endpoint

> 🔗 Level นี้ต่อจาก Level 1–24

> 🛟 **Checkpoint:** ทบทวนและรัน test ของ Level ก่อนหน้าก่อนทำต่อ

### ภารกิจ

สร้าง `GET /mission-control/{mission_id}` เพื่อรวมภารกิจ cargo summary และ readiness ใน response เดียว

### ข้อกำหนด

- เรียก `get_mission()`
- เรียก `get_mission_packages()` และ `build_cargo_summary()`
- เรียก `mission_reasons()`

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
client.post("/missions", json={"destination": "Mars", "budget": 200, "fuel": 20, "package_ids": [1]})
response = client.get("/mission-control/1")
print(response.status_code)
print(response.json()["cargo"])
print(response.json()["ready"])
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'package_count': 1, 'total_weight': 5.0, 'total_cost': 75.0}
True
```

<details>
<summary>💡 คำใบ้</summary>

ประกอบ dictionary จากผลลัพธ์ของฟังก์ชันเดิม ไม่คำนวณสูตรซ้ำ

</details>

---

## Level 26: ติดตามพัสดุ

**หัวข้อที่ฝึก:** Endpoint function reuse

> 🔗 Level นี้ต่อจาก Level 1–25

### ภารกิจ

สร้าง `GET /tracking/{package_id}` เพื่อแสดงข้อความติดตามจากข้อมูลพัสดุ

### ข้อกำหนด

- เรียก `get_package()`
- คืน id, name, status และข้อความภาษาไทย
- ไม่ loop ค้นหาใหม่

### โค้ดทดสอบ

```python
packages.clear()
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical"})
response = client.get("/tracking/1")
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
{'id': 1, 'name': 'Medicine', 'status': 'registered', 'message': 'Medicine อยู่ในสถานะ registered'}
```

<details>
<summary>💡 คำใบ้</summary>

สร้างข้อความจาก `package['name']` และ `package['status']`

</details>

---

## Level 27: ตรวจ API Key

**หัวข้อที่ฝึก:** Header + reusable dependency

> 🔗 Level นี้ต่อจาก Level 1–26

### ภารกิจ

สร้าง dependency `verify_api_key()` เพื่อตรวจ header `X-API-Key`

### ข้อกำหนด

- รับค่าด้วย `Header`
- ถ้าค่าไม่ใช่ `galaxy-123` ให้ตอบ 401
- คืน key เมื่อถูกต้อง

### โค้ดทดสอบ

```python
try:
    verify_api_key("wrong-key")
except HTTPException as error:
    print(error.status_code)
    print(error.detail)
print(verify_api_key("galaxy-123"))
```

### ผลลัพธ์ที่ต้องการ

```text
401
API Key ไม่ถูกต้อง
galaxy-123
```

<details>
<summary>💡 คำใบ้</summary>

ชื่อ parameter `x_api_key` จะถูกแปลงเป็น header `X-API-Key`

</details>

---

## Level 28: รายงานผู้ดูแลระบบ

**หัวข้อที่ฝึก:** Depends + protected endpoint

> 🔗 Level นี้ต่อจาก Level 1–27

### ภารกิจ

สร้าง `GET /admin/report` ที่เปิดใช้เฉพาะ request ที่ผ่าน `verify_api_key`

### ข้อกำหนด

- ใช้ `Depends(verify_api_key)`
- เรียก `build_cargo_summary()`
- คืนจำนวนภารกิจเพิ่มด้วย

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Food", "weight": 8, "package_type": "Supply"})
denied = client.get("/admin/report")
allowed = client.get("/admin/report", headers={"X-API-Key": "galaxy-123"})
print(denied.status_code)
print(allowed.status_code)
print(allowed.json())
```

### ผลลัพธ์ที่ต้องการ

```text
401
200
{'package_count': 1, 'total_weight': 8.0, 'total_cost': 120.0, 'mission_count': 0}
```

<details>
<summary>💡 คำใบ้</summary>

parameter dependency ไม่จำเป็นต้องนำไปใช้ในฟังก์ชัน แต่ FastAPI จะเรียกตรวจให้ก่อน

</details>

---

## Level 29: รีเซ็ตศูนย์ควบคุม

**หัวข้อที่ฝึก:** Protected DELETE + shared state

> 🔗 Level นี้ต่อจาก Level 1–28

### ภารกิจ

สร้าง `DELETE /admin/reset` เพื่อล้าง packages และ missions โดยต้องมี API Key

### ข้อกำหนด

- ใช้ `Depends(verify_api_key)`
- เรียก `.clear()` กับ list ทั้งสอง
- คืนจำนวนข้อมูลหลังล้าง

### โค้ดทดสอบ

```python
packages.clear()
missions.clear()
client.post("/packages", json={"name": "Food", "weight": 8, "package_type": "Supply"})
response = client.delete("/admin/reset", headers={"X-API-Key": "galaxy-123"})
print(response.status_code)
print(response.json())
print(client.get("/status").json())
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'message': 'รีเซ็ตระบบแล้ว', 'packages': 0, 'missions': 0}
{'status': 'online', 'package_count': 0}
```

<details>
<summary>💡 คำใบ้</summary>

ใช้ dependency รูปแบบเดียวกับ admin report

</details>

---

## Level 30: Final Checkpoint: รายงานภารกิจฉบับเต็ม

**หัวข้อที่ฝึก:** End-to-end API composition

> 🔗 Level นี้ต่อจาก Level 1–29

> 🛟 **Checkpoint:** ทบทวนและรัน test ของ Level ก่อนหน้าก่อนทำต่อ

### ภารกิจ

สร้าง `GET /missions/{mission_id}/full-report` รวมข้อมูลภารกิจ พัสดุ ราคา เชื้อเพลิง และ readiness

### ข้อกำหนด

- เรียก `get_mission()`
- เรียก `get_mission_packages()` และ `build_cargo_summary()`
- เรียก `calculate_required_fuel()` และ `mission_reasons()`
- ห้ามเขียนกฎเดิมซ้ำ

### โค้ดทดสอบ

```python
client.delete("/admin/reset", headers={"X-API-Key": "galaxy-123"})
client.post("/packages", json={"name": "Medicine", "weight": 5, "package_type": "Medical", "fragile": True})
client.post("/packages", json={"name": "Food", "weight": 8, "package_type": "Supply"})
client.post("/missions", json={"destination": "Europa", "budget": 400, "fuel": 30, "package_ids": [1, 2]})
response = client.get("/missions/1/full-report")
print(response.status_code)
print(response.json())
```

### ผลลัพธ์ที่ต้องการ

```text
200
{'mission_id': 1, 'destination': 'Europa', 'status': 'planning', 'packages': ['Medicine', 'Food'], 'cargo': {'package_count': 2, 'total_weight': 13.0, 'total_cost': 215.0}, 'required_fuel': 24, 'ready': True, 'reasons': []}
```

<details>
<summary>💡 คำใบ้</summary>

สร้างผลลัพธ์จาก helper ทั้งหมดที่มี แล้วคืน dictionary เดียว

</details>

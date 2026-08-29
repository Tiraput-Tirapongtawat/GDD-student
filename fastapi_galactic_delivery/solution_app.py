"""Galactic Delivery API — เฉลย

รัน API ด้วย: uvicorn solution_app:app --reload
เปิด Swagger UI ที่: http://127.0.0.1:8000/docs
"""


from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


app = FastAPI(title="Galactic Delivery API")
client = TestClient(app)

packages = []
missions = []
planet_distances = {
    "Europa": 240,
    "Mars": 120,
    "Moon": 40,
}


# -----------------------------------------------------------------------------
# Level 1: เปิดศูนย์ API
# -----------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "ยินดีต้อนรับสู่ Galactic Delivery API"}


# -----------------------------------------------------------------------------
# Level 2: ตรวจสถานะศูนย์
# -----------------------------------------------------------------------------
@app.get("/status")
def get_status():
    return {"status": "online", "package_count": len(packages)}


# -----------------------------------------------------------------------------
# Level 3: เครื่องคิดค่าส่ง
# -----------------------------------------------------------------------------
def calculate_shipping_cost(weight, fragile=False):
    cost = weight * 15
    if fragile:
        cost += 20
    return cost


# -----------------------------------------------------------------------------
# Level 4: ค่าส่งผ่าน Query Parameter
# -----------------------------------------------------------------------------
@app.get("/shipping-cost")
def get_shipping_cost(
    weight: float = Query(gt=0, le=20),
    fragile: bool = False,
):
    cost = calculate_shipping_cost(weight, fragile)
    return {"weight": weight, "fragile": fragile, "cost": cost}


# -----------------------------------------------------------------------------
# Level 5: Checkpoint 1: ค้นหาดาวปลายทาง
# -----------------------------------------------------------------------------
@app.get("/planets/{planet_name}")
def get_planet(planet_name: str):
    name = planet_name.strip().title()
    if name not in planet_distances:
        raise HTTPException(status_code=404, detail="ไม่พบดาวปลายทาง")
    return {"planet": name, "distance": planet_distances[name]}


# -----------------------------------------------------------------------------
# Level 6: สร้างแบบฟอร์มพัสดุ
# -----------------------------------------------------------------------------
class PackageCreate(BaseModel):
    name: str = Field(min_length=2)
    weight: float = Field(gt=0, le=20)
    package_type: str
    fragile: bool = False


# -----------------------------------------------------------------------------
# Level 7: ลงทะเบียนพัสดุ
# -----------------------------------------------------------------------------
@app.post("/packages", status_code=status.HTTP_201_CREATED)
def create_package(item: PackageCreate):
    record = item.model_dump()
    record["id"] = len(packages) + 1
    record["cost"] = calculate_shipping_cost(item.weight, item.fragile)
    record["status"] = "registered"
    packages.append(record)
    return record


# -----------------------------------------------------------------------------
# Level 8: ดูพัสดุทั้งหมด
# -----------------------------------------------------------------------------
@app.get("/packages")
def list_packages():
    return packages


# -----------------------------------------------------------------------------
# Level 9: ค้นหาพัสดุด้วย ID
# -----------------------------------------------------------------------------
@app.get("/packages/{package_id}")
def get_package(package_id: int):
    for package in packages:
        if package["id"] == package_id:
            return package
    raise HTTPException(status_code=404, detail="ไม่พบพัสดุ")


# -----------------------------------------------------------------------------
# Level 10: Checkpoint 2: กรองพัสดุ
# -----------------------------------------------------------------------------
@app.get("/packages-filter")
def filter_packages(
    package_type: Optional[str] = None,
    max_weight: Optional[float] = Query(default=None, gt=0),
):
    results = []
    for package in packages:
        if package_type and package["package_type"].lower() != package_type.lower():
            continue
        if max_weight is not None and package["weight"] > max_weight:
            continue
        results.append(package)
    return results


# -----------------------------------------------------------------------------
# Level 11: แบบฟอร์มแก้ไขพัสดุ
# -----------------------------------------------------------------------------
class PackageUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = Field(default=None, gt=0, le=20)
    package_type: Optional[str] = None
    fragile: Optional[bool] = None
    status: Optional[str] = None


# -----------------------------------------------------------------------------
# Level 12: แก้ไขพัสดุ
# -----------------------------------------------------------------------------
@app.patch("/packages/{package_id}")
def update_package(package_id: int, update: PackageUpdate):
    package = get_package(package_id)
    changes = update.model_dump(exclude_none=True)
    package.update(changes)
    package["cost"] = calculate_shipping_cost(
        package["weight"], package["fragile"]
    )
    return package


# -----------------------------------------------------------------------------
# Level 13: ลบพัสดุ
# -----------------------------------------------------------------------------
@app.delete("/packages/{package_id}")
def delete_package(package_id: int):
    package = get_package(package_id)
    packages.remove(package)
    return {"deleted_id": package_id, "message": "ลบพัสดุแล้ว"}


# -----------------------------------------------------------------------------
# Level 14: สร้างสรุปห้องเก็บของ
# -----------------------------------------------------------------------------
def build_cargo_summary(package_list):
    total_weight = 0
    total_cost = 0
    for package in package_list:
        total_weight += package["weight"]
        total_cost += package["cost"]
    return {
        "package_count": len(package_list),
        "total_weight": total_weight,
        "total_cost": total_cost,
    }


# -----------------------------------------------------------------------------
# Level 15: Checkpoint 3: Cargo Summary API
# -----------------------------------------------------------------------------
@app.get("/cargo-summary")
def get_cargo_summary():
    return build_cargo_summary(packages)


# -----------------------------------------------------------------------------
# Level 16: คำนวณเชื้อเพลิงตามดาว
# -----------------------------------------------------------------------------
def calculate_required_fuel(destination):
    name = destination.strip().title()
    if name not in planet_distances:
        raise HTTPException(status_code=404, detail="ไม่พบดาวปลายทาง")
    distance = planet_distances[name]
    return (distance + 9) // 10


# -----------------------------------------------------------------------------
# Level 17: สร้างแบบฟอร์มภารกิจ
# -----------------------------------------------------------------------------
class MissionCreate(BaseModel):
    destination: str
    budget: float = Field(ge=0)
    fuel: int = Field(ge=0)
    package_ids: list[int]


# -----------------------------------------------------------------------------
# Level 18: สร้างภารกิจขนส่ง
# -----------------------------------------------------------------------------
@app.post("/missions", status_code=status.HTTP_201_CREATED)
def create_mission(data: MissionCreate):
    calculate_required_fuel(data.destination)
    for package_id in data.package_ids:
        get_package(package_id)
    record = data.model_dump()
    record["id"] = len(missions) + 1
    record["destination"] = data.destination.strip().title()
    record["status"] = "planning"
    missions.append(record)
    return record


# -----------------------------------------------------------------------------
# Level 19: ค้นหาภารกิจ
# -----------------------------------------------------------------------------
@app.get("/missions/{mission_id}")
def get_mission(mission_id: int):
    for mission in missions:
        if mission["id"] == mission_id:
            return mission
    raise HTTPException(status_code=404, detail="ไม่พบภารกิจ")


# -----------------------------------------------------------------------------
# Level 20: Checkpoint 4: ดึงพัสดุของภารกิจ
# -----------------------------------------------------------------------------
def get_mission_packages(mission):
    selected = []
    for package_id in mission["package_ids"]:
        selected.append(get_package(package_id))
    return selected


# -----------------------------------------------------------------------------
# Level 21: วิเคราะห์เหตุผลที่ยังไม่พร้อม
# -----------------------------------------------------------------------------
def mission_reasons(mission):
    selected = get_mission_packages(mission)
    summary = build_cargo_summary(selected)
    required_fuel = calculate_required_fuel(mission["destination"])
    reasons = []
    if len(selected) == 0:
        reasons.append("ยังไม่มีพัสดุ")
    if summary["total_weight"] > 60:
        reasons.append("น้ำหนักเกินความจุ")
    if mission["budget"] < summary["total_cost"]:
        reasons.append("งบประมาณไม่เพียงพอ")
    if mission["fuel"] < required_fuel:
        reasons.append("เชื้อเพลิงไม่เพียงพอ")
    return reasons


# -----------------------------------------------------------------------------
# Level 22: Readiness Endpoint
# -----------------------------------------------------------------------------
@app.get("/missions/{mission_id}/readiness")
def get_mission_readiness(mission_id: int):
    mission = get_mission(mission_id)
    reasons = mission_reasons(mission)
    return {"mission_id": mission_id, "ready": len(reasons) == 0, "reasons": reasons}


# -----------------------------------------------------------------------------
# Level 23: บัญชีพัสดุแบบแบ่งหน้า
# -----------------------------------------------------------------------------
@app.get("/manifest")
def get_manifest(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=20),
):
    return {"skip": skip, "limit": limit, "items": packages[skip:skip + limit]}


# -----------------------------------------------------------------------------
# Level 24: ปล่อยยานออกเดินทาง
# -----------------------------------------------------------------------------
@app.post("/missions/{mission_id}/launch")
def launch_mission(mission_id: int):
    mission = get_mission(mission_id)
    reasons = mission_reasons(mission)
    if reasons:
        raise HTTPException(status_code=400, detail=reasons)
    mission["fuel"] -= calculate_required_fuel(mission["destination"])
    mission["status"] = "launched"
    for package in get_mission_packages(mission):
        package["status"] = "in_transit"
    return {"mission_id": mission_id, "status": mission["status"], "fuel_left": mission["fuel"]}


# -----------------------------------------------------------------------------
# Level 25: Checkpoint 5: Mission Control
# -----------------------------------------------------------------------------
@app.get("/mission-control/{mission_id}")
def mission_control(mission_id: int):
    mission = get_mission(mission_id)
    selected = get_mission_packages(mission)
    summary = build_cargo_summary(selected)
    reasons = mission_reasons(mission)
    return {
        "mission": mission,
        "cargo": summary,
        "ready": len(reasons) == 0,
        "reasons": reasons,
    }


# -----------------------------------------------------------------------------
# Level 26: ติดตามพัสดุ
# -----------------------------------------------------------------------------
@app.get("/tracking/{package_id}")
def track_package(package_id: int):
    package = get_package(package_id)
    return {
        "id": package_id,
        "name": package["name"],
        "status": package["status"],
        "message": f"{package['name']} อยู่ในสถานะ {package['status']}",
    }


# -----------------------------------------------------------------------------
# Level 27: ตรวจ API Key
# -----------------------------------------------------------------------------
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != "galaxy-123":
        raise HTTPException(status_code=401, detail="API Key ไม่ถูกต้อง")
    return x_api_key


# -----------------------------------------------------------------------------
# Level 28: รายงานผู้ดูแลระบบ
# -----------------------------------------------------------------------------
@app.get("/admin/report")
def admin_report(api_key: str = Depends(verify_api_key)):
    report = build_cargo_summary(packages)
    report["mission_count"] = len(missions)
    return report


# -----------------------------------------------------------------------------
# Level 29: รีเซ็ตศูนย์ควบคุม
# -----------------------------------------------------------------------------
@app.delete("/admin/reset")
def reset_system(api_key: str = Depends(verify_api_key)):
    packages.clear()
    missions.clear()
    return {"message": "รีเซ็ตระบบแล้ว", "packages": 0, "missions": 0}


# -----------------------------------------------------------------------------
# Level 30: Final Checkpoint: รายงานภารกิจฉบับเต็ม
# -----------------------------------------------------------------------------
@app.get("/missions/{mission_id}/full-report")
def get_full_report(mission_id: int):
    mission = get_mission(mission_id)
    selected = get_mission_packages(mission)
    summary = build_cargo_summary(selected)
    reasons = mission_reasons(mission)
    return {
        "mission_id": mission_id,
        "destination": mission["destination"],
        "status": mission["status"],
        "packages": [package["name"] for package in selected],
        "cargo": summary,
        "required_fuel": calculate_required_fuel(mission["destination"]),
        "ready": len(reasons) == 0,
        "reasons": reasons,
    }

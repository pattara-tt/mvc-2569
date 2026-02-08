ทำข้อสอบข้อที่ 2
การทำงานของแต่ละส่วน
> Model (ใช้จัดการข้อมูลและกฎของระบบ)
- database.py ใช้เชื่อมต่อกับ sqlite3 สร้างตาราง Users, Students, Credits, Projects, GraduationResults และใส่ข้อมูลเบื้องต้น
-  validator.py ตรวจ format email
- user_model.py ดึง role จาก Users ด้วย email
- student_model.py ดึงรายชื่อนักศึกษาแล้วดึงข้อมูลรายคน
-  credits_model.py ดึงหน่วยกิตสะสม ,แก้หน่วยกิตสะสม แล้ว CreditEvaluator ตรวจเกณฑ์หน่วยกิตขั้นต่ำ 135
-  projects_model.py ดึงสถานะโครงงาน ,แก้สถานะโครงงาน  และ ProjectEvaluator ตรวจว่าโครงงานผ่านหรือไม่
-  graduation_model.py GraduationEvaluator รวมผลประเมิน, GraduationResultModel บันทึกผลลง GraduationResults

> Controllers (ควบคุมลำดับการทำงาน)
- app_controller.py คุมการสลับหน้า view และเก็บ session, logout ล้าง session แล้วกลับหน้า login
- auth_controller.py รับเมลจาก view แล้วเรียก validator ตรวจ email เช็ค role ต้องเป็น admin เสร็จแล้วไปหน้ารายชื่อนักศึกษา
- student_controller.py ดึงรายชื่อนักศึกษาจาก student_model และเปิดหน้าประเมินตามที่เลือก
- evaluation_controller.py โหลดข้อมูลที่ใช้ประเมิน บันทึกค่าที่แก้ไข และประเมินตาม business rule และบันทึกผล
เสร็จแล้วไปหน้าผลการประเมิน

> Views (ใช้แสดงหน้าจอ และ รับinput จากผู้ใช้)
- base_view.py สร้าง frame ของแต่ละหน้ามี show/hide สำหรับสลับหน้า
- widgets.py  สร้าง topbar และปุ่ม logout ,ปรับตารางให้เรียบๆไม่มีเส้น
- login_view.py หน้าล็อกอินด้วย email เมื่อกดเข้าสู่ระบบเรียก auth_controller
- students_view.py  หน้ารายการนักศึกษา เลือกนักศึกษาแล้วกด evaluate ไปหน้าประเมินความพร้อมจบ
- evaluate_view.py  หน้าประเมินความพร้อมจบ admin สามารถแก้หน่วยกิต,สถานะโครงงาน,สถานะนักศึกษาได้ กดบันทึก หรือกดประเมินเพื่อไปหน้าผลการประเมืน
- result_view.py หน้าผลการประเมิน แสดงสรุปและรายละเอียด สามารถกดกลับไปหน้ารายชื่อนักศึกษาได้

main.py ทำหน้าที่เริ่มการทำงาาน
app.py  สร้าง model, controller, view และผูก views ให้ app_controller ใช้สลับหน้า


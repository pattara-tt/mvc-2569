โครงสร้าง
- Main.py
  เปิดแอปแบบโล่งๆ แค่เรียก run
- app.py
  รวมการประกอบ model/controller/view และเริ่มหน้า login

- models/
  database.py สร้างตาราง sqlite3 และ seed ข้อมูล
  validator.py ตรวจรูปแบบ email
  user_model.py อ่าน role ของ user
  student_model.py อ่านรายชื่อนักศึกษา และแก้สถานะนักศึกษา
  credits_model.py อ่าน/แก้หน่วยกิต และมี CreditEvaluator แยกกฎ
  projects_model.py อ่าน/แก้สถานะโครงงาน และมี ProjectEvaluator แยกกฎ
  graduation_model.py รวมผลประเมินและบันทึก GraduationResults

- controllers/
  app_controller.py คุมการสลับหน้า และ session
  auth_controller.py login admin
  student_controller.py คุมหน้ารายชื่อ
  evaluation_controller.py คุมหน้าประเมิน แก้ไขข้อมูล และบันทึกผล

- views/
  login_view.py หน้าล็อกอิน
  students_view.py หน้ารายการนักศึกษา
  evaluate_view.py หน้าประเมิน (แก้ไขหน่วยกิต/โครงงาน/สถานะได้)
  result_view.py หน้าผลการประเมิน
  widgets.py สไตล์ตารางและ topbar
  base_view.py โครง view พื้นฐาน

วิธีรัน
1) python Main.py
2) login ด้วย admin@uni.ac.th

from flask import Flask, render_template, redirect, request, jsonify
import mysql.connector
from flask_app.utils.database.database import database

app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
db = database()
db.createTables()

# empty route
@app.route('/')
def root():
	return redirect('/home')

# home page
@app.route('/home')
def home():
	students = db.query(query="SELECT * FROM students ORDER BY Last_Name, First_Name")
	count = db.query(query="SELECT COUNT(*) FROM students")
	school_year = db.query("""SELECT School_Year
						 FROM current_context""")[0]['School_Year']
	
	for student in students:
		student_id = student["ID"]
		grades = getGradesQuery(student_id=student_id)
		gpa = calcGPA(grades=grades)
		student["GPA"] = gpa
		attendance_percent = getCurrYearAttendance(student_id=student_id, school_year=school_year)
		student["Attendance"] = attendance_percent

		
	return render_template("home.html", students=students, count = count)

# query final grades with course name for one student
def getGradesQuery(student_id):
	grades = db.query("""
			SELECT 
				g.ID AS grade_id,
				g.Student_ID,
				g.Classes_ID,
				g.Letter_Grade,
				g.Grade_Level,
				g.Credit_Type,
				g.Credit_Awarded,
				g.Credit_Potential,
				c.Course_Name
			FROM finalgrades g
			JOIN classes c ON g.Classes_ID = c.ID
			WHERE g.Student_ID = %s
			ORDER BY g.Grade_Level
			""", (student_id,))

	return grades

# query attendance with course name for one student
def getCurrYearAttendance(student_id, school_year):
	attendance_summary = db.query("""
			SELECT 
				COUNT(*) AS total_days,
				SUM(CASE WHEN a.Code = 'P' THEN 1 ELSE 0 END) AS days_present
			FROM attendance a
			JOIN classes c ON a.Classes_ID = c.ID
			WHERE a.Student_ID = %s AND c.School_Year = %s
			""", (student_id, school_year))

	total_days = attendance_summary[0]["total_days"]
	days_present = attendance_summary[0]["days_present"]
	attendance_percent = round((days_present / total_days * 100), 2) if total_days > 0 else 0
	return attendance_percent

# student page
@app.route("/student")
@app.route("/student/<int:student_id>")
def student(student_id=None):
	students = db.query(query="SELECT * FROM students ORDER BY Last_Name, First_Name")
	return render_template("student.html", students=students, student_id=student_id)

# filter students on the home page table
@app.route('/filterStudents')
def filterStudents():
	grades = request.args.getlist('grade')
	grad_years = request.args.getlist('gradYear')
	genders = request.args.getlist('gender')
	schools = request.args.getlist('schools')
	others = request.args.getlist('other')

	where_clauses = []
	params = []

	if grades:
		placeholders = ','.join(['%s'] * len(grades))
		where_clauses.append(f"Grade IN ({placeholders})")
		params.extend(grades)
		
	if grad_years:
		placeholders = ','.join(['%s'] * len(grad_years))
		where_clauses.append(f"Expected_Graduation IN ({placeholders})")
		params.extend(grad_years)

	if genders:
		placeholders = ','.join(['%s'] * len(genders))
		where_clauses.append(f"Gender IN ({placeholders})")
		params.extend(genders)

	if schools:
		placeholders = ','.join(['%s'] * len(schools))
		where_clauses.append(f"School IN ({placeholders})")
		params.extend(schools)

	if 'ESL' in others:
		where_clauses.append("Flag_EnglishLanguageLearner = 1")
	if 'Foster' in others:
		where_clauses.append("Flag_FosterCare = 1")

	query = "SELECT * FROM students"
	if where_clauses:
		query += " WHERE " + " AND ".join(where_clauses)

	students = db.query(query, parameters=params)
	return render_template('partials/student_table_body.html', students=students)

# calculate student gpa
def calcGPA(grades):
	gp = {
			"A": 4,
			"B": 3,
			"C": 2,
			"D": 1,
			"F": 0
		}
	total_gp = 0
	total_credits = 0
	for grade in grades:
		letter_grade = grade["Letter_Grade"]

		if letter_grade == 'P':
			continue

		grade_points = gp[letter_grade]
		credits = grade["Credit_Awarded"]

		total_gp += grade_points * credits
		total_credits += credits

	gpa = round(total_gp/total_credits if total_credits != 0 else 0, 2)

	return gpa
	
# load tables upon selected a student on the student page
@app.route('/loadStudentTables')
def loadStudentTables():
	student_id = request.args.get("student_id")

	if not student_id:
		return ""

	try:
		# Student Info
		student_info = db.query("SELECT * FROM students WHERE ID = %s", (student_id,))

		# Attendance (with course name)
		attendance = db.query("""
			SELECT 
				a.ID as attendance_ID,
				a.Student_ID,
				a.Classes_ID,
				a.Date as attendance_date,
				a.Code,
				c.Course_Name
			FROM attendance a
			JOIN classes c ON a.Classes_ID = c.ID
			WHERE a.Student_ID = %s
			ORDER BY c.Course_Name, attendance_date
			""", (student_id,))

		# Classes
		classes = db.query("""
			SELECT *
			FROM classes
			WHERE Student_ID = %s
			ORDER BY Course_Name
			""", (student_id,))

		# Final Grades (with course name)
		grades = getGradesQuery(student_id=student_id)
		
		gpa = calcGPA(grades=grades)
		
		gradreq = db.query("""
			SELECT Credit_Type, SUM(Credit_Awarded) as total_credit
			FROM finalgrades
			WHERE Student_ID = %s
			GROUP BY Credit_Type
					 """, (student_id,))
		
		# initialize all credit types to 0
		credits_dict = {c: 0 for c in ["ELA","MTH","SCI","SS","LANG","ART","PE", "OTHER"]}

		# fill with actual values
		for row in gradreq:
			credits_dict[row["Credit_Type"]] = float(row["total_credit"])

		# total credits
		credits_dict["Total"] = sum(credits_dict.values())

		required_credits = 19

		# Render partials
		student_info_html = render_template("partials/single_student_table_body.html", student=student_info[0] if student_info else None)
		attendance_html = render_template("partials/attendance_table_body.html", attendance=attendance)
		classes_html = render_template("partials/classes_table_body.html", classes=classes)
		grades_html = render_template("partials/grades_table_body.html", grades=grades)
		credits_html = render_template("partials/grad_req_table_body.html", credits=credits_dict)

		return jsonify({
			"student_info": student_info_html,
			"attendance": attendance_html,
			"classes": classes_html,
			"grades": grades_html,
			"credits": credits_html,
			"curr_credits": credits_dict["Total"],
			"remaining_credits": required_credits - credits_dict["Total"],
			"required_credits": required_credits,
			"gpa": gpa,
		})
	except Exception as e:
		import traceback
		print("❌ ERROR in /loadStudentTables:", e)
		traceback.print_exc()
		return jsonify({"error": str(e)}), 500
	
# filter by current classes only on student page	
@app.route('/getCurrClasses')
def getCurrClasses():
	# check whether the checkbox is checked
	current_only = request.args.get("current_only", "false").lower() == "true"
	student_id = request.args.get("student_id")

	if current_only:
		con = db.query("SELECT School_Year, Term FROM current_context ORDER BY Updated_At DESC LIMIT 1")[0]
		curr = db.query("""SELECT *
			FROM classes
			WHERE school_year = %s AND Term = %s AND Student_ID = %s
			""", (con["School_Year"], con["Term"], student_id,))
	else:
		curr = db.query("""SELECT *
			FROM classes
			WHERE Student_ID = %s
			ORDER BY Course_Name
			""", (student_id,))

	classes_html = render_template("partials/classes_table_body.html", classes=curr)
	
	return jsonify({"classes": classes_html})



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int("8080"), debug=True)
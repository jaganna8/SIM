from flask import Flask, render_template, redirect, request, jsonify, session, flash
from flask_app.utils.database.database import database
from functools import wraps
import config
import logging

app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
app.secret_key = config.secret_key
db = database()
db.build_db()

# empty route
@app.route('/')
def root():
	return redirect('/login')


### login or create account ###

# login page
@app.route('/login')
def login():
	return render_template("login.html")

# create account page
@app.route('/create')
def create():
	return render_template("create_account.html")

# login account
@app.route('/login_account', methods=['POST'])
def login_account():
	email = request.form['email']
	password = request.form['password']

	user = db.query("SELECT * FROM users WHERE Email = %s", (email,))
	print(user)

	if not user or not db.check_password(password, user[0]['Password_Hash']):
		return jsonify({'error': 'Invalid email or password'}), 401
	
	session['user'] = email

	return redirect('/home')

# add account to db
@app.route('/create_account', methods=['POST'])
def create_account():
	email = request.form['email']
	password = request.form['createpassword']
	role = request.form['role']

	hashed = db.hash_password(password)

	try:
		db.insert_rows(table='users', columns=['Email', 'Password_Hash', 'Role'], parameters=[[email, hashed, role]])
		print(db.query("SELECT * FROM users"))
	except Exception as e:
		return jsonify({'error': str(e)}), 400
	
	session['user'] = email

	return redirect('/home')

### main page other routes ###

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



### home page ###

# home page
@app.route('/home')
@login_required
def home():
	count = db.query("SELECT COUNT(*) FROM students")[0]['COUNT(*)']

	email = session['user']
	user = db.query("SELECT Email, Role FROM users WHERE Email = %s", (email,))

	print(f"Session email: '{session['user']}'")
	print(f"Query result: {user}")

	return render_template("home.html", count=count, user = user)

@app.route('/loadStudents')
def loadStudents():
	base_gpa = config.base_gpa

	offset = int(request.args.get('offset', 0))
	limit = int(request.args.get('limit', 50))

	students = db.query("""
		SELECT 
			s.ID,
			s.First_Name,
			s.Last_Name,
			s.Grade,
			s.Expected_Graduation,
			s.Gender,
			s.School,
						
			ROUND(
				COALESCE(
					SUM(
						CASE 
							WHEN fg.Letter_Grade = 'A' THEN 4
							WHEN fg.Letter_Grade = 'B' THEN 3
							WHEN fg.Letter_Grade = 'C' THEN 2
							WHEN fg.Letter_Grade = 'D' THEN 1
							ELSE 0
						END
					) / NULLIF(COUNT(fg.ID),0), 
					0
				), 2
			) AS GPA
						
		FROM students s
		LEFT JOIN finalgrades fg ON fg.Student_ID = s.ID
		LEFT JOIN classes c ON c.ID = fg.Class_ID
		GROUP BY s.ID
		ORDER BY s.Last_Name, s.First_Name
		LIMIT %s OFFSET %s
	""", (limit, offset,))
	return render_template('partials/student_table_body.html', students=students, base_gpa = base_gpa)

# filter students on the home page table
@app.route('/filterStudents')
def filterStudents():
	base_gpa = config.base_gpa

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

	query = """
        SELECT 
            s.ID,
            s.First_Name,
            s.Last_Name,
            s.Grade,
            s.Expected_Graduation,
            s.Gender,
            s.School,
            ROUND(
                COALESCE(
                    SUM(
                        CASE 
                            WHEN fg.Letter_Grade = 'A' THEN 4
                            WHEN fg.Letter_Grade = 'B' THEN 3
                            WHEN fg.Letter_Grade = 'C' THEN 2
                            WHEN fg.Letter_Grade = 'D' THEN 1
                            ELSE 0
                        END
                    ) / NULLIF(COUNT(fg.ID),0),
                    0
                ),2
            ) AS GPA
        FROM students s
        LEFT JOIN finalgrades fg ON fg.Student_ID = s.ID
        LEFT JOIN classes c      ON c.ID = fg.Class_ID
    """
	if where_clauses:
		query += " WHERE " + " AND ".join(where_clauses)

	query += " GROUP BY s.ID ORDER BY s.Last_Name, s.First_Name"

	students = db.query(query, parameters=params)
	return render_template('partials/student_table_body.html', students=students, base_gpa = base_gpa)



### student page ###

# student page
@app.route("/student")
@app.route("/student/<int:student_id>")
@login_required
def student(student_id=None):
	students = db.query(query="SELECT * FROM students ORDER BY Last_Name, First_Name")
	email = session['user']
	user = db.query("SELECT Email, Role FROM users WHERE Email = %s", (email,))
	return render_template("student.html", students=students, student_id=student_id, user = user)

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
				a.Class_ID,
				a.`Date` as attendance_date,
				a.Code,
				c.Course_Name
			FROM attendance a
			JOIN classes c ON a.Class_ID = c.ID
			WHERE a.Student_ID = %s
			ORDER BY c.Course_Name, attendance_date
			""", (student_id,))
		
		# Classes
		classes = db.query("""
			SELECT c.*
			FROM classes c
			JOIN enrollment e on e.Class_ID = c.ID
			WHERE e.Student_ID = %s
			ORDER BY c.Course_Name
			""", (student_id,))

		# Final Grades (with course name)
		grades = db.query("""
			SELECT 
				g.ID AS grade_id,
				g.Student_ID,
				g.Class_ID,
				g.Letter_Grade,
				g.Grade_Level,
				g.Credit_Type,
				g.Credit_Awarded,
				g.Credit_Potential,
				c.Course_Name
			FROM finalgrades g
			JOIN classes c ON g.Class_ID = c.ID
			WHERE g.Student_ID = %s
			ORDER BY g.Grade_Level
			""", (student_id,))
		
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
		school_year = config.school_year
		term = config.term
		curr = db.query("""SELECT c.*
			FROM classes c
			JOIN enrollment e ON e.Class_ID = c.ID
			WHERE c.school_year = %s AND c.Term = %s AND c.Student_ID = %s
			""", (school_year, term, student_id,))
	else:
		curr = db.query("""SELECT c.*
			FROM classes c
			JOIN enrollment e ON e.Class_ID = c.ID
			WHERE e.Student_ID = %s
			ORDER BY c.Course_Name
			""", (student_id,))

	classes_html = render_template("partials/classes_table_body.html", classes=curr)
	
	return jsonify({"classes": classes_html})



### account page ###

@app.route('/account')
@login_required
def account():
	email = session['user']
	user = db.query("SELECT Email, Role FROM users WHERE Email = %s", (email,))
	return render_template("account.html", user = user)


### admin tools page ###

@app.route('/admin_tools')
@login_required
def admin_tools():
	email = session['user']
	user = db.query("SELECT Email, Role FROM users WHERE Email = %s", (email,))[0]

	if user['Role'] != 'admin':
		flash("You are not authorized to view Admin Tools.")
		return redirect('/home')

	return render_template("admin_tools.html", user = user)


### teacher tools page ###
@app.route('/teacher_tools')
@login_required
def teacher_tools():
	email = session['user']
	user = db.query("SELECT Email, Role FROM users WHERE Email = %s", (email,))

	teacher = db.query("SELECT ID FROM users WHERE Email = %s", (email,))[0]
	courses = db.query("SELECT Course_Name FROM classes WHERE Teacher_ID = %s", (teacher['ID'],))
	return render_template("teacher_tools.html", user = user, courses = courses)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int("8080"), debug=True)
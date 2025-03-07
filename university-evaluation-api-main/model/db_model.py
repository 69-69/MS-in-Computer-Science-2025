import random

from static.config import Config


class DBModel:
    def __init__(self):
        """Initialize the model with the database configuration."""
        self.config = Config()  # Uses the existing Config class

    def get_db_connection(self):
        """Helper method to get a DB connection from the Config class."""
        return self.config.get_db_cursor()

    def close_db_connection(self, cursor, conn):
        """Helper method to close DB connection and cursor."""
        self.config.close_db_cursor(cursor)
        self.config.close_db_connection(conn)

    def reset_database(self):
        return self.config.reset_database()


    def execute_query(self, query, params=None):
        """Helper function to execute a query using Config class."""
        return self.config.execute_query(query, params)

    def get_all_degrees(self):
        """Fetch all distinct degree names and levels."""
        query = "SELECT DISTINCT degree_name, level FROM Degree"
        return self.execute_query(query)

    def get_all_semesters(self):
        """Fetch all semesters."""
        query = "SELECT DISTINCT semester_code FROM Semester"
        return self.execute_query(query)

    def get_all_courses(self):
        """Fetch all course numbers and names."""
        query = "SELECT DISTINCT course_number, course_name FROM Course"
        return self.execute_query(query)
    

    def get_all_sections(self):
        """Fetch all section info."""
        query = """
            SELECT course_number, section_id, instructor_id, year, semester, enrollment 
            FROM Section ORDER BY course_number"""
        return self.execute_query(query)

    def get_all_goals(self):
        """Fetch all goals."""
        query = "SELECT * FROM Goal"
        return self.config.execute_query(query)

    def insert_course(self, course_number, course_name):
        """Insert a new Course into the 'Course' table."""
        query = "INSERT INTO Course (course_number, course_name) VALUES (%s, %s)"
        params = (course_number, course_name)
        return self.execute_query(query, params)

    def update_course(self, course_number, new_course):
        """Update a course."""
        query = "UPDATE Course SET course_name = %s WHERE course_number = %s"
        params = (new_course, course_number)
        return self.execute_query(query, params)

    def delete_course(self, course_number):
        """Delete a course from the 'course' table."""
        query = "DELETE FROM Course WHERE course_number = %s"
        params = (course_number,)
        return self.execute_query(query, params)

    def insert_section(self, section_id, course_number, year, semester, instructor_id, enrollment):
        """Insert a new Section into the 'Section' table."""
        query = "INSERT INTO Section (section_id, course_number, year, semester, instructor_id, enrollment) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (section_id, course_number, year, semester, instructor_id, enrollment)
        return self.execute_query(query, params)

    def get_all_degree_levels(self):
        query = "SELECT * FROM Degree_Level"
        return self.execute_query(query)

    def insert_degree_level(self, new_level):
        query = "INSERT INTO Degree_Level VALUES(%s)"
        params = (new_level,)

        return self.execute_query(query, params)

    def get_all_degrees(self):
        query = "SELECT degree_name, level FROM Degree"
        return self.execute_query(query)

    def get_degree(self, name, level):
        query = "SELECT * FROM Degree WHERE degree_name = %s and level = %s"
        params = (name, level)
        return self.execute_query(query, params)

    def insert_degree(self, name, level, department, courses):
        query = "INSERT INTO Degree VALUES(%s, %s, %s)"
        params = (name, level, department)

        degree_insert = self.execute_query(query, params)
        course_insert = True
        if len(courses) > 0 and degree_insert:
            course_query = "INSERT INTO Degree_Course_Requirement VALUES " + ", ".join(["(%s, %s, %s, %s)"] * len(courses))
            course_params = []
            for course in courses:
                course_params.extend([name, level, course['course_number'], course['is_core']])
            course_insert = self.execute_query(course_query, course_params)
        return degree_insert and course_insert

    def get_degree_courses(self, name, level):
        query = """
            SELECT dc.course_number AS course_number, dc.is_core AS is_core, c.course_name as course_name
            FROM Degree_Course_Requirement dc
            JOIN Course c ON dc.course_number = c.course_number
            WHERE degree_name = %s and degree_level = %s"""
        params = (name, level)
        return self.execute_query(query, params)

    def get_degree_goals(self, name, level):
        query = "SELECT * FROM Goal WHERE degree_name = %s and degree_level = %s"
        params = (name, level)
        return self.execute_query(query, params)

    def get_degree_sections(self, name, level, beginning_year_semester, ending_year_semester):
        query = """
            SELECT
                s.*,
                c.course_name as course_name,
                CASE 
                    WHEN s.semester = 'Spring' THEN CONCAT(s.year, '-01-20')
                    WHEN s.semester = 'Summer' THEN CONCAT(s.year, '-07-01')
                    WHEN s.semester = 'Fall' THEN CONCAT(s.year, '-09-01')
                    ELSE NULL
                END AS semester_date
            FROM Section s
            JOIN Degree_Course_Requirement dc ON s.course_number = dc.course_number
            JOIN Course c ON s.course_number = c.course_number
            WHERE
                dc.degree_name = %s
                AND dc.degree_level = %s
                AND CAST(CONCAT(s.year, CASE 
                    WHEN s.semester = 'Spring' THEN '-01-20'
                    WHEN s.semester = 'Summer' THEN '-07-01'
                    WHEN s.semester = 'Fall' THEN '-09-01'
                    ELSE NULL
                END) AS DATE) BETWEEN
                CAST(%s AS DATE) AND 
                CAST(%s AS DATE)
            ORDER BY semester_date;
         """
        params = (name, level, beginning_year_semester, ending_year_semester)
        return self.execute_query(query, params)
    
    def get_degree_goal_courses(self, goal_code):
        query = """
            SELECT c.course_number, c.course_name, dc.is_core
            FROM Course c
            JOIN Goal g ON c.course_number = g.course_number
            JOIN Degree_Course_Requirement dc ON g.degree_name = dc.degree_name AND g.degree_level = dc.degree_level AND  dc.course_number = g.course_number
            WHERE g.goal_code = %s 
        """
        params = (goal_code,)
        return self.execute_query(query, params)

    def get_degree_goal(self, goal_code, degree_name, degree_level):
        query = """
            SELECT g.*, d.department_name as department_name
            FROM Goal g
            JOIN Degree d ON g.degree_name = d.degree_name AND g.degree_level = d.level
            WHERE g.goal_code = %s and g.degree_name = %s and g.degree_level = %s
        """
        params = (goal_code, degree_name, degree_level)
        return self.execute_query(query, params)

    
    
    # Evaluation Page Functions

    def get_all_evaluations(self):
        """Fetch evaluations for a specific section and goal."""
        query = """
            SELECT *, C.course_name
            FROM Section_Evaluation E
            JOIN Course C ON E.course_number = C.course_number
            ORDER BY E.year, E.semester
        """
        return self.execute_query(query)
    
    # Function inputs Goal into each semester provided there is a section that exists in the Section Table for that semester
    def add_goal(self, goal_code, degree_name, degree_level, course_number, goal_description):
        """
        Insert a new goal into the Goal table and populate the Section_Evaluation table
        based on sections associated with the course number of the goal.
        """
        try:
            # Goal table insertion
            insert_goal_query = """
                INSERT INTO Goal (goal_code, degree_name, degree_level, course_number, goal_description)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    goal_description = VALUES(goal_description);
            """
            goal_params = (goal_code, degree_name, degree_level, course_number, goal_description)
            self.config.execute_query(insert_goal_query, goal_params)

            # Section Evaluation Table Insertion
            populate_section_evaluation_query = """
                INSERT INTO Section_Evaluation (
                    goal_code,
                    section_id,
                    instructor_notes,
                    number_of_a,
                    number_of_b,
                    number_of_c,
                    number_of_d,
                    number_of_f,
                    course_number,
                    year,
                    semester
                )
                SELECT
                    %s AS goal_code,       -- Use the new goal code
                    s.section_id,          -- Section ID from the Section table
                    NULL AS instructor_notes, -- Default to no instructor notes
                    0 AS number_of_a,      -- Default grades to 0
                    0 AS number_of_b,
                    0 AS number_of_c,
                    0 AS number_of_d,
                    0 AS number_of_f,
                    s.course_number,       -- Course number from the Section table
                    s.year,                -- Year from the Section table
                    s.semester             -- Semester from the Section table
                FROM Section s
                WHERE s.course_number = %s -- Match course number
                AND NOT EXISTS (           -- Avoid duplicate entries in Section_Evaluation
                    SELECT 1
                    FROM Section_Evaluation se
                    WHERE se.section_id = s.section_id
                    AND se.goal_code = %s
                    AND se.semester = s.semester
                );
            """
            section_params = (goal_code, course_number, goal_code)
            self.config.execute_query(populate_section_evaluation_query, section_params)

            return {"success": True, "message": "Goal added and Section_Evaluation table updated for existing semesters."}

        except Exception as e:
            print(f"Error in add_goal: {e}")
            return {"success": False, "message": str(e)}

    # Function states Not Completed if no entry or grades exceed enrollment. Complete if grades meet enrollment
    def get_sections_status(self, semester, percentage=None):
        """
        Fetch sections, their evaluation status, instructor notes status, and degree details for a given semester.
        """
        query = """
            SELECT 
                s.section_id, 
                s.course_number, 
                s.year, 
                s.semester,
                g.degree_name,
                g.degree_level,
                CASE 
                    WHEN SUM(se.number_of_a + se.number_of_b + se.number_of_c + se.number_of_d + se.number_of_f) = 0 THEN NULL
                    ELSE 
                        CAST(
                            SUM(se.number_of_a + se.number_of_b + se.number_of_c + se.number_of_d) * 100.0 / 
                            SUM(se.number_of_a + se.number_of_b + se.number_of_c + se.number_of_d + se.number_of_f)
                        AS DECIMAL(5, 2))
                END AS non_failing_percentage,
                CASE 
                    WHEN se.goal_code IS NOT NULL 
                        AND (se.number_of_a + se.number_of_b + se.number_of_c + se.number_of_d + se.number_of_f) = s.enrollment
                        AND se.number_of_a IS NOT NULL 
                        AND se.number_of_b IS NOT NULL 
                        AND se.number_of_c IS NOT NULL 
                        AND se.number_of_d IS NOT NULL 
                        AND se.number_of_f IS NOT NULL THEN 'Completed'
                    WHEN se.goal_code IS NOT NULL 
                        AND (se.number_of_a + se.number_of_b + se.number_of_c + se.number_of_d + se.number_of_f) > 0
                        AND (se.number_of_a + se.number_of_b + se.number_of_c + se.number_of_d + se.number_of_f) < s.enrollment THEN 'Partial'
                    WHEN se.goal_code IS NOT NULL THEN 'Not Completed'
                    ELSE 'None'
                END AS evaluation_status,
                CASE 
                    WHEN se.instructor_notes IS NOT NULL AND LENGTH(se.instructor_notes) >= 100 THEN 'Completed'
                    WHEN se.instructor_notes IS NOT NULL AND LENGTH(se.instructor_notes) > 0 THEN 'Partial'
                    ELSE 'None'
                END AS instructor_notes_status
            FROM Section s
            LEFT JOIN Section_Evaluation se 
                ON s.section_id = se.section_id
            LEFT JOIN Goal g 
                ON se.goal_code = g.goal_code
            WHERE s.semester = %s
            GROUP BY 
                s.section_id, 
                s.course_number, 
                s.year, 
                s.semester,
                g.degree_name,
                g.degree_level,
                se.goal_code, 
                se.number_of_a, 
                se.number_of_b, 
                se.number_of_c, 
                se.number_of_d, 
                se.number_of_f, 
                se.instructor_notes,
                s.enrollment
        """
        if percentage is not None:
            query += " HAVING non_failing_percentage >= %s"
            return self.execute_query(query, (semester, percentage))
        else:
            return self.execute_query(query, (semester,))


    def fetch_sections(self, semester, instructor_id):
        """
        Fetch sections for a specific semester and instructor, including goal descriptions, degree names, and degree levels.
        """
        query = """
            SELECT 
                s.section_id,
                s.course_number,
                c.course_name,
                s.year,
                s.semester,
                COALESCE(e.instructor_notes, '') AS instructor_notes,
                COALESCE(e.number_of_a, 0) AS number_of_a,
                COALESCE(e.number_of_b, 0) AS number_of_b,
                COALESCE(e.number_of_c, 0) AS number_of_c,
                COALESCE(e.number_of_d, 0) AS number_of_d,
                COALESCE(e.number_of_f, 0) AS number_of_f,
                e.goal_code,
                g.goal_description,
                g.degree_name,
                g.degree_level
            FROM Section s
            LEFT JOIN Section_Evaluation e 
                ON s.section_id = e.section_id 
                AND s.course_number = e.course_number 
                AND s.year = e.year 
                AND s.semester = e.semester
            JOIN Course c 
                ON s.course_number = c.course_number
            LEFT JOIN Goal g
                ON e.goal_code = g.goal_code
            WHERE s.instructor_id = %s 
            AND s.semester = %s
            ORDER BY s.year DESC, s.course_number;
        """
        params = (instructor_id, semester)
        return self.execute_query(query, params)

    #
    def save_evaluation_data(self, goal_code, section_id, instructor_notes, number_of_a, number_of_b, number_of_c, number_of_d, number_of_f, course_number, year, semester):
        """
        Insert or update evaluation data for a section.
        """
        query = """
            INSERT INTO Section_Evaluation (
                goal_code,
                section_id,
                instructor_notes,
                number_of_a,
                number_of_b,
                number_of_c,
                number_of_d,
                number_of_f,
                course_number,
                year,
                semester
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                instructor_notes = VALUES(instructor_notes),
                number_of_a = VALUES(number_of_a),
                number_of_b = VALUES(number_of_b),
                number_of_c = VALUES(number_of_c),
                number_of_d = VALUES(number_of_d),
                number_of_f = VALUES(number_of_f);
        """
        params = (goal_code, section_id, instructor_notes, number_of_a, number_of_b, number_of_c, number_of_d, number_of_f, course_number, year, semester)
        self.execute_query(query, params)

    def duplicate_evaluation_across_degrees(self, section_id, course_number, goal_code):
        """
        Duplicate or update evaluation data for the given goal_code into associated degrees
        with the same course number and goal description.
        """
        query = """
            INSERT INTO Section_Evaluation (
                goal_code,
                section_id,
                instructor_notes,
                number_of_a,
                number_of_b,
                number_of_c,
                number_of_d,
                number_of_f,
                course_number,
                year,
                semester
            )
            SELECT 
                g2.goal_code, 
                se.section_id, 
                se.instructor_notes, 
                se.number_of_a, 
                se.number_of_b, 
                se.number_of_c, 
                se.number_of_d, 
                se.number_of_f, 
                se.course_number, 
                se.year, 
                se.semester
            FROM Section_Evaluation se
            JOIN Goal g1 ON g1.goal_code = se.goal_code
            JOIN Goal g2 
                ON g1.course_number = g2.course_number
                AND g1.goal_description = g2.goal_description
                AND g1.goal_code <> g2.goal_code
            WHERE se.goal_code = %s
            ON DUPLICATE KEY UPDATE
                instructor_notes = VALUES(instructor_notes),
                number_of_a = VALUES(number_of_a),
                number_of_b = VALUES(number_of_b),
                number_of_c = VALUES(number_of_c),
                number_of_d = VALUES(number_of_d),
                number_of_f = VALUES(number_of_f);
        """
        params = (goal_code,)
        try:
            self.execute_query(query, params)
            return {"success": True, "message": "Evaluation data successfully duplicated and updated across degrees."}
        except Exception as e:
            return {"success": False, "message": f"Error duplicating evaluation data: {e}"}






    # Instructors
    def get_all_years(self):
        """Get all unique years from the Section table."""
        query = "SELECT DISTINCT year FROM Section ORDER BY year"
        return self.execute_query(query)

    def unique_digits(self):
        uid = random.sample(range(10), 4)
        # convert a list of digits to integer
        to_int = int(''.join(map(str, uid)))
        return to_int

    def generate_instructor_id(self):
        """Generate the next instructor ID based on the current count."""
        query = "SELECT COUNT(*) FROM instructor"
        result = self.execute_query(query)
        # Get the count and add 1 for the new ID
        next_instructor_number = result[0]['COUNT(*)'] + 1
        instructor_id = f"{self.unique_digits()}{next_instructor_number:04}"
        return instructor_id

    def get_all_instructors(self):
        """Fetch all instructors from the 'Instructor' table."""
        query = "SELECT * FROM Instructor ORDER BY instructor_id DESC"
        return self.execute_query(query)

    def insert_instructor(self, name):
        """Insert a new instructor into the 'Instructor' table."""
        instructor_id = self.generate_instructor_id()
        query = "INSERT INTO Instructor (instructor_id, name) VALUES (%s, %s)"
        params = (instructor_id, name)
        return self.execute_query(query, params)

    def update_instructor(self, instructor_id, new_name):
        """Update an instructor's information."""
        query = "UPDATE Instructor SET name = %s WHERE instructor_id = %s"
        params = (new_name, instructor_id)
        return self.execute_query(query, params)

    def delete_instructor(self, instructor_id):
        """Delete an instructor from the 'Instructor' table."""
        query = "DELETE FROM Instructor WHERE instructor_id = %s"
        params = (instructor_id,)
        return self.execute_query(query, params)

    def get_sections_by_instructor(self, instructor_id, start_year, end_year):
        """Get all sections taught by a specific instructor in a given year range."""
        query = """
            SELECT S.section_id, S.course_number, C.course_name, S.year, S.semester, S.enrollment, I.name 
            FROM Section S
            JOIN Course C ON S.course_number = C.course_number
            JOIN Instructor I ON S.instructor_id = I.instructor_id
            WHERE S.instructor_id = %s AND S.year BETWEEN %s AND %s
            ORDER BY S.year, S.semester
        """
        params = (instructor_id, start_year, end_year)
        return self.execute_query(query, params)

    def get_all_departments(self):
        """Fetch all distinct department names """
        query = "SELECT DISTINCT department_name FROM Department"
        return self.execute_query(query)

    def insert_department(self, department_name):
        """Insert a new Department into the 'Department' table."""
        query = "INSERT INTO Department (department_name) VALUES (%s)"
        params = (department_name)
        return self.execute_query(query, params)
    
    def get_course_sections(self, course_number, beginning_year_semester, ending_year_semester):
        query = """
            SELECT
                s.*,
                CASE 
                    WHEN s.semester = 'Spring' THEN CONCAT(s.year, '-01-20')
                    WHEN s.semester = 'Summer' THEN CONCAT(s.year, '-07-01')
                    WHEN s.semester = 'Fall' THEN CONCAT(s.year, '-09-01')
                    ELSE NULL
                END AS semester_date
            FROM Section s
            WHERE
                s.course_number = %s
                AND CAST(CONCAT(s.year, CASE 
                    WHEN s.semester = 'Spring' THEN '-01-20'
                    WHEN s.semester = 'Summer' THEN '-07-01'
                    WHEN s.semester = 'Fall' THEN '-09-01'
                    ELSE NULL
                END) AS DATE) BETWEEN
                CAST(%s AS DATE) AND 
                CAST(%s AS DATE)
            ORDER BY semester_date;
        """
        params = (course_number, beginning_year_semester, ending_year_semester)
        return self.execute_query(query, params)
from model.db_model import DBModel
from view.evaluation_view import EvaluationView
from flask import request, jsonify, redirect, flash


class EvaluationController:
    def __init__(self):
        
        self.model = DBModel()  
        self.view = EvaluationView()  

    def evaluation(self):
        """
        Render the evaluation page.
        Displays dropdowns for semesters and instructors, as well as data for the Add Goal feature.
        """
        if request.method == 'GET':
            try:

                degrees = self.model.get_all_degrees()
                courses = self.model.get_all_courses()
                goals = self.model.get_all_goals()
                instructors = self.model.get_all_instructors()
                semesters = self.model.get_all_semesters()
                return self.view.render(
                    success=True,
                    error=None,
                    degrees=degrees,
                    courses=courses,
                    goals=goals,
                    instructors=instructors,
                    semesters=semesters,
                    sections=[]  
                )
            except Exception as e:
                return self.view.render(
                    success=False,
                    error=str(e),
                    degrees=[],
                    courses=[],
                    goals=[],
                    instructors=[],
                    semesters=[],
                    sections=[]
                )
        return redirect('/evaluation')

    def add_goal(self):
        """
        Handle the addition of a new goal to the database.
        Redirects back to the evaluation page upon completion.
        """
        if request.method == 'POST':
            try:
                
                goal_code = request.form['goal_code']
                degree_name = request.form['degree_name']
                degree_level = request.form['degree_level']
                course_number = request.form['course_number']
                goal_description = request.form['goal_description']
                

                # Add the 'G' prefix to the goal code
                if not goal_code.isdigit() or len(goal_code) != 3:
                    flash("Invalid Goal Code. Must be a 3-digit non-negative number.", "danger")
                    return redirect('/evaluation')
            
                goal_code = f"G{goal_code}"
                print(goal_code)
                self.model.add_goal(goal_code, degree_name, degree_level, course_number, goal_description)

            except Exception as e:
                flash(f"Failed to add goal: {str(e)}", "danger")
        return redirect('/evaluation')

    def get_sections_status(self):
        """
        Fetch sections and their evaluation status for a given semester.
        Include non-failing percentage for sections that meet the threshold.
        """
        try:
            data = request.json
            semester = data.get('semester')
            percentage = data.get('percentage')  # Optional

            if not semester:
                return jsonify({"error": "Semester is required."}), 400

            # Validate and convert percentage
            if percentage is not None:
                try:
                    percentage = float(percentage)
                except ValueError:
                    return jsonify({"error": "Percentage must be a valid number."}), 400

            # Fetch sections and statuses
            sections_status = self.model.get_sections_status(semester, percentage)
            return jsonify({"success": True, "sections": sections_status})
        except Exception as e:
            print(f"Error in get_sections_status: {e}")
            return jsonify({"success": False, "message": str(e)}), 500

    def get_evaluation_sections(self):
        """
        Fetch sections taught by a specific instructor in a given semester.
        """
        try:
            data = request.json
            semester = data.get('semester')
            instructor = data.get('instructor')

            if not semester or not instructor:
                return jsonify({"error": "Both semester and instructor are required."}), 400

            sections = self.model.fetch_sections(semester, instructor)
            return jsonify({"success": True, "sections": sections}), 200
        except Exception as e:
            print(f"Error in get_evaluation_sections: {e}")
            return jsonify({"success": False, "message": str(e)}), 500

    def save_evaluation_data(self):
        """
        Save or update evaluation data for a section and duplicate it across degrees if needed.
        """
        try:
            
            data = request.json
            section_id = data.get('section_id')
            course_number = data.get('course_number')
            goal_code = data.get('goal_code')
            instructor_notes = data.get('instructor_notes')
            number_of_a = data.get('number_of_a', 0)
            number_of_b = data.get('number_of_b', 0)
            number_of_c = data.get('number_of_c', 0)
            number_of_d = data.get('number_of_d', 0)
            number_of_f = data.get('number_of_f', 0)
            duplicate_degrees = data.get('duplicate_degrees', False)
            if not section_id or not course_number or not goal_code:
                return jsonify({"success": False, "message": "Missing required fields: section_id, course_number, or goal_code."}), 400

            self.model.save_evaluation_data(
                goal_code=goal_code,
                section_id=section_id,
                instructor_notes=instructor_notes,
                number_of_a=number_of_a,
                number_of_b=number_of_b,
                number_of_c=number_of_c,
                number_of_d=number_of_d,
                number_of_f=number_of_f,
                course_number=course_number,
                year=data.get('year'),
                semester=data.get('semester')
            )

            if duplicate_degrees is True:
                self.model.duplicate_evaluation_across_degrees(section_id, course_number, goal_code)
            return jsonify({"success": True, "message": "Evaluation saved and duplicated across degrees if requested."}), 200

        except Exception as e:
            print(f"Error in save_evaluation_data: {e}")
            return jsonify({"success": False, "message": str(e)}), 500
        
        
        
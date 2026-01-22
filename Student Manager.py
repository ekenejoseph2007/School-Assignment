

import json
import os
from datetime import datetime

class StudentManager:
    def __init__(self, data_file="students.json"):
        """
        Initialize Student Manager with data file
        """
        self.data_file = data_file
        self.students = []
        self.load_data()
    
    def load_data(self):
        """
        Load student data from JSON file
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    self.students = json.load(file)
                print(f"✅ Loaded {len(self.students)} student records")
            except (json.JSONDecodeError, FileNotFoundError):
                self.students = []
                print("⚠️  No existing data found. Starting fresh.")
        else:
            self.students = []
            print("📁 Creating new data file")
    
    def save_data(self):
        """
        Save student data to JSON file
        """
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.students, file, indent=4)
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def generate_student_id(self):
        """
        Generate unique student ID
        Format: STU001, STU002, etc.
        """
        if not self.students:
            return "STU001"
        
        # Get the highest student ID
        max_id = 0
        for student in self.students:
            try:
                num = int(student['student_id'][3:])
                if num > max_id:
                    max_id = num
            except (ValueError, KeyError):
                continue
        
        return f"STU{max_id + 1:03d}"
    
    def add_student(self, name, age, grade, email, course):
        """
        Add a new student record
        """
        student_id = self.generate_student_id()
        
        student = {
            "student_id": student_id,
            "name": name,
            "age": age,
            "grade": grade,
            "email": email,
            "course": course,
            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.students.append(student)
        
        if self.save_data():
            print(f"✅ Student {student_id} added successfully!")
            return student_id
        else:
            print("❌ Failed to save student data")
            return None
    
    def view_students(self, student_id=None):
        """
        View all students or specific student by ID
        """
        if not self.students:
            print("📭 No student records found")
            return []
        
        if student_id:
            for student in self.students:
                if student['student_id'] == student_id:
                    return [student]
            print(f"❌ Student with ID {student_id} not found")
            return []
        
        return self.students
    
    def update_student(self, student_id, **kwargs):
        """
        Update student information
        """
        for student in self.students:
            if student['student_id'] == student_id:
                for key, value in kwargs.items():
                    if key in student:
                        student[key] = value
                
                student['date_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if self.save_data():
                    print(f"✅ Student {student_id} updated successfully!")
                    return True
                else:
                    print("❌ Failed to save updated data")
                    return False
        
        print(f"❌ Student with ID {student_id} not found")
        return False
    
    def delete_student(self, student_id):
        """
        Delete a student record
        """
        for i, student in enumerate(self.students):
            if student['student_id'] == student_id:
                deleted_student = self.students.pop(i)
                
                if self.save_data():
                    print(f"✅ Student {student_id} deleted successfully!")
                    return deleted_student
        
        print(f"❌ Student with ID {student_id} not found")
        return None
    
    def search_student(self, search_term):
        """
        Search students by name or ID
        """
        results = []
        search_term = search_term.lower()
        
        for student in self.students:
            if (search_term in student['name'].lower() or 
                search_term in student['student_id'].lower() or
                search_term in student['email'].lower()):
                results.append(student)
        
        return results
    
    def get_statistics(self):
        """
        Get system statistics
        """
        if not self.students:
            return {"total_students": 0}
        
        total = len(self.students)
        
        # Count by grade
        grade_count = {}
        for student in self.students:
            grade = student.get('grade', 'N/A')
            grade_count[grade] = grade_count.get(grade, 0) + 1
        
        return {
            "total_students": total,
            "by_grade": grade_count
        }

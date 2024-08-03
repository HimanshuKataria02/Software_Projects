import mysql.connector
from mysql.connector import Error

# Database connection parameters
config = {
    'host': 'localhost',
    'database': 'students_management',
    'user': 'root',
    'password': 'tiger'
}

def calculate_rank():
    """Calculate and return the rank for a new candidate."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # Fetch current max rank and assign the next rank
        query = "SELECT MAX(`rank`) FROM candidates"
        cursor.execute(query)
        max_rank = cursor.fetchone()[0]
        return max_rank + 1 if max_rank is not None else 1
    except Error as e:
        print(f"Error calculating rank: {e}")
        return 1  # Default to rank 1 in case of an error
    finally:
        cursor.close()
        conn.close()

def add_candidate():
    """Add a new candidate with input validation."""
    student_name = input("Enter student name (max 30 characters): ")
    while len(student_name) > 30 or not student_name.strip():
        student_name = input("Invalid input. Please enter a valid student name (max 30 characters): ")

    college_name = input("Enter college name (max 50 characters): ")
    while len(college_name) > 50 or not college_name.strip():
        college_name = input("Invalid input. Please enter a valid college name (max 50 characters): ")

    try:
        round_one_marks = float(input("Enter marks for round one (0-10): "))
        while round_one_marks < 0 or round_one_marks > 10:
            round_one_marks = float(input("Invalid input. Enter marks for round one (0-10): "))

        round_two_marks = float(input("Enter marks for round two (0-10): "))
        while round_two_marks < 0 or round_two_marks > 10:
            round_two_marks = float(input("Invalid input. Enter marks for round two (0-10): "))

        round_three_marks = float(input("Enter marks for round three (0-10): "))
        while round_three_marks < 0 or round_three_marks > 10:
            round_three_marks = float(input("Invalid input. Enter marks for round three (0-10): "))

        technical_round_marks = float(input("Enter marks for technical round (0-20): "))
        while technical_round_marks < 0 or technical_round_marks > 20:
            technical_round_marks = float(input("Invalid input. Enter marks for technical round (0-20): "))

    except ValueError:
        print("Invalid input. Please enter valid marks.")
        return

    rank = calculate_rank()

    # Save data to database
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        query = """INSERT INTO candidates (student_name, college_name, round_one_marks, 
                   round_two_marks, round_three_marks, technical_round_marks, `rank`) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (student_name, college_name, round_one_marks, round_two_marks, round_three_marks, technical_round_marks, rank))
        conn.commit()
        print("Candidate added successfully")
    except Error as e:
        print(f"Error adding candidate: {e}")
    finally:
        cursor.close()
        conn.close()

def display_candidates():
    """Display all candidates sorted by rank and result."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        query = """SELECT student_name, college_name, round_one_marks, round_two_marks, 
                          round_three_marks, technical_round_marks, total_marks, result, `rank`
                   FROM candidates 
                   ORDER BY `rank` ASC, result DESC"""
        cursor.execute(query)
        candidates = cursor.fetchall()
        print("Candidates:")
        for candidate in candidates:
            print(f"Name: {candidate[0]}, College: {candidate[1]}, Total Marks: {candidate[6]}, Result: {candidate[7]}, Rank: {candidate[8]}")
    except Error as e:
        print(f"Error displaying candidates: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    while True:
        print("1. Add Candidate")
        print("2. Display Candidates")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_candidate()
        elif choice == "2":
            display_candidates()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

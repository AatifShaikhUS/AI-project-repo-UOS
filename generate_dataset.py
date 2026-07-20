import os
import random
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------

TOTAL_STUDENTS = 2000
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

# -----------------------------
# Ensure dataset folder exists
# -----------------------------

os.makedirs("dataset", exist_ok=True)

# -----------------------------
# Helper Functions
# -----------------------------

def calculate_learning_level(
    attendance,
    gpa,
    math,
    english,
    science,
    study_hours,
    assignment,
    quiz
):
    """
    Calculate student learning level
    using weighted academic performance.
    """

    score = (
        attendance * 0.20 +
        gpa * 25 +
        math * 0.15 +
        english * 0.10 +
        science * 0.15 +
        assignment * 0.10 +
        quiz * 0.15 +
        study_hours * 2
    )

    if score >= 90:
        return "Advanced"

    elif score >= 75:
        return "Intermediate"

    else:
        return "Beginner"


# -----------------------------
# Dataset Generation
# -----------------------------

students = []

for student_id in range(1, TOTAL_STUDENTS + 1):

    age = random.randint(16, 23)

    attendance = random.randint(50, 100)

    gpa = round(random.uniform(2.0, 4.0), 2)

    math = random.randint(40, 100)

    english = random.randint(40, 100)

    science = random.randint(40, 100)

    study_hours = round(random.uniform(1.0, 8.0), 1)

    assignment = random.randint(40, 100)

    quiz = random.randint(40, 100)

    learning_level = calculate_learning_level(
        attendance,
        gpa,
        math,
        english,
        science,
        study_hours,
        assignment,
        quiz
    )

    students.append({

        "StudentID": student_id,

        "Age": age,

        "Attendance": attendance,

        "GPA": gpa,

        "Math": math,

        "English": english,

        "Science": science,

        "StudyHours": study_hours,

        "AssignmentCompletion": assignment,

        "QuizScore": quiz,

        "LearningLevel": learning_level

    })

# -----------------------------
# Save Dataset
# -----------------------------

df = pd.DataFrame(students)

dataset_path = "dataset/student_dataset.csv"

df.to_csv(dataset_path, index=False)

print("=" * 60)
print(" AI Tutor Dataset Generated Successfully ")
print("=" * 60)
print(f"Total Students : {len(df)}")
print(f"Dataset Saved  : {dataset_path}")
print("=" * 60)

print("\nFirst Five Records:\n")

print(df.head())

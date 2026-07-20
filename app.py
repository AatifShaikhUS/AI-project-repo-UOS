from flask import Flask, render_template, request, flash
from predict import predict_student
from datetime import datetime
import logging
import traceback

# =====================================================
# Flask Configuration
# =====================================================

app = Flask(__name__)
app.secret_key = "AI_TUTOR_SECRET_KEY_2026"

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =====================================================
# Prediction History
# =====================================================

prediction_history = []

# =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        result=None,
        history=prediction_history,
        chart_data={}
    )

# =====================================================
# Prediction
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ===========================
        # Debug Form Data
        # ===========================

        print("=" * 60)
        print("FORM DATA")
        print(request.form)
        print("=" * 60)

        # ===========================
        # Read Student Data
        # ===========================

        student = {

            "Age": int(request.form["Age"]),

            "Attendance": int(request.form["Attendance"]),

            "GPA": float(request.form["GPA"]),

            "StudyHours": float(request.form["StudyHours"]),

            "Math": int(request.form["Math"]),

            "English": int(request.form["English"]),

            "Science": int(request.form["Science"]),

            "AssignmentCompletion": int(request.form["AssignmentCompletion"]),

            "QuizScore": int(request.form["QuizScore"])

        }

        print("\nStudent Data")
        print(student)

        # ===========================
        # Validation
        # ===========================

        if not (0 <= student["Attendance"] <= 100):
            raise ValueError("Attendance must be between 0 and 100.")

        if not (0 <= student["Math"] <= 100):
            raise ValueError("Math score must be between 0 and 100.")

        if not (0 <= student["English"] <= 100):
            raise ValueError("English score must be between 0 and 100.")

        if not (0 <= student["Science"] <= 100):
            raise ValueError("Science score must be between 0 and 100.")

        if not (0 <= student["AssignmentCompletion"] <= 100):
            raise ValueError("Assignment Completion must be between 0 and 100.")

        if not (0 <= student["QuizScore"] <= 100):
            raise ValueError("Quiz Score must be between 0 and 100.")

        if not (0 <= student["GPA"] <= 4):
            raise ValueError("GPA must be between 0 and 4.")

        if not (0 <= student["StudyHours"] <= 24):
            raise ValueError("Study Hours must be between 0 and 24.")

        # ===========================
        # Prediction
        # ===========================

        prediction = predict_student(student)

        print("\nPrediction Result")
        print(prediction)

        # ===========================
        # Chart Data
        # ===========================

        chart_data = {

            "math": student["Math"],

            "english": student["English"],

            "science": student["Science"],

            "attendance": student["Attendance"],

            "study_hours": student["StudyHours"],

            "assignment": student["AssignmentCompletion"],

            "quiz": student["QuizScore"]

        }

        # ===========================
        # Result
        # ===========================

        result = {

            "LearningLevel": prediction["LearningLevel"],

            "Confidence": prediction["Confidence"],

            "WeakSubject": prediction["WeakSubject"],

            "StrongSubject": prediction["StrongSubject"],

            "Recommendations": prediction["Recommendations"]

        }

        # ===========================
        # Save History
        # ===========================

        prediction_history.append({

            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

            "level": result["LearningLevel"],

            "confidence": result["Confidence"]

        })

        # ===========================
        # Log
        # ===========================

        logging.info(
            f"Prediction Successful | "
            f"Level={result['LearningLevel']} | "
            f"Confidence={result['Confidence']}"
        )

        # ===========================
        # Return Page
        # ===========================

        return render_template(

            "index.html",

            result=result,

            history=prediction_history,

            chart_data=chart_data

        )

    except Exception as e:

        traceback.print_exc()

        logging.error(str(e))

        flash(str(e), "danger")

        return render_template(

            "index.html",

            result=None,

            history=prediction_history,

            chart_data={}

        )

# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True,

        use_reloader=False

    )
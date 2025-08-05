# 🎓 SmartLearn — Interactive Learning & Assessment Platform

SmartLearn is a modern, interactive learning platform built with Django, offering structured exams, real-time question solving, and intelligent session tracking. It's designed to help users practice, track progress, and learn through smart feedback.

> 🚀 Built using Django + Tailwind CSS + CKEditor + PostgreSQL

---

## 🌐 Live Demo

[SmartLearn Demo](http://mokamal1.pythonanywhere.com)

---

## 🔧 Features

- 📚 Categorized exams with subjects & questions
- ✅ Multiple choice questions with explanations
- 🧠 Sessions to simulate real test experiences
- 📊 Track correct/incorrect/skipped answers
- 🔁 Reuse question banks across exams and subjects
- ✏️ Admin-friendly with CKEditor5 integration
- 🧩 Modular structure for scalability

---

## 📦 Tech Stack

- **Backend:** Django, Django ORM, PostgreSQL
- **Frontend:** Django Templates + Tailwind CSS
- **Rich Text:** django-ckeditor-5
- **Authentication:** Django built-in User model
- **Media:** Questions with optional images and explanations

---

## 🗂️ Models Overview

- `Category` → Organizes subjects/exams hierarchically  
- `Exam` → A test composed of questions in a category  
- `Subject` → Ties questions to topics  
- `Question` → Multiple choice questions with optional figure/explanation  
- `Choice` → Choices related to each question (one is correct)  
- `Session` → Simulates a user exam attempt with tracking  
- `Answer` → User responses with correctness tracking  
- `Source` → Tracks question origins or references  
- `Issue` → Users can report issues with questions  
- `TestCategory/TestRow` → For representing lab test-style reference tables (optional)

---

## 📈 Session Flow

1. User starts a session for a selected exam
2. Questions are loaded and shuffled
3. User answers each question
4. After each answer, counts are updated:
   - ✅ Correct
   - ❌ Incorrect
   - ⏭ Skipped
5. Session is marked complete when all questions are answered

---

## 🧪 Sample Usage

```bash
git clone https://github.com/mookamal/smartlearn.git
cd smartlearn
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

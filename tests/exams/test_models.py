def test_category_total_questions(db,category_factory, question_factory,exam_factory):
    category = category_factory()
    category_0 = category_factory()
    exam = exam_factory(category=category)
    question_factory.create_batch(5,exam=exam)
    assert category.total_questions() == 5
    assert category_0.total_questions() == 0

def test_category_total_exams(db,category_factory, exam_factory):
    category = category_factory()
    category_0 = category_factory()
    exam_factory.create_batch(5,category=category,is_visible=True)
    assert category.total_exams() == 5
    assert category_0.total_exams() == 0

def test_exam_str_representation(db, exam_factory):
    exam = exam_factory(name="Midterm Exam")
    assert str(exam) == "Midterm Exam"

def test_exam_get_questions(db, exam_factory, question_factory):
    exam = exam_factory()
    question_factory.create_batch(3, exam=exam, is_approved=True)
    question_factory.create_batch(2, exam=exam, is_approved=False)
    assert exam.get_questions().count() == 3

def test_exam_get_subjects(db, exam_factory, subject_factory, question_factory):
    exam = exam_factory()
    subject1 = subject_factory()
    subject2 = subject_factory()
    question_factory(exam=exam, subject=subject1)
    question_factory(exam=exam, subject=subject1)
    question_factory(exam=exam, subject=subject2)
    subjects = exam.get_subjects()
    assert subjects.count() == 2
    assert subject1 in subjects
    assert subject2 in subjects

def test_exam_get_sources(db, exam_factory, question_factory, source_factory):
    exam = exam_factory()
    source1, source2 = source_factory.create_batch(2)
    q1 = question_factory(exam=exam, is_approved=True, sources=[source1, source2])
    q2 = question_factory(exam=exam, is_approved=True, sources=[source1])
    question_factory(exam=exam, is_approved=False, sources=[source1])
    sources = exam.get_sources()
    assert sources.count() == 2
    assert source1 in sources and source2 in sources

def test_source_str(db, source_factory):
    source = source_factory(name="Textbook Chapter 1")
    assert str(source) == "Textbook Chapter 1"

def test_source_get_questions(db, source_factory, question_factory):
    source = source_factory()
    question_factory.create_batch(3, sources=[source])
    question_factory()
    assert source.get_questions().count() == 3

def test_category_str(db, category_factory):
    category = category_factory(name="Science")
    assert str(category) == "Science"

def test_subject_str(db, subject_factory):
    subject = subject_factory(name="Physics")
    assert str(subject) == "Physics"

def test_subject_get_questions(db, subject_factory, question_factory):
    subject = subject_factory()
    question_factory.create_batch(4, subject=subject)
    question_factory()
    assert subject.get_questions().count() == 4

def test_question_str(db, question_factory):
    s = "What is the speed of light?"
    question = question_factory(text=s)
    assert str(question) == f"Question #{s[:50]}"


def test_choice_str(db, choice_factory):
    choice = choice_factory(text="Option A")
    assert str(choice) == "Option A"

def test_issue_str(db, issue_factory):
    s = "Typo in question text"
    issue = issue_factory(title=s)
    assert str(issue) == s

def test_session_str(db, session_factory):
    session = session_factory(pk=123)
    assert str(session) == "Session #123"

def test_session_state_methods(db, session_factory, question_factory, choice_factory, answer_factory):
    session = session_factory(number_of_questions=5)
    questions = question_factory.create_batch(5)
    session.questions.set(questions)
    
    c1 = choice_factory(question=questions[0], is_right=True)
    c2 = choice_factory(question=questions[1], is_right=False)

    answer_factory(session=session, question=questions[0], choice=c1)
    answer_factory(session=session, question=questions[1], choice=c2)

    session.refresh_from_db()
    assert session.correct_answer_count == 1
    assert session.incorrect_answer_count == 1
    assert session.skipped_answer_count == 3
    assert not session.is_session_completed()

    # Complete the session
    for q in questions[2:]:
        c = choice_factory(question=q, is_right=True)
        answer_factory(session=session, question=q, choice=c)
    
    session.refresh_from_db()
    session.mark_as_completed()
    session.refresh_from_db()
    assert session.is_session_completed()
    assert session.completed

def test_answer_str(db, answer_factory):
    answer = answer_factory()
    expected_str = f"Answer for {answer.question} in Session #{answer.session.pk}"
    assert str(answer) == expected_str

def test_answer_save_logic(db, answer_factory, choice_factory):
    c_right = choice_factory(is_right=True)
    answer = answer_factory(choice=c_right)
    assert answer.is_correct
    assert not answer.is_first # is_first is False on creation

    answer.save() # is_first should be true on subsequent saves
    assert answer.is_first

def test_testcategory_str(db):
    from exams.models import TestCategory
    category = TestCategory.objects.create(title="Blood Tests")
    assert str(category) == "Blood Tests"

def test_testrow_str(db):
    from exams.models import TestCategory, TestRow
    category = TestCategory.objects.create(title="General")
    row = TestRow.objects.create(category=category, test_name="pH", reference_range="7.35-7.45", test_result="7.4")
    assert str(row) == "pH - 7.35-7.45 - 7.4"
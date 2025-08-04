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
    # Approved questions
    question_factory.create_batch(3, exam=exam, is_approved=True)
    # Unapproved questions
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
    source1 = source_factory()
    source2 = source_factory()

    # Approved question with sources
    q1 = question_factory(exam=exam, is_approved=True)
    q1.sources.add(source1, source2)

    # Approved question with a shared source
    q2 = question_factory(exam=exam, is_approved=True)
    q2.sources.add(source1)

    # Unapproved question with a source
    q3 = question_factory(exam=exam, is_approved=False)
    q3.sources.add(source1)

    sources = exam.get_sources()
    assert sources.count() == 2
    assert source1 in sources
    assert source2 in sources
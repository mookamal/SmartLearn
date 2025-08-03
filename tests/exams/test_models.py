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



def test_category_total_questions(db,category_factory, question_factory,exam_factory):
    category = category_factory()
    exam = exam_factory(category=category)
    question_factory.create_batch(5,exam=exam)
    assert category.total_questions() == 5
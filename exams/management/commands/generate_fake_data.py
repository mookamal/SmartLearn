# This file is part of SmartLearn by Mohamed Kamal (github.com/mookamal) – Licensed under the MIT License
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from exams.models import Category, Subject, Source, Exam, Question, Choice, TestCategory, TestRow
from plan.models import SubscriptionPlan


class Command(BaseCommand):
    help = 'Generate fake operational data for SmartLearn'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing data before generating new data',
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=3,
            help='Number of parent categories to create (default: 3)',
        )
        parser.add_argument(
            '--subcategories',
            type=int,
            default=3,
            help='Number of subcategories per parent (default: 3)',
        )
        parser.add_argument(
            '--exams',
            type=int,
            default=2,
            help='Number of exams per subcategory (default: 2)',
        )
        parser.add_argument(
            '--questions',
            type=int,
            default=10,
            help='Number of questions per exam (default: 10)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        flush = options['flush']
        num_parents = options['categories']
        num_subs = options['subcategories']
        num_exams = options['exams']
        num_questions = options['questions']

        if flush:
            self.stdout.write(self.style.WARNING('Deleting existing data...'))
            TestRow.objects.all().delete()
            TestCategory.objects.all().delete()
            Choice.objects.all().delete()
            Question.objects.all().delete()
            Exam.objects.all().delete()
            Source.objects.all().delete()
            Category.objects.all().delete()
            Subject.objects.all().delete()
            SubscriptionPlan.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data deleted.'))

        self.create_subscription_plans()
        self.create_subjects()
        self.create_categories(num_parents, num_subs)
        self.create_sources()
        self.create_exams(num_exams)
        self.create_questions(num_questions)
        self.create_test_categories()

        self.stdout.write(self.style.SUCCESS('\n✓ Fake data generation complete!'))
        self.print_summary()

    def create_subscription_plans(self):
        self.stdout.write('Creating subscription plans...')
        plans_data = [
            {'name': 'FREE', 'sessions_per_month': 5, 'price': 0.00, 'description': 'Free plan with 5 sessions per month'},
            {'name': 'BASIC', 'sessions_per_month': 50, 'price': 9.99, 'description': 'Basic plan with 50 sessions per month'},
            {'name': 'PREMIUM', 'sessions_per_month': 200, 'price': 19.99, 'description': 'Premium plan with 200 sessions per month'},
        ]
        for data in plans_data:
            SubscriptionPlan.objects.get_or_create(
                name=data['name'],
                defaults={
                    'sessions_per_month': data['sessions_per_month'],
                    'price': data['price'],
                    'description': data['description']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(plans_data)} subscription plans'))

    def create_subjects(self):
        self.stdout.write('Creating subjects...')
        subject_names = [
            'Hematology', 'Biochemistry', 'Microbiology', 'Immunology',
            'Histopathology', 'Molecular Biology', 'Clinical Chemistry',
            'Blood Banking', 'Genetics', 'Endocrinology'
        ]
        for name in subject_names:
            Subject.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(subject_names)} subjects'))

    def create_categories(self, num_parents, num_subs):
        self.stdout.write('Creating categories...')
        parent_categories = [
            'Medical Laboratory Science',
            'Clinical Pathology',
            'Diagnostic Imaging',
            'Microbiology Testing',
            'Blood Sciences'
        ]
        subcategory_templates = [
            'Basic {parent}', 'Advanced {parent}', 'Specialized {parent}',
            'Emergency {parent}', 'Pediatric {parent}', 'Research {parent}'
        ]

        created_parents = 0
        created_subs = 0

        for i in range(min(num_parents, len(parent_categories))):
            parent_name = parent_categories[i]
            parent, _ = Category.objects.get_or_create(
                name=parent_name,
                defaults={
                    'slug': slugify(parent_name),
                    'is_listed': True
                }
            )
            created_parents += 1

            for j in range(num_subs):
                sub_name = subcategory_templates[j % len(subcategory_templates)].format(parent=parent_name)
                Category.objects.get_or_create(
                    name=sub_name,
                    defaults={
                        'slug': slugify(sub_name),
                        'parent_category': parent,
                        'is_listed': True
                    }
                )
                created_subs += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_parents} parent and {created_subs} sub categories'))

    def create_sources(self):
        self.stdout.write('Creating sources...')
        sources_data = [
            'Harrison Principles of Internal Medicine',
            'Robbins Basic Pathology',
            'Clinical Laboratory Science',
            'Diagnostic Hematology',
            'Medical Microbiology',
            'Tietz Textbook of Clinical Chemistry',
            'Henry Clinical Diagnosis',
            'Modern Blood Banking',
            'Immunology for Clinical Laboratory',
            'Molecular Diagnostics'
        ]
        categories = list(Category.objects.filter(parent_category__isnull=False))

        for source_name in sources_data:
            category = random.choice(categories) if categories else None
            Source.objects.get_or_create(
                name=source_name,
                defaults={'category': category}
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(sources_data)} sources'))

    def create_exams(self, num_exams):
        self.stdout.write('Creating exams...')
        subcategories = Category.objects.filter(parent_category__isnull=False)
        exam_templates = [
            'Introduction to {subject}',
            'Advanced {subject} Concepts',
            'Clinical {subject} Practice',
            '{subject} Case Studies',
            'Essential {subject} Skills',
            '{subject} for Beginners',
            'Mastering {subject}',
            'Practical {subject} Applications'
        ]

        created = 0
        subjects = list(Subject.objects.all())

        for subcategory in subcategories:
            for i in range(num_exams):
                subject = random.choice(subjects)
                exam_name = random.choice(exam_templates).format(subject=subject.name)
                exam_name = f'{exam_name} - {subcategory.name}'

                description = f'<p>This exam covers essential topics in {subject.name} under {subcategory.name}. ' \
                            f'It includes questions on practical applications, theoretical concepts, and clinical scenarios.</p>'

                Exam.objects.get_or_create(
                    name=exam_name,
                    defaults={
                        'category': subcategory,
                        'is_visible': True,
                        'description': description
                    }
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created} exams'))

    def create_questions(self, num_questions):
        self.stdout.write('Creating questions with choices...')
        exams = list(Exam.objects.all())
        subjects = list(Subject.objects.all())
        sources = list(Source.objects.all())

        question_templates = [
            {
                'text': 'What is the normal range for {parameter} in adult patients?',
                'choices': ['{low}-{high} g/dL', '{high}-{higher} g/dL', 'Less than {low} g/dL', 'More than {higher} g/dL'],
                'explanation': 'The normal range for {parameter} in adults is {low}-{high} g/dL. Values outside this range may indicate various conditions.'
            },
            {
                'text': 'Which of the following is the primary function of {component}?',
                'choices': [
                    '{function_primary}',
                    '{function_secondary}',
                    '{function_wrong1}',
                    '{function_wrong2}'
                ],
                'explanation': '{component} primarily functions to {function_primary}. This is essential for {process}.'
            },
            {
                'text': 'A patient presents with {symptom1} and {symptom2}. What is the most likely diagnosis?',
                'choices': ['{diagnosis_correct}', '{diagnosis_wrong1}', '{diagnosis_wrong2}', '{diagnosis_wrong3}'],
                'explanation': 'The combination of {symptom1} and {symptom2} is characteristic of {diagnosis_correct}. Other options present with different clinical pictures.'
            },
            {
                'text': 'In {test_name}, what does an elevated result indicate?',
                'choices': [
                    '{condition1}',
                    '{condition2}',
                    'Normal function',
                    'Laboratory error'
                ],
                'explanation': 'Elevated {test_name} typically indicates {condition1}. It may also suggest {condition2} in some cases.'
            },
            {
                'text': 'Which cell type is responsible for {function}?',
                'choices': ['{cell_correct}', '{cell_wrong1}', '{cell_wrong2}', '{cell_wrong3}'],
                'explanation': '{cell_correct} are specialized cells that handle {function} in the body.'
            }
        ]

        created_questions = 0
        created_choices = 0

        for exam in exams:
            subject = random.choice(subjects)
            sources_for_question = random.sample(sources, k=min(2, len(sources)))

            for i in range(num_questions):
                template = random.choice(question_templates)
                
                # Generate placeholder values
                values = self.generate_placeholder_values()
                
                question_text = template['text'].format(**values)
                explanation = template['explanation'].format(**values)

                question, _ = Question.objects.get_or_create(
                    text=question_text,
                    defaults={
                        'subject': subject,
                        'exam': exam,
                        'explanation': explanation,
                        'is_approved': True,
                        'reference': f'{random.choice(sources).name}, Chapter {random.randint(1, 20)}'
                    }
                )
                question.sources.set(sources_for_question)
                created_questions += 1

                # Create choices
                choice_texts = template['choices']
                correct_idx = 0  # First choice is always correct
                
                for idx, choice_template in enumerate(choice_texts):
                    choice_text = choice_template.format(**values)
                    Choice.objects.get_or_create(
                        text=choice_text,
                        question=question,
                        defaults={'is_right': idx == correct_idx}
                    )
                    created_choices += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_questions} questions with {created_choices} choices'))

    def generate_placeholder_values(self):
        parameters = ['Hemoglobin', 'Hematocrit', 'White Blood Cells', 'Platelets', 'Glucose', 'Creatinine', 'Urea', 'Sodium', 'Potassium', 'Calcium']
        components = ['Red Blood Cells', 'White Blood Cells', 'Platelets', 'Neutrophils', 'Lymphocytes', 'Monocytes', 'Eosinophils', 'Basophils']
        symptoms = ['fatigue', 'fever', 'weight loss', 'headache', 'chest pain', 'shortness of breath', 'nausea', 'joint pain']
        diagnoses = ['Anemia', 'Leukemia', 'Infection', 'Thrombocytopenia', 'Diabetes Mellitus', 'Kidney Disease', 'Liver Disease', 'Autoimmune Disorder']
        tests = ['Complete Blood Count', 'Liver Function Test', 'Kidney Function Test', 'Blood Glucose', 'Hemoglobin A1C', 'Thyroid Panel']
        functions = ['oxygen transport', 'immune defense', 'blood clotting', 'waste removal', 'nutrient transport', 'temperature regulation']
        cells = ['Erythrocytes', 'Leukocytes', 'Thrombocytes', 'Neutrophils', 'Macrophages', 'Lymphocytes']
        
        low_val = random.randint(10, 30)
        high_val = low_val + random.randint(5, 15)
        higher_val = high_val + random.randint(5, 10)

        return {
            'parameter': random.choice(parameters),
            'low': low_val,
            'high': high_val,
            'higher': higher_val,
            'component': random.choice(components),
            'function_primary': random.choice(['transport oxygen', 'fight infections', 'prevent bleeding', 'regulate temperature']),
            'function_secondary': random.choice(['maintain pH balance', 'transport nutrients', 'remove waste products']),
            'function_wrong1': random.choice(['produce hormones', 'store fat', 'synthesize proteins']),
            'function_wrong2': random.choice(['digest food', 'filter air', 'absorb sunlight']),
            'process': random.choice(['homeostasis', 'metabolism', 'cellular respiration']),
            'symptom1': random.choice(symptoms),
            'symptom2': random.choice(symptoms),
            'diagnosis_correct': random.choice(diagnoses),
            'diagnosis_wrong1': random.choice([d for d in diagnoses if d != random.choice(diagnoses)]),
            'diagnosis_wrong2': random.choice(diagnoses),
            'diagnosis_wrong3': random.choice(diagnoses),
            'test_name': random.choice(tests),
            'condition1': random.choice(['tissue damage', 'infection', 'inflammation', 'organ dysfunction']),
            'condition2': random.choice(['chronic disease', 'acute stress', 'medication effects']),
            'function': random.choice(functions),
            'cell_correct': random.choice(cells),
            'cell_wrong1': random.choice(cells),
            'cell_wrong2': random.choice(cells),
            'cell_wrong3': random.choice(cells),
        }

    def create_test_categories(self):
        self.stdout.write('Creating test categories and rows...')
        test_categories_data = [
            {
                'title': 'Complete Blood Count (CBC)',
                'rows': [
                    ('Hemoglobin', '12-16 g/dL', 'Normal'),
                    ('Hematocrit', '36-46%', 'Normal'),
                    ('WBC Count', '4,500-11,000/μL', 'Normal'),
                    ('Platelet Count', '150,000-400,000/μL', 'Normal'),
                ]
            },
            {
                'title': 'Liver Function Panel',
                'rows': [
                    ('ALT', '7-56 U/L', 'Normal'),
                    ('AST', '10-40 U/L', 'Normal'),
                    ('Bilirubin', '0.1-1.2 mg/dL', 'Normal'),
                    ('Albumin', '3.5-5.0 g/dL', 'Normal'),
                ]
            },
            {
                'title': 'Lipid Profile',
                'rows': [
                    ('Total Cholesterol', '< 200 mg/dL', 'Desirable'),
                    ('LDL Cholesterol', '< 100 mg/dL', 'Optimal'),
                    ('HDL Cholesterol', '> 40 mg/dL', 'Good'),
                    ('Triglycerides', '< 150 mg/dL', 'Normal'),
                ]
            }
        ]

        created_cats = 0
        created_rows = 0

        for cat_data in test_categories_data:
            category, _ = TestCategory.objects.get_or_create(title=cat_data['title'])
            created_cats += 1
            
            for row_data in cat_data['rows']:
                TestRow.objects.get_or_create(
                    category=category,
                    test_name=row_data[0],
                    defaults={
                        'reference_range': row_data[1],
                        'test_result': row_data[2]
                    }
                )
                created_rows += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_cats} test categories with {created_rows} rows'))

    def print_summary(self):
        self.stdout.write('\n' + '='*50)
        self.stdout.write('SUMMARY')
        self.stdout.write('='*50)
        self.stdout.write(f'Subscription Plans: {SubscriptionPlan.objects.count()}')
        self.stdout.write(f'Categories: {Category.objects.count()} (Parents: {Category.objects.filter(parent_category__isnull=True).count()})')
        self.stdout.write(f'Subjects: {Subject.objects.count()}')
        self.stdout.write(f'Sources: {Source.objects.count()}')
        self.stdout.write(f'Exams: {Exam.objects.count()}')
        self.stdout.write(f'Questions: {Question.objects.count()}')
        self.stdout.write(f'Choices: {Choice.objects.count()}')
        self.stdout.write(f'Test Categories: {TestCategory.objects.count()}')
        self.stdout.write('='*50)

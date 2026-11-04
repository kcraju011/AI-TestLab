TEST_SUITES = {
    "basic_qa": [
        {
            "test_id": "QA001",
            "question": "What is Python?",
            "expected_answer": "Python is a programming language.",
            "actual_answer": "Python is a programming language."
        },
        {
            "test_id": "QA002",
            "question": "What is SQL?",
            "expected_answer": "SQL is used to manage databases.",
            "actual_answer": "SQL is used to manage databases."
        },
        {
            "test_id": "QA003",
            "question": "What is an API?",
            "expected_answer": "An API allows software systems to communicate.",
            "actual_answer": "An API allows software systems to communicate."
        }
    ],

    "negative_qa": [
        {
            "test_id": "NEG001",
            "question": "Can Python execute Java bytecode directly?",
            "expected_answer": "No, Python cannot directly execute Java bytecode.",
            "actual_answer": "Yes, Python directly executes Java bytecode."
        },
        {
            "test_id": "NEG002",
            "question": "Is SQL a programming language for styling web pages?",
            "expected_answer": "No, SQL is used to manage relational databases.",
            "actual_answer": "No, SQL is used to manage relational databases."
        }
    ]
}
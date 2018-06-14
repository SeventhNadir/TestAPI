import requests
import random

example_api = "https://knockknock.readify.net/api/"
implementation = "http://127.0.0.1:5000/api/"
implementation1 = "http://flask-env1.adjmtcsdm8.us-west-2.elasticbeanstalk.com/api/"


def validate_fibonacci(n):

    example_api_fib = requests.get(f"{example_api}Fibonacci?n={n}").content
    implementation_fib = requests.get(f"{implementation}Fibonacci?n={n}").content

    return example_api_fib == implementation_fib


def validate_reverse_words(sentence):

    example_api_rev = requests.get(
        f"{example_api}ReverseWords?sentence={sentence}"
    ).content
    implementation_rev = requests.get(
        f"{implementation}ReverseWords?sentence={sentence}"
    ).content
    return example_api_rev == implementation_rev


def validate_triangle_type(a, b, c):

    example_api_tri = requests.get(
        f"{example_api}TriangleType?a={a}&b={b}&c={c}"
    ).content
    implementation_tri = requests.get(
        f"{implementation}TriangleType?a={a}&b={b}&c={c}"
    ).content

    return example_api_tri == implementation_tri


def test_suite_fibonacci():
    #  Positive test cases
    for i in range(-25, 50):
        assert validate_fibonacci(i)

    #  Negative & edge test cases
    test_cases = [999, 1.5, "abc"]
    for test in test_cases:
        try:
            assert validate_fibonacci(test)
        except Exception as e:
            print(e)


def test_suite_reverse_words():
    #  Positive test cases
    test_cases = [
        "one",
        "19",
        "longer sentence",
        "long sentence & special characters",
        "commas, punctuation.",
        r"\\\\\\\\\\\\\\\\\\\\\\\\\\",
        r"????????????\\\\!!!!!",
    ]
    for test in test_cases:
        validate_reverse_words(test)

    #  Negative test cases
    test_cases = ["", "ØÙæ", "目に見えない", "웨스턴오스트레일리아 주"]
    for test in test_cases:
        validate_reverse_words(test)


def test_suite_triangle_types():
    #  Positive test cases
    for iteration in range(1):
        a, b, c = random.sample(range(1, 100), 3)
        assert validate_triangle_type(a, b, c)
    for iteration in range(1):
        a, b = random.sample(range(1, 100), 2)
        assert validate_triangle_type(a, b, b)
    for iteration in range(1):
        a = random.sample(range(1, 100), 1)[0]
        assert validate_triangle_type(a, a, a)
    #  Negative test cases
    test_cases = (
        [0, 0, 0],
        [-1, 1, 1],
        [1, 2],
        [1, 2, 3, 4],
        ["trianglestuff", 6, 5],
        [1.5, 1.5, 1.5],
    )
    for test in test_cases:
        try:
            a, b, c = test
            assert validate_triangle_type(a, b, c)
        except Exception as e:
            print(e)


test_suite_triangle_types()
test_suite_reverse_words()
test_suite_fibonacci()

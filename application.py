from flask import Flask, request
import json

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# If this API was used in prod, we'd be using a database to store our cache.
# In memory data representation appropriate for this use case, but won't scale out.

computation_cache = dict()
computation_cache[0] = 0  # Zero is a special case.


@application.route("/api/Fibonacci", methods=["GET"])
def get_fibonacci():
    try:
        n = int(request.args.get("n"))
        return str(calculate_fibonacci(n))
    except RecursionError:
        return "recursion error"
    except Exception:
        return json.dumps({"message": "The request is invalid."})


@application.route("/api/ReverseWords", methods=["GET"])
def get_reverse_words():
    try:
        sentence = str(request.args.get("sentence"))
        reversed_sentence = reverse_words(sentence)
        return json.dumps(reversed_sentence, ensure_ascii=False).encode("utf8")
    except Exception:
        return json.dumps("Error")


@application.route("/api/Token", methods=["GET"])
def get_token():
    #  If this was a secret, store in secrets file or env variable. Not needed here.
    return json.dumps("9730770d-13d5-4a7c-ba84-6850ba43dccb")


@application.route("/api/TriangleType", methods=["GET"])
def get_triangle_types():
    try:
        a, b, c = request.args.get("a"), request.args.get("b"), request.args.get("c")
        a, b, c = int(a), int(b), int(c)  # Convert to int and handle invalid input
        for side in [a, b, c]:
            if side <= 0:  # Assumption: Sides cannot have negative or zero length
                raise NotImplementedError  # No support for non-Euclidean triangles
        return json.dumps(str(triangle_type(a, b, c)))
    except NotImplementedError:
        return json.dumps("Error")
    except Exception:
        return json.dumps({"message": "The request is invalid."})


def calculate_fibonacci(n):
    """Returns the nth fibonacci number"""
    if n in computation_cache:
        return computation_cache[n]
    if n > -1:
        if n == 1:
            return 1
        else:
            computation = calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
            computation_cache[n] = computation
            return computation
    if n <= -1:  # For the bidirectional series
        return int((-1) ** (n + 1)) * calculate_fibonacci(-n)


def reverse_words(sentence):
    """For word in sentence, reverse letter order"""
    words = sentence.split(" ")
    reversed_words = [word[::-1] for word in words]
    return " ".join(reversed_words)


def triangle_type(a, b, c):
    def triangle_inequality_theorem(
        a, b, c
    ):  # z < x + y (z denoting the greatest side)
        sides = [a, b, c]
        sides.sort()
        x, y, z = sides
        if z < x + y:
            return True
        else:
            return False

    if triangle_inequality_theorem(a, b, c):
        if a == b and b == c:  # a == c not required due to transitive property
            return "Equilateral"
        if a == b or a == c or b == c:
            return "Isosceles"
        else:  # Invalid input would return "Scalene" if not checked in calling function
            return "Scalene"
    else:
        return "Error"


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True

    application.run()

from flask import Flask, jsonify, request

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
        return calculate_fibonacci(n)
    except RecursionError:
        return "recursion error"
    except Exception:
        return "error"


@application.route("/api/ReverseWords", methods=["GET"])
def get_reverse_words():
    try:
        sentence = str(request.args.get("sentence"))
        return jsonify(reverse_words(sentence))
    except Exception:
        return jsonify("Error")


@application.route("/api/Token", methods=["GET"])
def get_token():
    #  If this was a secret, store in secrets file or env variable. Not needed here.
    return jsonify("9730770d-13d5-4a7c-ba84-6850ba43dccb")


@application.route("/api/TriangleType", methods=["GET"])
def get_triangle_types():
    try:
        a, b, c = request.args.get("a"), request.args.get("b"), request.args.get("c")
        a, b, c = int(a), int(b), int(c)  # Convert to int and handle invalid input
        for side in [a, b, c]:
            assert side > 0  # Assumption: Sides cannot have negative or zero length

        return jsonify(triangle_type(a, b, c))
    except Exception:
        return jsonify("The request is invalid")


def calculate_fibonacci(n):
    """Returns the nth fibonacci number"""
    if n in computation_cache:
        return computation_cache[n]
    if n == 1:
        return 1
    else:
        computation = calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
        computation_cache[n] = computation
        return computation


def reverse_words(sentence):
    """For word in sentence, reverse letter order"""
    words = sentence.split(" ")
    reversed_words = [word[::-1] for word in words]
    return " ".join(reversed_words)


def triangle_type(a, b, c):

    if a == b and b == c:  # a == c not required due to transitive property
        return "Equilateral"
    if a == b or a == c or b == c:
        return "Isoceles"
    else:  # Invalid input would return "Scalene" if not checked in calling function
        return "Scalene"

    return calculate_triangle_type(a, b, c)


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True

    application.run()

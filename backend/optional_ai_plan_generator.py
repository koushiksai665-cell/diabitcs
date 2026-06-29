"""
Optional addition to app.py — generates a personalized diet/exercise
plan using an external AI API (example uses Anthropic's Claude API).

IMPORTANT: The API key NEVER goes in the HTML/JS frontend — anyone could
open dev tools and steal it. It lives only on the server, in an
environment variable.
"""
import os
import anthropic  # pip install anthropic

# Set this in your terminal before running app.py:
#   export ANTHROPIC_API_KEY="sk-ant-..."
# Never hardcode the key in your source files or commit it to GitHub.
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def generate_plan(risk_category, glucose, bmi, age):
    prompt = (
        f"Create a concise 7-day diet and exercise plan for someone "
        f"classified as '{risk_category}' for diabetes risk. "
        f"Glucose: {glucose}, BMI: {bmi}, Age: {age}. "
        f"Keep it practical and structured by day."
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


# Then add a new route in app.py:
#
# @app.route("/generate-plan", methods=["POST"])
# def plan_route():
#     data = request.get_json()
#     plan_text = generate_plan(data["risk_category"], data["glucose"],
#                                data["bmi"], data["age"])
#     return jsonify({"plan": plan_text})

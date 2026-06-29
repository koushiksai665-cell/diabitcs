"""
ai_plan_generator.py
Generates a personalized 7-day diet and exercise plan.
Supports Google Gemini API, Hugging Face API, and a robust offline fallback.
"""
import os
import json
import requests

def generate_local_plan(risk_category, glucose, bmi, age):
    """
    Generates a highly structured, tailored 7-day plan locally without calling external APIs.
    """
    # Customize recommendations based on clinical factors
    is_high_risk = risk_category in ["Diabetic", "At Risk"]
    is_overweight = bmi >= 25.0
    is_high_glucose = glucose >= 130
    is_senior = age >= 60

    # Diet strategy
    diet_focus = "General Balanced Nutrition"
    if is_high_risk:
        diet_focus = "Low Glycemic Index & Carb Control"
    elif is_overweight:
        diet_focus = "Caloric Deficit & High Protein"

    diet_tips = [
        "Focus on non-starchy vegetables (spinach, broccoli, cauliflower).",
        "Prioritize lean proteins (chicken, fish, tofu, legumes) to maintain muscle mass."
    ]
    if is_high_risk:
        diet_tips.append("Limit refined carbohydrates (white bread, white rice) and added sugars.")
        diet_tips.append("Spread carbohydrate intake evenly throughout the day to prevent glucose spikes.")
    if is_high_glucose:
        diet_tips.append("Avoid sugar-sweetened beverages and high-glycemic fruits like watermelons or ripe bananas.")
    if is_overweight:
        diet_tips.append("Practice portion control and drink a glass of water 15 minutes before meals.")

    # Exercise strategy
    exercise_type = "Moderate-intensity cardio & strength training"
    if is_senior:
        exercise_type = "Low-impact joints-friendly activities"
    elif is_high_risk and is_overweight:
        exercise_type = "Brisk walking and progressive resistance training"

    exercise_tips = [
        "Stay active throughout the day. Take a 10-minute walk after major meals.",
        "Ensure adequate hydration before, during, and after physical exercise."
    ]
    if is_senior:
        exercise_tips.append("Focus on balance, flexibility, and light strength training (e.g., Yoga, Swimming, Tai Chi).")
    else:
        exercise_tips.append("Aim for at least 150 minutes of moderate-intensity aerobic exercise per week.")
        exercise_tips.append("Include 2 days of strength/resistance training to build insulin-sensitive muscle tissue.")

    # Generate 7-day schedule
    days = {}
    
    # Template meals based on risk
    meals_diabetic = [
        {"breakfast": "Oatmeal topped with walnuts & chia seeds", "lunch": "Grilled chicken breast with a large green salad", "snack": "A handful of almonds", "dinner": "Baked salmon with steamed broccoli and quinoa"},
        {"breakfast": "Scrambled eggs with spinach and cherry tomatoes", "lunch": "Quinoa bowl with mixed veggies and grilled tofu", "snack": "Greek yogurt (unsweetened)", "dinner": "Turkey stir-fry with cauliflower rice"},
        {"breakfast": "Chia seed pudding with a few berries", "lunch": "Lentil soup with a side of steamed spinach", "snack": "Cucumber slices with hummus", "dinner": "Grilled mackerel with asparagus and wild rice"},
        {"breakfast": "Avocado toast on 100% whole grain bread", "lunch": "Tuna salad lettuce wraps with olive oil dressing", "snack": "One boiled egg", "dinner": "Chicken breast with baked brussels sprouts"},
        {"breakfast": "Protein smoothie (whey/vegan protein, spinach, almond milk)", "lunch": "Chickpea salad with diced cucumber, tomatoes, and feta", "snack": "Celery sticks with peanut butter", "dinner": "Baked cod with a side of roasted zucchini"},
        {"breakfast": "Oat bran with flaxseeds and unsweetened almond milk", "lunch": "Turkey breast slice salad with mixed leafy greens", "snack": "A small cup of mixed berries", "dinner": "Tofu vegetable curry with brown rice (small portion)"},
        {"breakfast": "Veggie omelet (2 eggs) cooked in olive oil", "lunch": "Black bean and avocado salad with lime vinaigrette", "snack": "A handful of pumpkin seeds", "dinner": "Grilled shrimp skewers with bell peppers and onions"}
    ]

    meals_healthy = [
        {"breakfast": "Whole-grain cereal with skim milk and banana slices", "lunch": "Brown rice bowl with black beans and grilled chicken", "snack": "Apple slices", "dinner": "Whole wheat pasta with marinara sauce and turkey meatballs"},
        {"breakfast": "Fruit smoothie with Greek yogurt and honey", "lunch": "Turkey wrap with whole wheat tortilla and lettuce", "snack": "Baby carrots with hummus", "dinner": "Baked salmon with sweet potato and green beans"},
        {"breakfast": "Oatmeal with honey and fresh strawberries", "lunch": "Quinoa salad with tomatoes, cucumbers, and olive oil", "snack": "Mixed nuts", "dinner": "Lean beef stir-fry with mixed vegetables and jasmine rice"},
        {"breakfast": "Poached eggs on sourdough toast", "lunch": "Lentil soup with whole-grain crackers", "snack": "Greek yogurt with fruit", "dinner": "Grilled chicken skewers with bell peppers and couscous"},
        {"breakfast": "Granola with almond milk and blueberries", "lunch": "Spinach salad with grilled chicken and vinaigrette", "snack": "Rice cakes with almond butter", "dinner": "Baked sea bass with roasted potatoes and salad"},
        {"breakfast": "Scrambled eggs with whole wheat toast", "lunch": "Tuna salad sandwich on whole wheat bread", "snack": "A small orange", "dinner": "Vegetarian chili with a side of cornbread"},
        {"breakfast": "Burrito bowl with brown rice, salsa, and lean beef", "lunch": "Cottage cheese with pineapple chunks", "snack": "A small handful of mixed seeds", "dinner": "Grilled pork chop with applesauce and roasted broccoli"}
    ]

    # Active routines
    exercises = [
        "30 mins brisk walking + 10 mins post-dinner stroll",
        "20 mins light bodyweight exercises (squats, pushups, lunges)",
        "30 mins cycling or swimming at moderate pace",
        "Rest day: 15 mins gentle stretching or yoga",
        "30 mins brisk walking or jog + 15 mins strength training",
        "40 mins outdoor hike or active recreation",
        "Rest day: Light walk or stretching"
    ]

    active_meals = meals_diabetic if is_high_risk else meals_healthy

    for idx in range(7):
        day_num = idx + 1
        meal = active_meals[idx]
        ex = exercises[idx]
        if is_senior:
            ex = ex.replace("jog", "walk").replace("strength training", "light stretching").replace("hike", "flat trail walk")
            
        days[f"Day {day_num}"] = {
            "Diet": {
                "Breakfast": meal["breakfast"],
                "Lunch": meal["lunch"],
                "Snack": meal["snack"],
                "Dinner": meal["dinner"]
            },
            "Exercise": ex
        }

    plan_title = f"7-Day Health Plan for '{risk_category}' Profile"
    summary = f"This plan is tailored for a {age}-year-old with a BMI of {bmi} and fasting/random glucose level of {glucose} mg/dL. It focuses on: {diet_focus} and {exercise_type}."

    return {
        "title": plan_title,
        "summary": summary,
        "diet_focus": diet_focus,
        "exercise_focus": exercise_type,
        "diet_tips": diet_tips,
        "exercise_tips": exercise_tips,
        "schedule": days,
        "generator": "Local Rule-Based Engine (Offline)"
    }


def generate_gemini_plan(api_key, risk_category, glucose, bmi, age):
    """
    Calls the Google Gemini API to generate a personalized health plan.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = (
        f"You are a medical dietitian and fitness coach. "
        f"Create a structured, personalized 7-day diet and exercise plan for a patient with the following profile:\n"
        f"- Diabetes Risk Classification: {risk_category}\n"
        f"- Blood Glucose Level: {glucose} mg/dL\n"
        f"- BMI: {bmi}\n"
        f"- Age: {age} years\n\n"
        f"Return ONLY a JSON object matching this exact schema (no markdown, no backticks, no wrap):\n"
        f"{{\n"
        f"  \"title\": \"Plan Title\",\n"
        f"  \"summary\": \"Brief medical summary and rationale\",\n"
        f"  \"diet_focus\": \"Core dietary target\",\n"
        f"  \"exercise_focus\": \"Core exercise target\",\n"
        f"  \"diet_tips\": [\"tip 1\", \"tip 2\"],\n"
        f"  \"exercise_tips\": [\"tip 1\", \"tip 2\"],\n"
        f"  \"schedule\": {{\n"
        f"    \"Day 1\": {{\n"
        f"      \"Diet\": {{\n"
        f"        \"Breakfast\": \"...\",\n"
        f"        \"Lunch\": \"...\",\n"
        f"        \"Snack\": \"...\",\n"
        f"        \"Dinner\": \"...\"\n"
        f"      }},\n"
        f"      \"Exercise\": \"Description of exercise\"\n"
        f"    }},\n"
        f"    ... up to Day 7\n"
        f"  }}\n"
        f"}}"
    )
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=15)
    response.raise_for_status()
    
    result_json = response.json()
    text_content = result_json["candidates"][0]["content"]["parts"][0]["text"]
    
    plan = json.loads(text_content.strip())
    plan["generator"] = "Google Gemini 1.5 Flash (AI Generated)"
    return plan


def generate_hf_plan(api_token, risk_category, glucose, bmi, age):
    """
    Calls Hugging Face Serverless Inference API to generate a personalized health plan.
    """
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"You are a medical dietitian. Create a structured 7-day diet and exercise plan for a patient:\n"
        f"- Diabetes Risk: {risk_category}\n"
        f"- Glucose: {glucose} mg/dL\n"
        f"- BMI: {bmi}\n"
        f"- Age: {age}\n"
        f"You must return ONLY a raw valid JSON object. Do not wrap in ```json or markdown. Match this schema:\n"
        f"{{\n"
        f"  \"title\": \"Plan Title\",\n"
        f"  \"summary\": \"Brief rationale\",\n"
        f"  \"diet_focus\": \"Diet goal\",\n"
        f"  \"exercise_focus\": \"Exercise goal\",\n"
        f"  \"diet_tips\": [\"tip 1\"],\n"
        f"  \"exercise_tips\": [\"tip 1\"],\n"
        f"  \"schedule\": {{\n"
        f"    \"Day 1\": {{\n"
        f"      \"Diet\": {{\"Breakfast\": \"...\", \"Lunch\": \"...\", \"Snack\": \"...\", \"Dinner\": \"...\"}},\n"
        f"      \"Exercise\": \"...\"\n"
        f"    }},\n"
        f"    ... up to Day 7\n"
        f"  }}\n"
        f"}}\n<|eot_id|>"
        f"<|start_header_id|>user<|end_header_id|>\nGenerate the JSON now.<|eot_id|>"
        f"<|start_header_id|>assistant<|end_header_id|>\n"
    )
    
    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1200,
            "temperature": 0.2,
            "return_full_text": False
        }
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=20)
    response.raise_for_status()
    
    result = response.json()
    
    # Hugging Face usually returns a list of dictionaries with 'generated_text'
    if isinstance(result, list) and len(result) > 0:
        generated_text = result[0].get("generated_text", "")
    else:
        generated_text = result.get("generated_text", "")
        
    # Attempt to clean up text and parse JSON
    text_content = generated_text.strip()
    # Find the first '{' and last '}'
    start_idx = text_content.find('{')
    end_idx = text_content.rfind('}')
    if start_idx != -1 and end_idx != -1:
        text_content = text_content[start_idx:end_idx+1]
        
    plan = json.loads(text_content)
    plan["generator"] = "Hugging Face Llama-3-8B (AI Generated)"
    return plan


def generate_plan(risk_category, glucose, bmi, age):
    """
    Main entry point. Decides which generator to use based on available keys.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    hf_token = os.environ.get("HF_API_KEY")
    
    # Try Gemini first
    if gemini_key:
        try:
            return generate_gemini_plan(gemini_key, risk_category, glucose, bmi, age)
        except Exception as e:
            print(f"Gemini API error: {e}. Falling back...")
            
    # Try Hugging Face next
    if hf_token:
        try:
            return generate_hf_plan(hf_token, risk_category, glucose, bmi, age)
        except Exception as e:
            print(f"Hugging Face API error: {e}. Falling back...")
            
    # Fallback to local rule engine
    return generate_local_plan(risk_category, glucose, bmi, age)

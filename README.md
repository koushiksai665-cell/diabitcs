# AI-Based Diabetes Predictor

A diabetes risk screening web application combining a weighted ensemble
machine learning model (Random Forest + Gradient Boosting) with an
automated Diabetes Pedigree Function calculator and a personalized
diet/exercise plan generator.

## Repository structure

```
.
├── backend/
│   ├── app.py                       # Flask API serving the trained model
│   ├── train_model.py               # Trains and exports diabetes_ensemble.pkl
│   ├── optional_ai_plan_generator.py # Optional: external AI API for diet plans
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── diabetes_ai_v3.html          # The web application (replace placeholder)
│   └── api_integration_snippet.html # Reference fetch() code for calling the API
├── .gitignore
└── README.md
```

## Dataset

Trained on the Pima Indians Diabetes Dataset (768 records, 8 clinical
features). `train_model.py` fetches it automatically over HTTPS at
training time — no manual download or Kaggle login required:

```
https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv
```

Original source: National Institute of Diabetes and Digestive and Kidney
Diseases (Smith et al., 1988).

## Running locally

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python train_model.py      # creates diabetes_ensemble.pkl
python app.py               # starts API at http://localhost:5000
```

Verify it's running:

```bash
curl http://localhost:5000/health
```

### 2. Frontend

Open `frontend/diabetes_ai_v3.html` directly in a browser. Make sure
`API_BASE` inside the file's `<script>` block points to
`http://localhost:5000` for local testing.

## Deploying the backend (free tier)

This repo includes a `Dockerfile` ready for **Google Cloud Run**:

```bash
cd backend
gcloud run deploy diabetes-api --source . --allow-unauthenticated
```

Cloud Run gives you a public HTTPS URL. Update `API_BASE` in
`diabetes_ai_v3.html` to that URL once deployed.

Alternatives: Render, Railway, or PythonAnywhere also work for a free
demo deployment — see the project report for tradeoffs (cold starts,
request limits, etc.).

## Optional: AI-generated diet plans

`backend/optional_ai_plan_generator.py` shows how to wire in an external
AI API (e.g. Anthropic's Claude) to generate richer diet/exercise text
instead of static templates. This is optional and requires an API key.

**Never commit an API key to this repository.** Set it as an
environment variable on whichever platform you deploy to:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Model performance

| Model | Accuracy |
|---|---|
| Random Forest | ~86.4% |
| Gradient Boosting | ~88.3% |
| Weighted Ensemble (0.55 / 0.45) | combines both for better generalization |

## License

MIT — see `LICENSE`.

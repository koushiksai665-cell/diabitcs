FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Train the model at build time so diabetes_ensemble.pkl is baked into the image.
# (Safe because train_model.py fetches the dataset over HTTPS at build time.)
RUN python train_model.py

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

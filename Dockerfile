FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn pandas

# Copy all project files (frontend and backend)
COPY . .

# Train the model at build time inside the backend directory
RUN cd backend && python train_model.py

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Start Flask via Gunicorn, binding to the dynamic $PORT (defaulting to 7860)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-7860} --chdir backend app:app"]

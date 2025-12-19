FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source code
COPY . .

# Expose port (Hugging Face Spaces uses port 7860 or 8000)
EXPOSE 8000

# Run the FastAPI application from the app.py entry point
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
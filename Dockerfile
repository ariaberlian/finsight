FROM python:3.12-slim

WORKDIR /app

# Install uv for faster dependency installation
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system -e .

# Copy application code
COPY . .

# Expose Gradio default port
EXPOSE 7860

# Run the application
CMD ["python", "main.py"]

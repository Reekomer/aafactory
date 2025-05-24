FROM python:3.13-slim

# Install OS-level dependencies needed for building Python extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    g++ \
    cmake \
    cython3 \
    libsndfile1 \
    libsndfile1-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

EXPOSE 7860

# Run your app
CMD ["python", "aafactory/src/aafactory/create_gradio_ui.py"]

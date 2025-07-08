# === Build Stage ===
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set working directory
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install dependencies into /install
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# === Final Stage ===
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /install /usr/local

# Copy app source
COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

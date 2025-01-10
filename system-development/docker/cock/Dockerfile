FROM nvidia/cuda:11.8.0-base-ubuntu22.04

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and minimal dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-minimal \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip

RUN mkdir -p /app/src /app/data

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

# Create minimal directory structure

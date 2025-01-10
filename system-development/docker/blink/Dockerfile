FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV TZ=Asia/Tokyo
ENV LANG=ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    python3.12 \
    python3.12-dev \
    python3-pip \
    wget \
    git \
    libopencv-dev \
    tzdata \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links and set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    ln -s /usr/bin/python3.12 /usr/bin/python && \
    ln -s /usr/bin/python3.12 /usr/bin/python3

WORKDIR /workspace

COPY requirements.txt .

# Optimize pip installation process
RUN pip install --no-cache-dir --upgrade pip==24.0.0 setuptools==69.0.3 wheel==0.42.0 && \
    # Pre-install core scientific packages
    pip install --no-cache-dir \
        numpy==2.0.0 \
        pandas==3.0.0 \
        scipy==1.13.0 \
        pyarrow==15.0.0 && \
    # Install PyTorch ecosystem
    pip install --no-cache-dir \
        torch==2.5.0 \
        torchvision==0.20.0 \
        torchaudio==2.5.0 \
        --index-url https://download.pytorch.org/whl/cu121 && \
    # Install remaining requirements
    pip install --no-cache-dir -r requirements.txt && \
    # Clean up
    rm -rf ~/.cache/pip

# Verify critical installations
RUN python -c "import torch; print(f'PyTorch version: {torch.__version__}, CUDA available: {torch.cuda.is_available()}')" && \
    python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"

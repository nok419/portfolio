FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV TZ=Asia/Tokyo
ENV LANG=ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    wget \
    git \
    libopencv-dev \
    tzdata \
    build-essential \
    curl \
    vim \
    htop \
    nvidia-smi \
    fonts-ipafont \
    fonts-ipaexfont \
    ninja-build \
    cmake \
    libaio-dev \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    ln -s /usr/bin/python3.10 /usr/bin/python3 && \
    ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip==23.1.2 setuptools==67.8.0 wheel==0.40.0 && \
    pip install --no-cache-dir torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118 && \
    pip install --no-cache-dir numpy==1.24.3 pandas==2.0.3 && \
    pip install --no-cache-dir -r requirements.txt && \
    python -c "import torch; print(f'PyTorch CUDA Available: {torch.cuda.is_available()}')"

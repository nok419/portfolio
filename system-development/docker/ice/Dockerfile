FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV TZ=Asia/Tokyo
ENV LANG=ja_JP.UTF-8
ENV PYTHONUNBUFFERED=1

# Essential system packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    build-essential \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python aliases
RUN ln -s /usr/bin/python3.10 /usr/bin/python3 && \
    ln -s /usr/bin/python3 /usr/bin/python

# Create necessary directories
RUN mkdir -p /workspace/notebooks /workspace/data /workspace/src
WORKDIR /workspace

COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118 && \
    pip install --no-cache-dir -r requirements.txt

# Configure Jupyter
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py


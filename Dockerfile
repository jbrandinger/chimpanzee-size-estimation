FROM nvidia/cuda:11.0-cudnn8-devel-ubuntu18.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    unzip \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install numpy pandas matplotlib tensorflow torch torchvision

# Clone Meta's Segment-Anything repository
RUN git clone https://github.com/metaai/segment-anything.git

# Set working directory
WORKDIR /segment-anything

# Install additional dependencies
RUN pip3 install -r requirements.txt

# Expose any necessary ports
EXPOSE 8888

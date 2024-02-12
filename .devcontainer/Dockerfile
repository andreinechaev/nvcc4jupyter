FROM ubuntu:22.04

ARG VENV_PATH=/opt/dev-venv
ENV VENV_ACTIVATE=${VENV_PATH}/bin/activate
ENV DEBIAN_FRONTEND="noninteractive"

# install the latest CUDA toolkit (https://developer.nvidia.com/cuda-downloads)
RUN apt update
RUN apt install -y wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt update
RUN apt -y install cuda-toolkit-12-3
RUN echo "PATH=\"\$PATH:/usr/local/cuda/bin\"" >> ~/.bashrc

# install OpenCV to test compilation with external libraries
RUN apt install -y libopencv-dev pkg-config

# make & language-pack-en are for documentation
RUN apt install -y \
    gcc \
    git \
    language-pack-en \
    make \
    python3.10-venv \
    vim

# we create the virtualenv here so that the devcontainer.json setting
# python.defaultInterpreterPath can be used to find it; if we do it in the
# post_create.sh script, the virtualenv will not be loaded and features like
# pylance, black, isort, etc. will not work
RUN python3.10 -m venv ${VENV_PATH}
RUN echo "source ${VENV_ACTIVATE}" >> ~/.bashrc

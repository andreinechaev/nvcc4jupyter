FROM nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04

ARG VENV_PATH=/opt/dev-venv
ENV VENV_ACTIVATE=${VENV_PATH}/bin/activate
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt update
RUN apt install -y \
    gcc \
    git \
    language-pack-en \
    libopencv-dev \
    make \
    pkg-config \
    python3.10-venv \
    vim

# we create the virtualenv here so that the devcontainer.json setting
# python.defaultInterpreterPath can be used to find it; if we do it in the
# post_create.sh script, the virtualenv will not be loaded and features like
# pylance, black, isort, etc. will not work
RUN python3.10 -m venv ${VENV_PATH}
RUN echo "source ${VENV_ACTIVATE}" >> ~/.bashrc

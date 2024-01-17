FROM mambaorg/micromamba:1.5.3-jammy-cuda-12.1.1
USER root
WORKDIR /app

#create the environment for the run
COPY environment.yml .

RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
# Put env activation into bashrc for running in shell
RUN echo "micromamba activate base" >> ~/.bashrc
ENV PATH /opt/micromamba/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH

RUN apt-get update && apt-get install vim libglib2.0-0 -y
ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV PYTHONPATH "${PYTHONPATH}:/app/code_package"

COPY code_package ./code_package

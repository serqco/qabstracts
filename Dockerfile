FROM rocker/verse:4.4.2

# Install Python and create a virtual environment to install the dependencies in
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt
RUN rm requirements.txt
ENV PATH="/opt/venv/bin:$PATH"

# Install reticulate to connect R to Python and tell it where to find the environment
RUN install2.r reticulate
ENV RETICULATE_PYTHON=/opt/venv/bin/python

# Install kableExtra (R package)
RUN install2.r kableExtra

# Install LaTeX (parts of it are already in the base image, but just to be sure we have everything)
RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-xetex texlive-fonts-recommended latexmk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

FROM public.ecr.aws/lambda/python:3.9
LABEL org.opencontainers.image.title="scraper_image"

# System dependencies for Chrome
RUN yum -y update && \
    yum install -y wget unzip atk libX11-xcb libXcomposite libXcursor libXdamage \
    libXext libXi libXtst cups-libs libXScrnSaver libXrandr pango at-spi2-atk \
    alsa-lib gtk3 && \
    yum clean all

# Add chrome and chromedriver to PATH so selenium can find them automatically
ENV PATH="/var/task/src/chrome-linux64:/var/task/src/chromedriver-linux64:${PATH}"

# Install requirements in a separate layer for caching
COPY ./src/requirements.txt src/
RUN pip install -r src/requirements.txt

COPY ./src src/
WORKDIR src

ENTRYPOINT ["python", "index.py"]
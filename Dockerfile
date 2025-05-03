FROM ubuntu:22.04

WORKDIR /usr/src/app
RUN chmod 755 /usr/src/app

# Install dependencies and MEGAcmd
RUN apt-get update && \
    apt-get install -y curl lsb-release python3 python3-pip libc6 libcrypto++8 libpcrecpp0v5 libmediainfo0v5 zlib1g && \
    curl -O https://mega.nz/linux/repo/xUbuntu_jammy/amd64/megacmd-xUbuntu_jammy_amd64.deb && \
    apt-get install -y ./megacmd-xUbuntu_jammy_amd64.deb && \
    rm ./megacmd-xUbuntu_jammy_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade setuptools wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure start.sh is executable
RUN chmod +x start.sh

CMD ["bash", "start.sh"]
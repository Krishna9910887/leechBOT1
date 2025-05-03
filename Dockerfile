FROM mysterysd/wzmlx:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# Update package lists and install megacmd
RUN apt-get update && \
    apt-get remove -y megacmd && \
    apt-get install -y curl && \
    curl -O https://mega.nz/linux/repo/xUbuntu_22.04/amd64/megacmd-xUbuntu_22.04_amd64.deb && \
    apt-get install -y ./megacmd-xUbuntu_22.04_amd64.deb && \
    apt-get clean
    
# Update package lists, remove existing megacmd, install curl, and install the correct megacmd version
#RUN apt-get update && \
   # apt-get remove -y megacmd && \
   # apt-get install -y curl lsb-release && \
   # UBUNTU_VERSION=$(lsb_release -cs) && \
   # curl -O https://mega.nz/linux/repo/xUbuntu_${UBUNTU_VERSION}/amd64/megacmd-xUbuntu_${UBUNTU_VERSION}_amd64.deb && \
   # apt-get install -y ./megacmd-xUbuntu_${UBUNTU_VERSION}_amd64.deb && \
   # rm ./megacmd-xUbuntu_${UBUNTU_VERSION}_amd64.deb && \
   # apt-get clean

COPY requirements.txt .
RUN pip3 install --upgrade setuptools wheel
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]


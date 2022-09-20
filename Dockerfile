#FROM  amazonlinux:latest
FROM amd64/amazonlinux:latest

RUN mkdir /tmp/workbench
WORKDIR /tmp/workbench/

# Python
# https://tecadmin.net/install-python-3-9-on-amazon-linux/
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compile-software.html
RUN yum groupinstall "Development Tools" -y
RUN yum install gcc openssl-devel bzip2-devel libffi-devel wget tar gzip -y
RUN yum install rust cargo -y
RUN wget https://www.python.org/ftp/python/3.9.14/Python-3.9.14.tgz
RUN tar xfvz Python-3.9.14.tgz
RUN cd Python-3.9.14 && ./configure --enable-optimizations
RUN cd Python-3.9.14 && make altinstall


# Node.js
# https://github.com/nvm-sh/nvm
RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.profile
RUN echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.profile
ENV ENV="~/.profile"
RUN source ~/.profile
RUN . ~/.nvm/nvm.sh && nvm install 14
RUN . ~/.nvm/nvm.sh && nvm use 14

# Packaging step

RUN python3.9 -m venv venv
RUN source ./venv/bin/activate && pip install --upgrade pip

COPY env /tmp/workbench/env/
COPY src /tmp/workbench/src/
COPY package.json /tmp/workbench/
COPY package-lock.json /tmp/workbench/
COPY serverless.yml /tmp/workbench/
COPY requirements.txt /tmp/workbench/
COPY env/set_env.sh /tmp/workbench/

RUN . ~/.nvm/nvm.sh && npm install
RUN source ./venv/bin/activate && pip install -r ./requirements.txt
RUN . ~/.nvm/nvm.sh && source ./venv/bin/activate && npx serverless package

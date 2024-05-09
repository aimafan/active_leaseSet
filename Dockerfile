FROM debian:bullseye

# 设置工作目录
WORKDIR /app

# 安装基本工具和依赖
RUN apt-get update && apt-get install -y \
    vim \
    sudo \
    python3.9 \
    python3-pip \
    python3.9-venv \
    net-tools \
    wget    \
    curl    

# 将vim设为默认编辑器
RUN update-alternatives --set editor /usr/bin/vim.basic

ADD . .
# 取消网卡合并包，需要在启动容器之后跑
RUN pip3 install --no-cache-dir -r requirements.txt


# 默认命令，打开vim
CMD ["bash"]
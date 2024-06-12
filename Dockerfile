# 二开推荐阅读[如何提高项目构建效率](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/scene/build/speed.html)
# 选择基础镜像。如需更换，请到[dockerhub官方仓库](https://hub.docker.com/_/python?tab=tags)自行选择后替换。
# 已知alpine镜像与pytorch有兼容性问题会导致构建失败，如需使用pytorch请务必按需更换基础镜像。
#FROM tiangolo/uvicorn-gunicorn:python3.10
#FROM python:3.9.12-alpine3.14
FROM python:3.10-slim
#FROM alpine:3.14

# 容器默认时区为UTC，如需使用上海时间请启用以下时区设置命令
# RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone

#RUN apk add ca-certificates

#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
#&& apk add --update --no-cache python3 py3-pip \
#&& rm -rf /var/cache/apk/*

RUN apt-get install ca-certificates

# 拷贝当前项目到/app目录下（.dockerignore中文件除外）
COPY . /app

# 设定当前的工作目录
WORKDIR /app


# 安装依赖到指定的/install文件夹
# 选用国内镜像源以提高下载速度
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
&& pip config set global.trusted-host mirrors.cloud.tencent.com \
&& pip install --upgrade pip \
# pip install scipy 等数学包失败，可使用 apk add py3-scipy 进行， 参考安装 https://pkgs.alpinelinux.org/packages?name=py3-scipy&branch=v3.13
&& pip install -r requirements.txt --no-warn-script-location

# 验证版本
RUN python3 -V

# 此处端口必须与「服务设置」-「流水线」以及「手动上传代码包」部署时填写的端口一致，否则会部署失败。
EXPOSE 8088

# 执行启动命令
CMD ["python3", "run.py"]
#CMD ["python3", "-m", "uvicorn", "run:app", "--host", "0.0.0.0", "--port ", "80"]


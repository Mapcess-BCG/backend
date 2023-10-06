# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# RUN mkdir -p /home/.aws && \
#     echo "[default]" > /home/.aws/credentials && \
#     echo "aws_access_key_id = AKIAUOE65TFG6UZKDCWO" >> /home/.aws/credentials  && \
#     echo "aws_secret_access_key = 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" >> /home/.aws/credentials

# RUN mkdir -p /home/app/.aws && \
#     echo "[default]" > /home/app/.aws/credentials && \
#     echo "aws_access_key_id = AKIAUOE65TFG6UZKDCWO" >> /home/app/.aws/credentials  && \
#     echo "aws_secret_access_key = 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" >> /home/app/.aws/credentials

COPY . .

CMD ["python3", "server.py"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

ENV AWS_ACCESS_KEY_ID=AKIAUOE65TFG6UZKDCWO
ENV AWS_SECRET_ACCESS_KEY=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

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

CMD ["python3", "server.py"]

#!/usr/bin/env bash
# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# выполняем команды из Makefile
make install && make tailwind_build && make collectstatic && make migrate
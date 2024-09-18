#!/bin/bash

cd /volume
celery -A videocaption worker --loglevel=info


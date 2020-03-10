#!/bin/bash

set -eux

git add -A

git commit -m "New commit!"

git push origin master

gcloud functions deploy function-1

#!/bin/bash

find -name '*.pyc' | xargs rm -vf
find -name '.*.swp' | xargs rm -vf

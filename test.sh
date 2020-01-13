#!/bin/sh

make bandit
make test-unit
make test-integration
make validate

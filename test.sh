#!/bin/bash
./manage.py test --settings=test_settings
flake8 . --exclude migrations

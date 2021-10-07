find . | grep '\.py$' | grep -v "tests/" | xargs pylint

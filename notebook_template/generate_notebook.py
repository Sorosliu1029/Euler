#!/usr/bin/python3
"""
generate jupyter notebook for Project Euler
"""
import json
import sys
from urllib.request import urlopen
import re
import os

template = {
    "nbformat": 4,
    "nbformat_minor": 2,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "authors": [{"name": "Soros Liu"}],
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "{}.{}.{}".format(*sys.version_info[:3])
        }
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [ "TODO" ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [ "TODO" ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [ "---" ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [ "### Idea" ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [ "What's your idea?" ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [ "---" ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def solve():\n",
                "    pass"
            ]
        }
    ]
}

def get_html_content(problem_id):
    assert problem_id > 0
    with urlopen("https://projecteuler.net/problem={}".format(problem_id)) as f:
        html_content = f.read().decode('utf-8')
        problem_header_match = re.search(r"<h2>(.*?)</h2>", html_content)
        problem_content_match = re.search(r'<div class=\"problem_content\" role=\"problem\">(.*?)</div>', html_content, flags=re.DOTALL)
        return problem_header_match.group(1), problem_content_match.group(1).strip()

if __name__ == "__main__":
    argvs = sys.argv[1:]
    if not argvs:
        print("Please provide problem id.")
        sys.exit(0)

    problem_id = int(argvs[0])
    
    header, content = get_html_content(problem_id)
    assert header != ""
    assert content != ""
    template["cells"][0]["source"] = ["# "+header]
    template["cells"][1]["source"] = [content]

    interval_start = (problem_id-1) // 25 * 25 + 1
    directory = "{}-{}".format(interval_start, interval_start+24)
    if not os.path.exists(directory):
        os.mkdir(directory)

    with open(os.path.join(directory, 'p{}.ipynb'.format(problem_id)), 'w+') as f:
        json.dump(template, f, indent=2)

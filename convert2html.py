#!/usr/bin/python3
"""
Convert .ipynb to .html by nbconvert
"""
import os
from nbconvert import HTMLExporter
import re
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from collections import Counter

PROBLEM_JSON = os.path.join('docs', 'problems.json')
TEMPLATE_PATH = os.path.join('docs', 'templates')
INDEX_HTML_PATH = os.path.join('docs', 'index.html')

class Converter(object):
    def __init__(self):
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_path = [os.path.join('docs', 'templates')]
        self.html_exporter.template_file = 'full'

    def convert(self, ipynb_path):   
        return self.html_exporter.from_filename(ipynb_path)

    def write(self, source_ipynb_path):
        assert os.path.exists(source_ipynb_path)
        body, resources = self.convert(source_ipynb_path)
        name = resources['metadata']['name']
        problem_id = int(re.search(r'p(\d+)', name).group(1))

        interval_start = (problem_id-1) // 100 * 100 + 1
        directory = os.path.join('docs', '{}-{}'.format(interval_start, interval_start+99))
        if not os.path.exists(directory):
            os.mkdir(directory)
        with open(os.path.join(directory, 'p{}.html'.format(problem_id)), 'wt', encoding='utf-8') as f:
            f.write(body)
        # print('{} write success'.format(os.path.join(directory, 'p{}.html'.format(problem_id))))
        return problem_id

def convert_all():
    converter = Converter()
    
    solved_problems = dict()
    for dirpath, dirnames, filenames in os.walk('.'):
        if re.match(r'^\.\\(\d+)-(\d+)$', dirpath):
            for filename in filenames:
                source_ipynb_path = os.path.join(dirpath, filename)
                problem_id = converter.write(source_ipynb_path)
                modified_datetime = datetime.fromtimestamp(os.path.getmtime(source_ipynb_path)).strftime('%a, %d %b %Y, %H:%M')
                solved_problems[problem_id] = modified_datetime
    return solved_problems

def change_problem_json(solved_problems):
    with open(PROBLEM_JSON, 'rt', encoding='utf-8') as f:
        problems = json.load(f)
    
    for p in problems:
        if p['id'] in solved_problems:
            p['completed_on'] = solved_problems[p['id']]
        else:
            p['completed_on'] = None
    
    with open(PROBLEM_JSON, 'wt', encoding='utf-8') as f:
        json.dump(problems, f, indent=2)

    return solved_problems, problems

def render_index(solved_problems, problems):
    solved_count = len(solved_problems)
    highest_level = solved_count // 25
    total_difficulty_counter = Counter((p['difficulty'] for p in problems))
    solved_difficulty_counter = Counter((problems[idx-1]['difficulty'] for idx in solved_problems.keys()))

    data = {
        'highest_level': highest_level,
        'solved_count': solved_count,
        'total_count': len(problems),
        'progress_percentage': '{}'.format(solved_count * 100 // len(problems)),
        'solved': set(solved_problems.keys()),
        'problems': problems,
        'total_difficulty_counter': total_difficulty_counter,
        'solved_difficulty_counter': solved_difficulty_counter,
        'total_mean_difficulty': '{:.2f}'.format(sum((k * v for k, v in total_difficulty_counter.items() if k)) / len(problems)),
        'solved_mean_difficulty': '{:.2f}'.format(sum((k * v for k, v in solved_difficulty_counter.items() if k)) / solved_count),
        'solved_max_difficulty': max(filter(None, solved_difficulty_counter.keys()))
    }

    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    readme_template = env.get_template('index.html.j2')
    readme_template.stream(**data).dump(INDEX_HTML_PATH)

def convert_and_render():
    solved_problems = convert_all()
    print('Convert done.')
    solved_problems, problems = change_problem_json(solved_problems)
    print('problems.json changed.')
    render_index(solved_problems, problems)
    print('index.html rendered.')

def main():
    converter = Converter()
    converter.write('./1-25/p1.ipynb')

if __name__ == '__main__':
    main()
    # with open(PROBLEM_JSON, 'rt', encoding='utf-8') as f:
    #     problems = json.load(f)
    # render_index(problems=problems)
    # convert_and_render()
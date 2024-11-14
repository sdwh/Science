from flask import Flask, render_template, render_template_string
import markdown
from jinja2 import Environment, FileSystemLoader
import htmlmin
from dbcontext import fetch_common_questions

app = Flask(__name__)

# 設置 Jinja2 環境
env = Environment(loader=FileSystemLoader('templates'))

@app.route('/')
def index():
    questions = [(idx + 1, row[0]) for idx, row in enumerate(results)]
    return render_template('index.jinja', questions=questions)

@app.route('/<int:id>')
def question(id):
    if id < 1 or id > len(results):
        return "Question not found", 404

    row = results[id - 1]
    template = env.get_template('page.jinja')
    html_content = markdown.markdown(row[1])

    rendered_content = template.render(
        title = f"{id} - {row[0]}",
        content=f'<p>{html_content}</p>',
        prev=max(id - 1, 1),
        next=min(id + 1, len(results))
    )

    minified_content = htmlmin.minify(rendered_content, remove_empty_space=True)
    return render_template_string(minified_content)

if __name__ == '__main__':
    results = fetch_common_questions()
    app.run(debug=True)
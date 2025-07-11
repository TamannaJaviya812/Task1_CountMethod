from flask import Flask, request, render_template_string
import os
import re

app = Flask(__name__)

def is_title(line):
    words = line.strip().split()
    return all(word.istitle() for word in words) and len(words) > 0

def count_document_metrics(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    num_paragraphs = len(paragraphs)

    words = re.findall(r'\b\w+\b', text)
    num_words = len(words)

    sentences = re.findall(r'[.!?]+', text)
    num_sentences = len(sentences)

    lines = text.split('\n')
    title_count = sum(1 for line in lines if is_title(line))

    file_size_kb = os.path.getsize(file_path) / 1024

    return num_paragraphs, num_words, num_sentences, title_count, file_size_kb


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filepath = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(filepath)

        para, words, sents, titles, size = count_document_metrics(filepath)

        return render_template_string('''
            <h2>📄 Document Analysis Result</h2>
            <ul>
              <li><strong>Paragraphs:</strong> {{ para }}</li>
              <li><strong>Words:</strong> {{ words }}</li>
              <li><strong>Sentences:</strong> {{ sents }}</li>
              <li><strong>Titles:</strong> {{ titles }}</li>
              <li><strong>File size:</strong> {{ size | round(2) }} KB</li>
            </ul>
            <a href="/">🔁 Analyze another file</a>
        ''', para=para, words=words, sents=sents, titles=titles, size=size)

    return '''
    <h1>📂 Upload .txt file for Analysis</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".txt" required>
        <button type="submit">Analyze</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)

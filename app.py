from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

vocabulary_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vocabulary', methods=['GET', 'POST'])
def vocabulary():
    if request.method == 'POST':
        words_string = request.form.get('words', '')
        if words_string:
            new_words = words_string.strip().split()
            for word in new_words:
                if word not in vocabulary_list: # Avoid duplicates
                    vocabulary_list.append(word)
        return redirect(url_for('vocabulary'))
    return render_template('vocabulary.html', words=vocabulary_list)

@app.route('/reading')
def reading():
    return render_template('reading.html')

@app.route('/classical')
def classical():
    return render_template('classical.html')

if __name__ == '__main__':
    app.run(debug=True)

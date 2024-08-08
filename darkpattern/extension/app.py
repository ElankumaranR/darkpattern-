from flask import Flask, jsonify, request
from flask_cors import CORS
from joblib import load
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')


presence_classifier = load('presence_classifer.joblib')
presence_vect = load('presence_vectorizer.joblib')

def extract_tokens_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    sentences = []
    for string in soup.stripped_strings:
        sentences.extend(nltk.sent_tokenize(string))
    return sentences



app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def main():
    if request.method == 'POST':
        try:
            data = request.json      
            html_content = data.get('htmlcontent')
            tokens = extract_tokens_from_html(html_content)
            dark = {}
            text=[]
            for token in tokens:
                result = presence_classifier.predict(presence_vect.transform([token]))
                if result!='Not Dark':
                    text.append(token)
                    dark[token] = result[0] 
            message = {'result': dark}
            print(message)
            return jsonify(message)
        except Exception as e:
            print("error")
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(threaded=True, debug=True)

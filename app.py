from flask import Flask, request, jsonify
from flask import render_template
import knowledgeExtraction
import build_model

model = build_model.FakeNewClassifier("/Users/vietnguyen/Workspace/Codes/Python/Knowledge-Graph-Intro/my_dataset/embeddings/TransE")
app = Flask(__name__, static_folder="static")
kgExtracter = knowledgeExtraction.KnowledgeExtraction()
@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        inputText = request.form.get('inputText')
        score = model.detect_fake_new(inputText)
        triples = kgExtracter.extract_triple_by_openIO(inputText)
        if len(triples) > 0:
            triple = triples[0]
            inputText = inputText.replace(triple[0], '<span class="style-ent">{}</span>'.format(triple[0]))
            inputText = inputText.replace(triple[1], '<span class="style-rel">{}</span>'.format(triple[1]))
            inputText = inputText.replace(triple[2], '<span class="style-obj">{}</span>'.format(triple[2]))
            if score > 0.5:
                return render_template("index.html", input_text=inputText, result="Trust", score=int(score*100))
            else:
                return render_template("index.html", input_text=inputText, result="Fake", score=int((1-score)*100))
        return render_template("index.html", input_text=inputText, result="Fake", score=int((1-score)*100))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
from confluence_qa import DiagnosisLLM

app = Flask(__name__)
CORS(app)

# def load_confluence():
#     cqa = ConfluenceQA()
#     cqa.init_embeddings()
#     cqa.init_models()
#     cqa.vector_db_confluence_docs()
#     cqa.retrieval_qa_chain()
#     return cqa
#
# confluence_qa = load_confluence()


@app.route('/query', methods=['POST'])
def query_agent():
    data = request.json
    response = confluence_qa.answer_confluence(data["query"])
    return jsonify({"response": response})

@app.route('/')
def index():
    return 'Index Page'

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    cqa = DiagnosisLLM()
    cqa.init_models()
    cqa.try_ask("What's the weather like today? Give me a link to the weather forecast.")

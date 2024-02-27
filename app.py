from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    #Lógica para ler os valores do formulário html inseridos (texto e a lingua)
    original_text = request.form['text']
    target_language = request.form['language']

    #Ler os dados do .env
    key = os.environ['KEY']
    endpoint= os.environ['ENDPOINT']
    location= os.environ['LOCATION']

    path = '/translate?api-version=3.0'  #indica a tradução e a versão da API
    target_language_parameter = '&to=' + target_language #adiciona o parâmetro da lingua
    constructed_url = endpoint + path + target_language_parameter #CRIAR O URL

    headers = { #informação do header, inclui a chave de inscrição
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{ 'text': original_text }]

    #faz a requisição usando POST
    translator_request = requests.post(constructed_url, headers=headers, json=body)

    #recupera a resposta JSON
    translator_response = translator_request.json()

    #pega a tradução
    translated_text = translator_response[0]['translations'][0]['text']
    
    #chama o render template, pas sa o texto traduzido, o texto original e a lingua
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )
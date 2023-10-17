import sched
import time
import requests
from flask import Flask, render_template
import datetime
from datetime import datetime, timedelta

app = Flask(__name__)

chave_api_nasa = 'xioK8s8govXyjsMco4THtn6ME1nL53miaVVMxMgD'


def get_astronomy_data():
    url = f'https://api.nasa.gov/planetary/apod?api_key={chave_api_nasa}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        explanation = data['explanation']
        date = data['date']
        image_url = data['url']
        return explanation, date, image_url
    else:
        return "Não foi possível obter a explicação.", "Data indisponível.", ""


# buscar e atualizar os dados astronômicos do dia
def update_astronomy_data(sc):
    # você chama outra função chamada get_astronomy_data() para buscar os dados astronômicos mais recentes do dia.
    explanation, date, image_url = get_astronomy_data()


    app.config['current_explanation'] = explanation
    app.config['current_date'] = date
    app.config['current_image_url'] = image_url

    schedule.enter(86400, 1, update_astronomy_data, (sc,))


# Você cria um objeto sched.scheduler chamado s, que é usado para agendar tarefas.
schedule = sched.scheduler(time.time, time.sleep)

update_astronomy_data(schedule)


@app.route('/')
def astronomy_picture_daily():
    current_explanation = app.config.get('current_explanation', "Não foi possível obter a explicação.")
    current_date = app.config.get('current_date', "Data indisponível.")
    current_image_url = app.config.get('current_image_url', "")

    # Calculate previous and next dates based on the current date
    current_date_obj = datetime.strptime(current_date, '%Y-%m-%d')
    previous_date = (current_date_obj - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (current_date_obj + timedelta(days=1)).strftime('%Y-%m-%d')

    return render_template('index.html', explanation=current_explanation, date=current_date,
                           image_url=current_image_url,
                           previous_date=previous_date, next_date=next_date)


def get_astronomy_data_for_date(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y-%m-%d')
    except ValueError:
        # Return None for date when it's not available
        return "Não foi possível obter a explicação.", None, ""

    url = f'https://api.nasa.gov/planetary/apod?api_key={chave_api_nasa}&date={formatted_date}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        explanation = data['explanation']
        image_url = data['url']
        return explanation, date, image_url
    else:
        # Return None for date when it's not available
        return "Não foi possível obter a explicação.", None, ""


@app.route('/image/<date>')
def astronomy_picture_by_date(date):
    explanation, date, image_url = get_astronomy_data_for_date(date)

    selected_date_obj = datetime.strptime(date, '%Y-%m-%d')
    previous_date = (selected_date_obj - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (selected_date_obj + timedelta(days=1)).strftime('%Y-%m-%d')

    return render_template('index.html', explanation=explanation, date=date, image_url=image_url,
                           previous_date=previous_date, next_date=next_date)

if __name__ == '__main__':
    app.run()

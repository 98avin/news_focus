from flask import Flask, render_template
from application import db
from application.build_dict import build_dict
from application.models import Data

application = Flask(__name__)
application.debug=True
#application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

@application.route('/', methods=['GET', 'POST'])
@application.route('/hello', methods=['GET', 'POST'])
def hello():
    return render_template('index.html', dict = build_dict())

if __name__ == '__main__':
    application.run(host='0.0.0.0')


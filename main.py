from website import create_app
from website import db
from website import models

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) #host='0.0.0.0'

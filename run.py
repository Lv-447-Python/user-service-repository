from user_service import app

@app.route('/')
def index():
    return "heeey"


if __name__ == '__main__':
    app.run()

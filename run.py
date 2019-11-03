from user_service import app
from user_service.views.authentication import ProfileResource

if __name__ == '__main__':
    app.run(debug=True)

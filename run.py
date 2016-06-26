from app import app
import os
app.secret_key = 'PWN3D'


if __name__ == '__main__':
    PORT = os.environ.get('PORT', 80)
    app.run(port=int(PORT),  host='0.0.0.0', debug=True)

from app import app
import os
app.secret_key = 'PWN3D'
if __name__ == '__main__':
    PORT = os.environ.get('PORT', 5000)
    app.run(port=int(PORT), debug=True)

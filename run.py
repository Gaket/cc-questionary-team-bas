from app import app
import os
app.secret_key = 'PWN3D'
PORT = os.environ.get('PORT', 5000)

app.run(host="0.0.0.0", port=int(PORT), debug=True)

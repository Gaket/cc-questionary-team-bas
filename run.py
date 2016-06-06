from app import app
import os
app.secret_key = 'PWN3D'
if "PORT" in os.environ:
    port = os.environ["PORT"]
else:
    port = 5000
app.run(port=port, debug=True)

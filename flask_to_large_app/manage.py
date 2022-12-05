from app import create_app
from flask import Flask

a = create_app()



a.run(debug=True)
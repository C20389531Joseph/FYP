# Author: Joseph Egan    Complier: VSCode   Last updated:15/04/2025
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

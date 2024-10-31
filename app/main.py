import sys
import os

# Add the root project directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


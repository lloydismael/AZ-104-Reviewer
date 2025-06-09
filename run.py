import os
import sys

# Add the app directory to Python path for imports
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.insert(0, app_dir)

# Import the Flask app
from app import app

if __name__ == '__main__':
    # Get host and port from environment variables if set
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # Set debug mode based on environment
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Run the app
    app.run(host=host, port=port, debug=debug)

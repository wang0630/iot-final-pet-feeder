import threading
from app import create_app
from hx711py.driver import hx

if __name__ == '__main__':
    app = create_app()
    # Create thread for weight sensor
    hx_thread = threading.Thread(target=hx.run_hx711, daemon=True)
    hx_thread.start()
    # Explicitly state host = 0.0.0.0 to prevent network error
    app.run(host='0.0.0.0', port=5000, debug=True)

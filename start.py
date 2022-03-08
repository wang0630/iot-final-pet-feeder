from app import create_app

if __name__ == '__main__':
    app = create_app()
    # Explicitly state host = 0.0.0.0 to prevent network error
    app.run(host='0.0.0.0', port=5000, debug=True)

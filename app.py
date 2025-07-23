if __name__ == "__main__":
    from routes import *
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000, host='0.0.0.0')
    
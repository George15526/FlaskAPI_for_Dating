from user import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            port=8000, 
            ssl_context=('server.crt', 'server.key'), 
            debug=True
            )
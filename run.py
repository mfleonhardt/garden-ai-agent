from garden_ai_agent import create_app
from garden_ai_agent.config import PORT

app = create_app()

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from EKS via Jenkins CI/CD 🚀"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
print("🚀 Starting run.py...")

from app import create_app

print("📦 Import done. Creating app...")

app = create_app()

if __name__ == '__main__':
    print("✅ App is running!")
    app.run(debug=True)

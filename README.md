# Portfolio Backend & Admin Panel

## Setup

1. Create a free MongoDB Atlas cluster and get your connection string.
2. Set environment variables:
   - `MONGODB_URI`: your MongoDB connection string
   - `JWT_SECRET`: any random secret phrase
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn main:app --reload`
5. Open `http://localhost:8000/admin/login.html` to access admin panel.

## Deploy to Render.com
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Add env variables as above.

## Admin Credentials
- Username: `admin`
- Password: `admin123` (change in `auth.py`)

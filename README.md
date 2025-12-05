**1. Clone and Navigate**:
```bash
cd /path/to/SoluGenAI
```

**2. Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure Environment**:
```bash
cp .env.example .env
# rename the file to .env and add: OPENAI_API_KEY=sk-your-key-here
```

**4. Frontend Setup**:
```bash
cd ../frontend
npm install
```

**5. Process Dataset**:
```bash
cd ../backend
source venv/bin/activate
python process_dataset.py
```

**65. Ingest Dataset (Creates Vector Database)**:
```bash
cd ../backend
source venv/bin/activate
python ingest_reviews.py
```


### Running the Application

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn main:app
```
→ Backend runs at `http://localhost:8000`


**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```
→ Frontend runs at `http://localhost:5173`


**Run Tests**:
```bash
pytest -v


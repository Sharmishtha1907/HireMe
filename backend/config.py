import os
import dotenv

dotenv.load_dotenv()



MODEL="llama3.2"
llm_provider="ollama"
DB_URL = os.environ["DATABASE_URL"]
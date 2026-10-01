- Replace hardcoded 'localhost' with os.getenv('POSTGRES_HOST', 'localhost')
  in all 3 ETL scripts, so they work both outside and inside containers
- Add requirements.txt (pandas, sqlalchemy, python-dotenv, psycopg2-binary)
- Add Dockerfile (single image shared by bronze/silver/gold services)
- Add bronze/silver/gold services to docker-compose.yml with:
  - healthcheck on postgres (wait until DB actually accepts connections)
  - depends_on + condition: service_completed_successfully to chain
    bronze -> silver -> gold in correct order automatically
- Fix driver ambiguity: postgresql:// -> postgresql+psycopg2:// in all
  connection strings

Previously: had to manually run 3 scripts in order after starting
postgres via docker-compose. Now: 'docker-compose up --build' runs
the entire pipeline end-to-end automatically."

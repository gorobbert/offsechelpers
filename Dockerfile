# Gebruik een officiele python image met bekende recente versie
FROM python:3.9-slim

# Stel de directory in waar we onze app plaatsen
WORKDIR /app

# Link de sourcode vd app naar de container in de app workdir
# handig voor testen
ADD src /app

# Installeer de benodigde dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Zet port 8000 open (standaard van fastapi)
EXPOSE 8000

# Start de app en reload by gedetecteerde changes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

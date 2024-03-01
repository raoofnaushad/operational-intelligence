## Steps to Deploy Client

### Without Docker

1. Clone the repo
2. Build ReactApp: `npm run build`
3. Preview the application: `npm run serve`

### With Docker

1. Clone the repository
2. Build the dockerfile: `docker build -t farpointoi-client .`
3. Run the docker file: `docker run -d -p 5173:5173 farpointoi-client`
4. Open `http://localhost:5173`

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/oi.farpointhq.com/fullchain.pem
Key is saved at: /etc/letsencrypt/live/oi.farpointhq.com/privkey.pem

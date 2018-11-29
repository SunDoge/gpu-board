# GPU Monitor



## Usage

### Server

```
cd server
pip install -r requirements.txt
python main.py
```

### Client

Add server addresses to `src/config.js`

```
cd client
mv src/config.js.example src/config.js
yarn install
yarn serve
```
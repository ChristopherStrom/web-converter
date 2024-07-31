Build the React App:

```
npm run build
sudo cp -r build/* /var/www/html/
sudo systemctl restart nginx

```

Build Backend Flask app

```
sudo systemctl restart web-converter.service
```

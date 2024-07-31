Build the React App:

```
npm run build
Deploy the Build to Nginx:


sudo cp -r build/* /var/www/html/
sudo systemctl restart nginx

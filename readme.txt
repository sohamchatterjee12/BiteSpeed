To run the app perform the following steps:-

1. Open Docker for Desktop if on Windows else have Docker installed on Linux machines

2. Build image using command - docker build -t bitespeed_img .

3. Run image in container with port forwarding using command - docker run -p 5000:5000 bitespeed_img

4. Endpoint will be accessible at localhost:5000/identify(http://127.0.0.1:5000/identify)
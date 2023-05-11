docker stop -t 1 touch
docker build -t touch .
docker run -d -p 31337:31337 --rm --name touch touch
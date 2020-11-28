# web-crawler

## welcome to my web scrawler application!

### Explanation: 
* The crawller will search every 2 minutes for new pastes in https://pastebin.com.
* In case he found some he will update the db.

### Technolegis and libraries:
* Docker and docker-compose
* beautifulsoup4
* pymongo docker image
* requests
* arrow

### How to start:
* [Install Docker.](https://docs.docker.com/get-docker/)
* [Install Docker compose.](https://docs.docker.com/compose/install/)
* run docker-compose up in the terminal and wait till docker building all the images and running the containers.
* After you will get the message "sucessfully connected to mongo" in your terminal, you can query the images from your docker mongo container.
* To get all pastes from db while app is running:
1. docker exec -it mongodb bash
2. show dbs
3. use scrawler
4. db.pastes.find({}) - will give you all the pastes
* If you want to stop the app, press ^C in your docker-compose terminal. 




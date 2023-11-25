# Project Name: Web crawler
## Purpose of the project: 
###   To see how the search engine works
###   To see network graphs and connections between sites
###   Educational purposes
## Project description:
## the project has three parts:
###   1.	Crawler (main.py): this is the main program that crawls all links in websites and sends the connections to the database as a (source, target) format
###   main.py first uses all the links (main domains) from links.csv file and puts these websites as the main node to start the crawling process.
###   2.	Database: you need an SQL Database to create the table(“link”) that has two columns source and target to store connections between sites (ex: A --> B)
###   You need to update the db_config dictionary base on your database configuration in main.py and Visualization.ipynb
###   3.	Visualization (Visualization.ipynb): We use this Jupyter Notebook to connect to the database in real-time and see the crawling speed, how many links are crawled up that point and ###   draw a beautiful graph using the NetworkX library.
### Note: This project uses a multiprocessing pool and SQL pool connection. you can alter the pool size parameter based on your machine to get the best results.
### Alert: This project was for educational purposes only. Please respect the website crawling policies and their robots.txt file. Don’t use it illegally and respect each website's crawling policies. illegal use case may lead to blocking and other issues.



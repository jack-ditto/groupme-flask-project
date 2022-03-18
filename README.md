# GroupMe Flask Project

## Technologies
#### Frontend: HTML/CSS, Bootstrap, JQuery
#### Backend: Python Flask

## What does it do? 
This is a pretty simple application that takes in a GroupMe API key and interacts with the GroupMe API to pull in groups and messsages. The frontend provides a visualization of this message data, providing charts for "Who talks the most?" and "Who gets the most likes per message?". Charts are created using Chart.js, and a type of caching system is implemented by saving local json files since it can take time to fetch all messages for a group that has existed for a long time. Obviously this is intended for local use since this compromises security / privacy. 

## Screenshots
<img width="1289" alt="image" src="https://user-images.githubusercontent.com/31874647/158958177-e38824fb-cfcd-4e7a-a19a-4ded7eb87f3e.png">
<img width="1310" alt="image" src="https://user-images.githubusercontent.com/31874647/158958451-eceedb29-b695-4753-8792-bfa353a18775.png">
<img width="1315" alt="image" src="https://user-images.githubusercontent.com/31874647/158958489-6baf05c3-6f6e-4e63-81c2-8a40d3956d90.png">
<img width="1308" alt="image" src="https://user-images.githubusercontent.com/31874647/158958658-d3b4017e-0558-4bb5-b433-04bfd60e589c.png">

## Notes and Improvements
Overall this is a simple application as it stand now. The framework is laid for producing various different meaningful metrics, and I hope to get around to improving the application in the future. 

If I were to write this again (or dare host a production version) I would certainly make changes. The Javascript is not structured well and I am sure if I were to go back with the experience I have now I could greatly improve the efficiency of making requests to the GroupMe API and parsing data.

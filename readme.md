# Videocaption
A web application that allows users to upload videos with subtitles and watch them with more interactivity.

## Key Features:
    1. Watch in multiple language subtitles.
    2. Skip to your favourite part by searching for dialogues.

## Tech Stack used: 
    django, postgres, redis, celery, react, docker


## How to run:
    1. Clone this repo in your linux local or macos local.
    2. `cd Videocation`
    3. `./devstart`
    4. Wait for all containers to start.
    5. Go to browser and open `http://localhost:8000`

## Website guide

### Upload file
    1. To upload file, click on upload button.
    2. Choose file from the give file input.
    3. When it shows "success", then return to history page by clicking on the history button.
    4. You will see your file there.

`Note: Can't upload two files at the same time. After uploading one go to history and then click on upload to upload the other.` 

### Interact with file
    1. Click on history button.
    2. Click on your file.
    3. Before playing the video, set the language from the dropdown.
    4. Click on video. It will start playing. Captions will show on the video in white and also below the video for better view.

### Change language

    1. From the dropdown, select your language. 

    `Subtitles will not immediately change. Once the speaker has spoken the displayed subtitle line, new subtitle line with your selected language will be loaded and then shown.`

### Get timestamp
    1. Search the subtitle that you want in the text field below the video.
    2. Click on search right next to it.
    3. Timestamp will show in blue. Timestamp is in seconds.

### Run the video from timestamp

    1. Click anywhere on the blue timestamp text shown.
    2. The video will start running from that timestamp immediately.






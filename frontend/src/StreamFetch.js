import { useDispatch } from "react-redux";

export default function StreamingFetch(url, setProgress) {

    return fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contentLength = +response.headers.get('Content-Length');
        let receivedLength = 0;
        const chunks = [];
  
        const reader = response.body.getReader();
  
        function pump() {
          return reader.read().then(({ done, value }) => {
            if (done) {
                if (setProgress) {
                    setProgress(Math.round((receivedLength / contentLength) * 100));
                  }
              const blob = new Blob(chunks);
              const objectUrl = URL.createObjectURL(blob);
              //setVideoObjectUrl(objectUrl);
              //console.log("video src is "+objectUrl);
              return objectUrl;
            }
  
            chunks.push(value);
            receivedLength += value.length;
  
  
            return pump();
          });
        }
  
        return pump();
      })
      .catch(error => {
        console.error('Download failed:', error);
      });
  }
  
  // Usage
  //streamingFetch(
  //  `http://127.0.0.1:8000/api/get_file_by_name/?name=${actual_name}`,
  //  setvideo_object_url,
  //  (progress) => console.log(`Download progress: ${progress}%`)
  //);
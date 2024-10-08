import React, { useCallback } from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import { useDispatch, useSelector } from 'react-redux';

export default function VideoJS(props){
  const videoRef = React.useRef(null);
  const playerRef = React.useRef(null);
  const {options} = props;
  const dispatch=useDispatch();
  const startTime=useSelector(state=>state.startTime);

  React.useEffect(()=>{
    console.log("player updated");
  })


  React.useEffect(() => {

    // Make sure Video.js player is only initialized once
    if (!playerRef.current) {
      // The Video.js player needs to be _inside_ the component el for React 18 Strict Mode. 
      const videoElement = document.createElement("video-js");

      videoElement.classList.add('vjs-big-play-centered');
      videoRef.current.appendChild(videoElement);

      const player = playerRef.current = videojs(videoElement, options, () => {
        videojs.log('player is ready');

        player.on('timeupdate',()=>{
          dispatch({
            type: "update timestamp",
            payload: player.currentTime()
          })
        })

      });

    // You could update an existing player in the `else` block here
    // on prop change, for example:
    } else {
      const player = playerRef.current;

      player.autoplay(options.autoplay);
      player.src(options.sources);
    }
  }, [options, videoRef,startTime]);

  // Dispose the Video.js player when the functional component unmounts
  React.useEffect(() => {
    const player = playerRef.current;

    return () => {
      if (player && !player.isDisposed()) {
        player.dispose();
        playerRef.current = null;
      }
      localStorage.removeItem('startTime');
    };
  }, [playerRef]);

  return (
    <div data-vjs-player style={{ display: 'flex', justifyContent: 'center' }}
    >
      <div id="videoid" ref={videoRef}  style={{
        width: '800px',
        height: '500px'
      }}> 
        </div>
    </div>
  );
}


import {useDispatch, useSelector } from "react-redux"
import VideoJS from "./VideoJs";
import Captions from "./Captions";
import StreamingFetch from "./StreamFetch";
import { useEffect } from "react";


export default function Operations(){
    const video_src = useSelector(state => state.video_src);
    const video_name=useSelector(state=>state.video_full_name);
    const short_name=video_name.split("/").pop()
    const dispatch=useDispatch();

    
    useEffect(()=>{StreamingFetch(
        `http://127.0.0.1:8000/api/get_file_by_name/?name=${short_name}`,
        (progress) => console.log(`Download progress: ${progress}%`)
        )
        .then((url)=>{
            dispatch({
                type: "set video url",
                payload: url
            })
        })
        
    },[video_name])


    return (
        <div style={{
            position: "relative",
        }}>
            {video_src!=""?
            <VideoJS
            options={{
                controls: true,
                sources:[{
                    src: video_src,
                    type: "video/"+video_name.split("/").pop().split(".").pop()
                }]
            }}
            style={
                {
                    position: "absolute"
                }
            } />:null}
           <Captions/>
        </div>
    )
}
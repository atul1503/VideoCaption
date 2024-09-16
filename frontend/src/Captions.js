import { useState,useRef,useEffect } from "react";
import { useSelector } from "react-redux";

export default function Captions(){

    const time=useSelector(state=>state.timestamp);
    const video_full_name=useSelector(state=>state.video_full_name);
    const short_name=video_full_name.split("/").pop();
    const [languages,setlanguages]=useState([]);
    const [caption,setcaption]=useState("");
    const languageref=useRef(null);
    const [startTime,setstartTime]=useState(-1);
    const [endTime,setEndTime]=useState(-1);


    useEffect(()=>{
        fetch("http://127.0.0.1:8000/api/get_lang/?video_name="+video_full_name)
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            var langs=data["subtitles"].map((item,index)=>{
                return item["language"];
            })
            setlanguages(langs);
        })
    },[video_full_name])

    useEffect(()=>{
        if(!languageref.current){
            return;
        }
        if(languageref.current.value==""){
            return 
        }
        if(time<endTime && time>startTime){
            return
        }
        fetch("http://127.0.0.1:8000/api/get_current_subtitle/?video_name="+short_name+"&time="+time+"&language="+languageref.current.value)
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            if(data.subtitle.length<1){
                return;
            }
            setstartTime(Math.floor(parseFloat(data.subtitle[0]['startSecond'])))
            setEndTime(Math.floor(parseFloat(data.subtitle[0]['endSecond'])))
            setcaption(data.subtitle[0]["caption"]);
        })
    },[video_full_name,time])

    return (
        <div>
            <div>
                {caption}
            </div>
            {languages!=[]?
            <select ref={languageref}>
                {languages.map((item,idx)=>{
                    if(idx===0){
                        return (
                            <option key={item} value={item} >{item}</option>
                        )
                    }
                    return (
                        <option key={item} value={item}>{item}</option>
                    )
                })} 
            </select>
:null}


        </div>
    )
}
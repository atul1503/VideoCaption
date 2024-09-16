import { useEffect,useState } from "react"
import { useDispatch } from "react-redux"

export default function History(){
    const [names,setnames]=useState([])
    const dispatch=useDispatch();


    useEffect(()=>{
        fetch("http://127.0.0.1:8000/api/get_all_files/")
        .then(response=>response.json())
        .then((data)=>{
            data=data.subtitles;
            //console.log(data);
            console.log(data[0]["name"]);
            setnames(data.map((item,idx)=>{
              return item["name"];  
            }))
        })
    },[])


    return(
        <div>
             <ul>
                {names.map((item,idx)=>{
                    return(
                        <li onClick={()=>{
                                dispatch({
                                    type: "set video name",
                                    payload: item
                                })
                                dispatch({
                                    type: "set app context",
                                    payload: "operations"
                                })
                        }}>
                           {item.split("/").pop()} 
                        </li>
                    )
                })}
             </ul>
        </div>
    )
}
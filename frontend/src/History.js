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
            if(data.length<1){
                return;
            }
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
                        <li 
                        
                        style={{ 
                            cursor: 'pointer', 
                            backgroundColor: 'lightblue',
                            padding: '10px',
                            border: '1px solid #ccc',
                            margin: '5px 0'
                        }}
                        
                        onClick={()=>{
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
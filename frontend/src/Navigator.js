import { useContext } from "react"
import { AppContext } from "./App"
import { useDispatch } from "react-redux";


export default function Navigator(){
    const dispatch=useDispatch();

    return(
        <div>
            <div onClick={()=>{

                dispatch({
                    type: "set app context",
                    payload: "history"
                })

            }}>History</div>
            <div onClick={()=>{
                
                dispatch({
                    type: "set app context",
                    payload: "upload"
                })

            }}>Upload</div>
            <div onClick={()=>{
                
                dispatch({
                    type: "set app context",
                    payload: "operations"
                })

            }}>Operations</div>
        </div>
    )
}
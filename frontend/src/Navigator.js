import { useContext } from "react"
import { AppContext } from "./App"
import { useDispatch } from "react-redux";


export default function Navigator(){
    const dispatch=useDispatch();

    return(
        <div style={{
            display : 'flex',
            //justifyContent: "space-between"
        }}>
            <div style={{
                marginRight: '300px',
                marginLeft: '100px',
                backgroundColor: 'blue', color: 'white'
            }} onClick={()=>{

                dispatch({
                    type: "set app context",
                    payload: "history"
                })

            }}>History</div>
            <div style={{
                marginRight: '300px',
                backgroundColor: 'blue', color: 'white'
            }} onClick={()=>{
                
                dispatch({
                    type: "set app context",
                    payload: "upload"
                })

            }}>Upload</div>
            <div style={{
                marginRight: '300px',
                backgroundColor: 'blue', color: 'white'
            }} onClick={()=>{
                
                dispatch({
                    type: "set app context",
                    payload: "operations"
                })

            }}>Operations</div>
        </div>
    )
}
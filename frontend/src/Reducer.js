
const initState={
    appContext: "history",
    timestamp: 0,
    startTime: 0,
    video_src: "",
    video_full_name: "/Users/attripathi/Projects/VideoCaption/media/test2.mkv.webm"
}


const reducer=(state=initState,action)=>{
    switch(action.type){
        case "update start time":
            //console.log("got time "+action.payload)
            return{
                ...state,
                startTime: action.payload
            }

        case "update timestamp":
            return {
                ...state,
                timestamp: action.payload
            }
        case "set player":
            return {
                ...state,
                playerRef: action.payload
            }


        case "set app context":
            return {
                ...state,
                appContext: action.payload
            }
        
        case "set video url":
            return {
                ...state,
                video_src: action.payload
            }

        case "set video name": 
            return {
                ...state,
                video_full_name: action.payload
            }
        default:
            return state
    }
}

export default reducer;
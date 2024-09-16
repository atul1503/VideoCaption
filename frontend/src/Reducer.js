
const initState={
    appContext: "history",
    timestamp: 0,
    playerRef: null,
    video_src: "",
    video_full_name: "/Users/attripathi/Projects/VideoCaption/media/test1.webm"
}


const reducer=(state=initState,action)=>{
    switch(action.type){
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
        default:
            return state
    }
}

export default reducer;
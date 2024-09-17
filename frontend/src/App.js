import { createContext, useState } from "react";
import Navigator from "./Navigator";
import History from "./History";
import Upload from "./Upload";
import Operations from "./Operations";
import { useSelector } from "react-redux";



function App() {

  console.log(process.env);
  const ctx=useSelector(state=>state.appContext);

  // history, upload, operations

  return (
    <div className="App">

      <Navigator/>
      {ctx==="history"?<History/>:ctx==="upload"?<Upload/>:ctx==="operations"?<Operations/>:null}
      
    </div>
  );
}

export default App;

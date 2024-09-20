import { useEffect, useState } from "react";

export default function Upload() {
  const [id, setId] = useState(0);
  const [status, setStatus] = useState("not started");

  useEffect(() => {
    if (id === 0) return;

    const interval = setInterval(() => {
      fetch(`http://127.0.0.1:8000/api/poll_status/?id=${id}`)
        .then(response => response.json())
        .then(data => {
          console.log(data.status);
          if (data.status === "SUCCESS") {
            setStatus("success");
            clearInterval(interval); // Stop further polling
          }
          else if(data.status === "FAILURE"){
            setStatus("failed")
            clearInterval(interval); // Stop further polling
          }
          else{
            setStatus("pending")
          }
        });

    }, 1000);

    // Cleanup on unmount or on id/success change
    return () => clearInterval(interval);
  }, [id]);

  const uploadFile = (event) => {
    const formData = new FormData();
    formData.append('file', event.target.files[0]);

    fetch("http://127.0.0.1:8000/api/upload_and_process/", {
      method: 'POST',
      body: formData
    }).then(response => response.json())
      .then(data => {
        const taskId = data.task_id;
        setId(taskId);
      });
  };

  return (
    <div>
      <input type="file" onChange={uploadFile} />
      {id !== 0
            ? <div>Upload and processing: {status}</div>
            : null
      }
    </div>
  );
}
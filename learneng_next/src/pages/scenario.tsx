import { useEffect } from "react";

const ScenarioPage = () => {
  useEffect(() => {
    const triggerChatPost = async () => {
      try {
        // Send the POST request to the backend (Express server)
        const response = await fetch("http://localhost:3000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: "", // Empty or default message
          }),
        });

        if (response.ok) {
          // If the response is successful, parse it
          const data = await response.json();
          console.log("Server response:", data);

          // You can now use `data.audio` and `data.lipsync` as needed
        } else {
          console.error("Error in response:", response.statusText);
        }
      } catch (error) {
        console.error("Error triggering chat:", error);
      }
    };

    // Trigger the POST request after the page loads
    triggerChatPost();
  }, []);

  return <div>Scenario page content</div>;
};

export default ScenarioPage;


// const Scenario = () => {
//     const [message, setMessage] = useState("Loading");

//     useEffect(() => {
//         fetch("http://127.0.0.1:5000/api/data")
//         .then((response) => response.json())
//         .then((data) => {
//             setMessage(data.response);
//             console.log(message);
//         })
//     }, []);

//     // Send a POST request to Flask when the page loads
//     const [response, setResponse] = useState<string>("");

//     const handleButtonClick = async () => {
//         fetch("http://127.0.0.1:5000/api/data")
//         .then((response) => response.json())
//         .then((data) => {
//             setMessage(data.response);
//             console.log(message);
//         })
//     };

//   return (
//     <div>
//         <div>{message}</div>
//       <h1>Next.js AJAX Example</h1>
//       <p>Response from Flask: {response}</p>
//       <button onClick={handleButtonClick} className="btn btn-primary">Fetch From Flask</button>
//       {response && <p>Response: {response}</p>}
//     </div>
//   );
// };

// export default Scenario;

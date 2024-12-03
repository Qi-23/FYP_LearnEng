import { lipSyncMessage, audioFileToBase64, readJsonTranscript } from '../../utils/lipSync'; // Import your utility functions here

export default async function handler(req, res) {
    // const response = await fetch("http://127.0.0.1:5000/api/chat", {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ message: "Hello from the client!" })
    // });
    if (req.method === "GET") {
        const userMessage = req.body.message;

        let audioName = "";
        if (!userMessage) {
            try {
                // the initial message is initialized with the below python backend
                // the audio file will be saved in audios folder
                // passing back the voice file name
                // the audio file should be in learneng_net/public/audios/audioName.mp3
                console.log('Fetching data from Python backend...');

                // Fetching audio data from the Python backend

                // --------------------------------------
                
                // const response = await fetch("http://127.0.0.1:5000/api/chat")
                // const data = await response.json();
                // const message = data.tts_audio_name;

                // console.log(message);

                // res.status(200).json({ message });

                // --------------------------------------
                
                const response = await fetch("http://127.0.0.1:5000/api/chat");

                if (!response.ok) {
                    console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                    throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
                }

                const data = await response.json();
                audioName = data.tts_audio_name;
                console.log("Audio name from Python:", audioName);

                // Ensure the audio name is not empty
                if (!audioName) {
                    throw new Error('Audio name is empty');
                }

                // Your processing logic for lip sync
                const fileName = `public/audios/${audioName}`; // Adjust path if necessary
                await lipSyncMessage(fileName);
                
                // Convert audio file to base64 and read lipsync data
                const audioData = await audioFileToBase64(fileName);
                const lipsyncData = await readJsonTranscript(fileName);

                // Send the final response with audio and lipsync data
                res.status(200).json({
                    audio: audioData,
                    lipsync: lipsyncData,
                });
            } catch (error) {
                console.error("Error:", error);
                res.status(500).json({ error: "Failed to fetch data from Python backend or process audio." });
            }
        } else {
            // Handle user message processing here if needed
            console.log("Processing with user message:", userMessage);
            // Example: You could return a response based on the userMessage
            res.status(200).json({ message: "User message received", userMessage });
        }
    } else {
        // Handle unsupported HTTP methods (e.g., GET)
        res.status(405).json({ error: "Method Not Allowed" });
    }
}

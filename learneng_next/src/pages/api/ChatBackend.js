import { lipSyncMessage, audioFileToBase64, readJsonTranscript } from '../../utils/lipSync'; // Import your utility functions here

export default async function handler(req, res) {
    if (req.method === "POST") {
        const userMessage = req.body.message;

        let audioName = "";
        if (!userMessage) {
            try {
                // the initial message is initialized with the below python backend
                // the audio file will be saved in audios folder
                // passing back the voice file name
                // the audio file should be in learneng_net/public/audios/audioName.mp3
                const response = await fetch("http://127.0.0.1:5000/api/data");
                const data = await response.json();
                audioName = data.tts_audio_name;
                console.log("Audio name from Python:", audioName);

                // Your processing logic for lip sync
                const fileName = `/audios/${audioName}.mp3`;
                await lipSyncMessage(audioName);
                const audioData = await audioFileToBase64(fileName);
                const lipsyncData = await readJsonTranscript(`/audios/${audioName}.json`);

                // Send the final response with audio and lipsync data
                res.status(200).json({
                    audio: audioData,
                    lipsync: lipsyncData,
                });
            } catch (error) {
                console.error("Error fetching data from Python backend:", error);
                res.status(500).json({ error: "Failed to fetch data from Python backend" });
            }
        } else {
            console.log("Processing with user message:", userMessage);
            // Handle user message processing here if needed
        }
    }
};
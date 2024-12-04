import { lipSyncMessage, audioFileToBase64, readJsonTranscript } from '../utils/lipSync.js'; // Import your utility functions here

export const ChatBackend = async (req, res) => {
    if (req.method === "POST") {
        let response = "";
        try {
            const { response_type } = req.body
            if (response_type == "init") {
                response = await fetch("http://127.0.0.1:5000/start_chat", { method: 'POST' });
            } else if (response_type == "cont") {
                response = await fetch("http://127.0.0.1:5000/next_chat", { method: 'POST' });
            }

            if (!response.ok) {
                console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
            }

            const data = await response.json();
            const audioName = data.audio_name;
            const audioType = data.audio_type;
            // const audioName = "initial_output";
            // const audioType = ".mp3";
            console.log("Audio name from Python:", audioName);

            if (!audioName) {
                throw new Error('Audio name is empty');
            }

            const fileName = `public/audios/${audioName}`;
            await lipSyncMessage(fileName, audioType);

            const audioData = await audioFileToBase64(fileName);
            const lipsyncData = await readJsonTranscript(fileName);

            res.status(200).json({
                audio: audioData,
                lipsync: lipsyncData,
            });

        } catch (error) {
            console.error("Error:", error);
            res.status(500).json({ error: "Failed to fetch data from Python backend or process audio." });
        }
    } else {
        console.log("Get ChatBackend");
        res.status(200).json({ message: "Get ChatBackend" });
    }
}

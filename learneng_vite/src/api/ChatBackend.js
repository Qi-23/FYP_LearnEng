import { lipSyncMessage, audioFileToBase64, readJsonTranscript } from '../utils/lipSync.js'; // Import your utility functions here

export const ChatBackend = async (req, res) => {
    if (req.method === "POST") {
        let response = "";
        const maxAttempts = 3;
        let attempt = 0;

        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        while (attempt < maxAttempts) {
            try {
                const { response_type } = req.body
                const { id } = req.body

                if (response_type == "init") {
                    // post with scenario id
                    response = await fetch("http://127.0.0.1:5000/start_chat", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ id: id })
                    });
                } else if (response_type == "cont") {
                    response = await fetch("http://127.0.0.1:5000/next_chat", { method: 'POST' });
                }

                if (!response.ok) {
                    console.error(`Attempt ${attempt + 1}: Failed to fetch from Python backend: ${response.statusText}`);
                    if (attempt === maxAttempts - 1) {
                        throw new Error(`Failed to fetch from python backend after ${maxAttempts} attempts: ${response.statusText}`);
                    }
                    await delay(300);
                    
                } else {
                    const data = await response.json();
                    const audioName = data.audio_name;
                    const audioType = data.audio_type;

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
                    break;
                }
            } catch (error) {
                console.error(`Attempt ${attempt + 1}: Error fetching scenario -`, error);
                if (attempt === maxAttempts - 1) {
                    return res.status(500).json({ message: "Failed to fetch data from Python backend or process audio after multiple attempts." });
                }
                attempt++;

                await delay(300);
            }
        }
    } else {
        console.log("Get ChatBackend");
        res.status(200).json({ message: "Get ChatBackend" });
    }
}

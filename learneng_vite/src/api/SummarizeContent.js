export const SummarizeContent = async (req, res) => {
    if (req.method === "GET") {
        const maxRetries = 2; // Maximum number of retries
        let attempt = 0;
        let response;
    
        while (attempt <= maxRetries) {
            try {
                response = await fetch("http://127.0.0.1:5000/get_summarized_content", { method: 'GET' });
    
                if (!response.ok) {
                    console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                    throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
                }
    
                let data = await response.json();
                console.log(data.summarized_content);
    
                res.status(200).json({
                    summarized_content: data.summarized_content
                });
                return;
            } catch (error) {
                console.error(`Attempt ${attempt + 1} failed. Error:`, error);
    
                if (attempt === maxRetries) {
                    res.status(500).json({ error: "Failed to summarize content after multiple attempts." });
                    return;
                }
    
                attempt++;
            }
        }
    }     else if (req.method === "POST") {
        try {
            const { id } = req.body
            if (id) {
                let response = await fetch("http://127.0.0.1:5000/get_summarized_content?id=" + id, { method: 'GET' })
                if (!response.ok) {
                    console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                    throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
                }
                let summarized_content = await response.json();
                res.status(200).json({ message: "Scenario fetched successfully", summarized_content: summarized_content });
            } else {
                res.status(500).json({ message: "None Scenario" });
            }
        } catch (error) {
            console.error("Error:", error);
            res.status(500).json({ error: "Failed to process scenario." });
        }
    } else {
        res.status(405).json({ message: "Method not allowed" });
    }
}


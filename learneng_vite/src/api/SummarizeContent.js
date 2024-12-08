export const SummarizeContent = async (req, res) => {
    if (req.method === "GET") {
        let response = "";
        try {
            response = await fetch("http://127.0.0.1:5000/get_summarized_content", { method: 'GET' });
            const data = await response.json();
            console.log(data.summarized_content);

            if (!response.ok) {
                console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
            }

            res.status(200).json({
                summarized_content: data.summarized_content
            });

        } catch (error) {
            console.error("Error:", error);
            res.status(500).json({ error: "Failed to summarize content." });
        }
    } else {
        console.log("Get SummarizedContent");
        res.status(200).json({ message: "Get SummarizedContent" });
    }
}


export const ScenarioConfig = async (req, res) => {
    if (req.method === "POST") {
        try {
            const { id } = req.body;
            console.log(id);

            if (!id) {
                return res.status(400).json({ message: "Scenario ID is required." });
            }

            const maxAttempts = 3;
            let attempt = 0;
            let scenario;

            const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

            while (attempt < maxAttempts) {
                try {
                    let response = await fetch(`http://127.0.0.1:5000/scenario/get_scenario_info?id=${id}`, { method: 'GET' });

                    if (!response.ok) {
                        console.error(`Attempt ${attempt + 1}: Failed to fetch from Python backend: ${response.statusText}`);
                        if (attempt === maxAttempts - 1) {
                            throw new Error(`Failed to fetch scenario after ${maxAttempts} attempts: ${response.statusText}`);
                        }
                        await delay(300); 
                    } else {
                        scenario = await response.json();
                        break;  // Exit loop if successful
                    }
                    attempt++;

                } catch (error) {
                    console.error(`Attempt ${attempt + 1}: Error fetching scenario -`, error);
                    if (attempt === maxAttempts - 1) {
                        return res.status(500).json({ message: "Failed to fetch scenario after multiple attempts." });
                    }
                    attempt++;

                    await delay(300);
                }
            }
            res.status(200).json({ message: "Scenario fetched successfully", scenario: scenario });

        } catch (error) {
            console.error("Error:", error);
            res.status(500).json({ error: "Failed to process scenario." });
        }
    } else {
        res.status(405).json({ message: "Method not allowed" });
    }
};

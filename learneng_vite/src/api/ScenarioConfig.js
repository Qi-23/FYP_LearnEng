export const ScenarioConfig = async (req, res) => {
    if (req.method === "POST") {
        try {
            const { id } = req.body
            console.log(id)
            if (id) {
                let response = await fetch("http://127.0.0.1:5000/scenario/get_scenario_info?id=" + id, { method: 'GET' })
                if (!response.ok) {
                    console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                    throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
                }
                let scenario = await response.json();
                res.status(200).json({ message: "Scenario fetched successfully", scenario: scenario });
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
};

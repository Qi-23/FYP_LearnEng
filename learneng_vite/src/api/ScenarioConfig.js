let scenario = null
let level = null
export const ScenarioConfig = async (req, res) => {
    if (req.method === "POST") {
        try {
            // const parsedData = JSON.parse(scenario);
            let load = req.body
            if (load.process && load.process === "loadScenario") {
                scenario = load.scenario
                res.status(200).json({ message: "Scenario processed successfully", scenario });
            } else if (load.process && load.process === "addScenario") {
                level = load.level.id
                scenario = null
                res.status(200).json({ message: "New scenario processed successfully", level });
            } else {
                scenario = null
                level = null
                res.status(500).json({ message: "None Scenario" });
            }
        } catch (error) {
            console.error("Error:", error);
            res.status(500).json({ error: "Failed to process scenario." });
        }
    } else if (req.method === "GET") {
        try {
            if (scenario) {
                let response = await fetch("http://127.0.0.1:5000/scenario/get_scenario_info?id=" + scenario.id, { method: 'GET' })
                if (!response.ok) {
                    console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                    throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
                }
                let scenario = await response.json();
                res.status(200).json({ message: "Scenario fetched successfully", scenario: scenario });
            } else if (level) {
                res.status(200).json({ message: "Level fetched successfully", level: level });
            } else {
                res.status(300).json({ message: "error get" });
            }
        } catch (error) {
            console.error("Error fetching scenario:", error);
            res.status(500).json({ error: "Failed to fetch scenario." });
        }
    } else {
        res.status(405).json({ message: "Method not allowed" });
    }
};

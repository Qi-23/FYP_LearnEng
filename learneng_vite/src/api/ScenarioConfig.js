let scenario = null
export const ScenarioConfig = async (req, res) => {
    if (req.method === "POST") {
        try {
            try {
                // const parsedData = JSON.parse(scenario);
                let load = req.body
                if (load.process && load.process === "loadScenario") {
                    scenario = load.scenario
                    console.log("Scenario data:", scenario)
                } else {
                    scenario = null
                }
            } catch (error) {
                console.error("Error parsing JSON:", error);
            }
            // Process the scenario here
            res.status(200).json({ message: "Scenario processed successfully", scenario });
        } catch (error) {
            console.error("Error:", error);
            res.status(500).json({ error: "Failed to process scenario." });
        }
    } else if (req.method === "GET") {
        try {
            if (scenario) {
                let response = await fetch("http://127.0.0.1:5000/scenario/get_scenario_info?id=" + scenario.id, { method: 'GET' })
                // console.log(response)
                if (!response.ok) {
                    console.error(`Failed to fetch from Python backend: ${response.statusText}`);
                    throw new Error(`Failed to fetch from Python backend: ${response.statusText}`);
                }
                let load = await response.json();
                console.log(load)
                scenario = load
            }
            res.status(200).json({ message: "Scenario fetched successfully", scenario: scenario });
        } catch (error) {
            console.error("Error fetching scenario:", error);
            res.status(500).json({ error: "Failed to fetch scenario." });
        }
    } else {
        res.status(405).json({ message: "Method not allowed" });
    }
};

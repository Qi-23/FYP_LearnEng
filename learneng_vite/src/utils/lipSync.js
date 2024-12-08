import { exec } from "child_process";
import { promises as fs } from "fs";

const execCommand = (command) => {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) reject(error);
            resolve(stdout);
        });
    });
};

export const readJsonTranscript = async (file) => {
    file = file + '.json';
    const data = await fs.readFile(file, "utf8");
    return JSON.parse(data);
};

export const audioFileToBase64 = async (file) => {
    try {
        file = file + '.mp3';
        console.log(`Processing file convert for: ${file}`);
        const data = await fs.readFile(file);
        return data.toString("base64");
    } catch (error) {
        console.error("Error in lipSyncMessage:", error);
        throw new Error("Lip sync processing failed");
    }
};


export const lipSyncMessage = async (message, audioType) => {
    const time = new Date().getTime();
    console.log(`Starting conversion for message ${message}`);

    if (audioType == ".mp3") {
        await execCommand(
            `ffmpeg -y -i ${message}.mp3 ${message}.wav`
            // -y to overwrite the file
        );
        console.log(`Conversion done in ${new Date().getTime() - time}ms`);
    }
    
    await execCommand(
        `bin\\rhubarb -f json -o ${message}.json ${message}.wav -r phonetic`
    );
    // -r phonetic is faster but less accurate
    console.log(`Lip sync done in ${new Date().getTime() - time}ms`);
};
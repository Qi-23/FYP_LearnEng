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

const readJsonTranscript = async (file) => {
    const data = await fs.readFile(file, "utf8");
    return JSON.parse(data);
};

const audioFileToBase64 = async (file) => {
    const data = await fs.readFile(file);
    return data.toString("base64");
};

const lipSyncMessage = async (message) => {
    const time = new Date().getTime();
    console.log(`Starting conversion for message ${message}`);
    await execCommand(
        `ffmpeg -y -i /audios/${message}.mp3 /audios/${message}.wav`
        // -y to overwrite the file
    );
    console.log(`Conversion done in ${new Date().getTime() - time}ms`);
    await execCommand(
        `./bin/rhubarb -f json -o /audios/${message}.json /audios/${message}.wav -r phonetic`
    );
    // -r phonetic is faster but less accurate
    console.log(`Lip sync done in ${new Date().getTime() - time}ms`);
};
import multer from 'multer';
import path from 'path';

const backgroundImageStorage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = path.join(process.cwd(), 'public', 'background');
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        const uploadPath = path.join(process.cwd(), 'public', 'background', file.originalname);

        if (fs.existsSync(uploadPath)) {
            console.log(`File ${file.originalname} exists and will be replaced.`);
        }
        cb(null, file.originalname); 
    },
});

const scenarioImageStorage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = path.join(process.cwd(), 'public', 'page_photo');
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        const uploadPath = path.join(process.cwd(), 'public', 'page_photo', file.originalname);

        // Check if a file with the same name exists
        if (fs.existsSync(uploadPath)) {
            console.log(`File ${file.originalname} exists and will be replaced.`);
        }
        cb(null, file.originalname); 
    },
});

const uploadBackgroundImage = multer({ backgroundImageStorage });
const uploadScenarioImage = multer({ scenarioImageStorage });

export const UploadImage = async (req, res) => {
    if (req.method === "POST") {
        try {
            let load = req.body
            console.log(load)
            if (load.imageType === "backgroundImage") {
                uploadBackgroundImage.single('scenarioImage')(req, res, (err) => {
                    if (err) {
                        console.error("Upload Error:", err);
                        return res.status(500).json({ error: "Failed to upload image." });
                    }

                    const filePath = `/background/${req.file.filename}`;
                    console.log("Uploaded File Path:", filePath);

                    res.status(200).json({ message: "Image uploaded successfully", filePath });
                });
            } else if (load.imageType === "scenarioImage") {
                uploadScenarioImage.single('scenarioImage')(req, res, (err) => {
                    if (err) {
                        console.error("Upload Error:", err);
                        return res.status(500).json({ error: "Failed to upload image." });
                    }

                    const filePath = `/page_photo/${req.file.filename}`;
                    console.log("Uploaded File Path:", filePath);

                    res.status(200).json({ message: "Image uploaded successfully", filePath });
                });
            }
        } catch (error) {
            console.error("Error:", error);
            res.status(500).json({ error: "Failed to upload image." });
        }
    } else {
        console.log("Get SummarizedContent");
        res.status(200).json({ message: "Get SummarizedContent" });
    }
}


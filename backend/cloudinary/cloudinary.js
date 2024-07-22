import { v2 as cloudinary } from 'cloudinary';
import {fileURLToPath} from 'url';
import path from "path";

const __filename = fileURLToPath(import.meta.url);

// 👇️ "/home/john/Desktop/javascript"
const __dirname = path.dirname(__filename);

// Configuración de Cloudinary
cloudinary.config({
    cloud_name: process.env.CLOUD_NAME,
    api_key: process.env.API_KEY_CLOUD,
    api_secret: process.env.API_SECRET_CLOUD
});

export const uploadFunction = async (filePath) => {
    const options = {
        use_filename: true,
        unique_filename: false,
        overwrite: true,
        resource_type: 'auto',
        //format: 'mp3'
    };

    try {
        const result = await cloudinary.uploader.upload(filePath, { resource_type: "video" }, (error, result) => {
            if (error) {
                console.error('Error al subir el archivo:', error);
            } else {
                console.log('Archivo subido exitosamente:', result);
            }
        });
        console.log(result);
        return result.secure_url;
    } catch (error) {
        console.error(error);
    }
}

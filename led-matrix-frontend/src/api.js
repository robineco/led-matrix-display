const axios = require('axios');

const createImage = async (grid, save) => {
    const headers = {
        'Content-Type': 'application/json',
    };
    const data = {
        image: grid,
        save: save,
    }
    const response = await axios.post('http://192.168.178.62:5000/image', data, {headers});

    return  response.data;
};

const readFile = async (file) => {
    return new Promise((resolve, reject) => {
        let reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = () => {
            resolve(reader.result);
        };

        reader.onerror = reject;
    })
}

const uploadImage = async (image) => {
    const encoded = await readFile(image);
    const headers = {
        'Content-Type': 'application/json',
    };
    const data = {
        image: encoded,
    };
    const response = await axios.post('http://192.168.178.62:5000/image/matrix', data, {headers});

    return response.data;

}

export {
    createImage,
    uploadImage,
}

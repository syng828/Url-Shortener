import axios from 'axios';
import { ApiResponse } from './ApiResponse';

let BASE_URL = "http://127.0.0.1:8000";

export async function getAllUrls() {
    let status = new ApiResponse();
    await axios.get(BASE_URL + '/list_all')
        .then(res => {
            status.responseData = res.data;
        })
        .catch(err => {
            status.responseData = err;
            status.error = true;
        });
    return status;
}

export async function addUrl(requestBody) {
    let status = new ApiResponse();
    await axios.post(BASE_URL + '/create_url', requestBody).then(res => {
        status.responseData = res.data
    })
        .catch(err => {
            status.responseData = err;
            status.error = true;
        });
    return status;
}

export async function deleteAlias(alias) {
    let status = new ApiResponse();
    await axios.post(BASE_URL + '/delete/' + alias).then(res => {
        status.responseData = res.data
    }).catch(err => {
        status.responseData = err;
        status.error = true;
    })
    return status;
}

//TODO: right lets test that this all works first. just open up your backend and analyze the response first
//oh but to do that you need to create the inputs option
//once it works add in the table too with the useEffect
//add the randomizer toggle. good for today

//TODO: Add in error rendering, loading regex, css, and the requirements.txt
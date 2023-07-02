
import axios from 'axios'
let server_address = 'http://localhost:14449'

export function getMediaData(callback) {
    // let formData = {"mediaDataSet": params1}
    axios({
        methods: 'get',
        url: server_address + '/media_dataset',
        // params: formData,
        timeout: 1000000
    })
    .then((res) => {
        let mediaDataSet = res["data"]["data"];
        console.log('mediaDataSet:', mediaDataSet);
        callback(mediaDataSet);
    })
}

export function getMediaMatrixData(callback) {
    axios({
        methods: 'get',
        url: server_address + '/media_matrix_dataset',
        // params: formData,
        timeout: 1000000
    })
    .then((res) => {
        let mediaMatrixData = res["data"]["data"];
        console.log('mediaMatrixData:', mediaMatrixData);
        callback(mediaMatrixData);
    })
}
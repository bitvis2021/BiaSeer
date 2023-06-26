
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
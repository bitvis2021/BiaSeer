
import axios from 'axios'
let server_address = 'http://localhost:14449'

export function getSelectedTopMedia(mediaTopDataList, getMediaTopDataCallback) {
    let formData = {"mediatopData": mediaTopDataList}
    axios({
        methods: 'get',
        url: server_address + '/media_top_data',
        params: formData,
        timeout: 1000000
    })
    .then((res) => {
        let mediaTopDatasetList = res["data"]["data"]
        // console.log("mediaTopDatasetList", mediaTopDatasetList)
        getMediaTopDataCallback(mediaTopDatasetList)
    })
}
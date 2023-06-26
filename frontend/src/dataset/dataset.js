export function Dataset () {
    this.buildingDatasetList = [];

    this.mediaDataSet = null;
}

Dataset.prototype = {
    init: function() {
    },
    updateBuildingDatasetList: function(data) {
        this.buildingDatasetList = data
    },

    updateMediaDataSet: function(data) {
        this.mediaDataSet = data
    }
}
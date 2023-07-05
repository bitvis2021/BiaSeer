export function Dataset () {
    this.buildingDatasetList = [];

    this.mediaDataSet = null;

    this.mediaMatrixDataSet = null;

    this.mediaMatrixSelected = null;
}

Dataset.prototype = {
    init: function() {
    },
    updateBuildingDatasetList: function(data) {
        this.buildingDatasetList = data;
    },

    updateMediaDataSet: function(data) {
        this.mediaDataSet = data;
    },

    updateMediaMatrixDataSet: function(data) {
        this.mediaMatrixDataSet = data;
    },

    updateMediaMatrixSelected: function(data) {
        // console.log(data);
        this.mediaMatrixSelected = data;
    }
}
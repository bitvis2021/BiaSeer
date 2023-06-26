export function Dataset () {
    this.buildingDatasetList = [];
}

Dataset.prototype = {
    init: function() {
    },
    updateBuildingDatasetList: function(data) {
        this.buildingDatasetList = data
    }
}
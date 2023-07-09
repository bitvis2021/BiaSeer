export function Dataset () {
    this.buildingDatasetList = [];

    this.mediaDataSet = null;

    this.mediaMatrixDataSet = null;

    this.mediaMatrixSelected = null;

    this.storyTreeDataset = null;


    this.mediaScatterSelected = [];
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
        this.mediaMatrixSelected = data;
    },

    updateStoryTreeDataset: function(data) {
        this.storyTreeDataset = data;
    },

    updateMediaScatterSelected: function(data) {
        if(this.mediaScatterSelected.indexOf(data)==-1){
            console.log(data + "不存在");
            this.mediaScatterSelected.push(data);
        }
        else{
            console.log(data + "已经存在");
        }
    }
}
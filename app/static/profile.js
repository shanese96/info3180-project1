var loadFile = function(event) {
    var output = document.getElementById('output');
    output.src = global.URL.createObjectURL(event.target.files[0]);
  };
function timer(){
    const start = Date.now();
    var ptmp = new Date();

    var t;
    var timer_is_on = 0;
    if (!timer_is_on) {
        var c = 0;
        timer_is_on = 1;

        timedCount();
        var fin = start + 1450
      }


    function timedCount() {
      var tempRest = fin - Date.now()
      if (tempRest > 0){
        document.getElementById("txt").value = tempRest;

      }
      else {
        document.getElementById("txt").value = "On est à 0";
      }
      t = setTimeout(timedCount, 1);




    }

}





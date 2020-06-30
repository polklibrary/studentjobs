var Activity = {
    refresh : function() {
        url = domain + '/activity?type=refresh';
        $.get(url, function(response){
        });
    },
    
    check : function() {
        url = domain + '/activity?type=check';
        $.get(url, function(response){
            if (response.logout == 1 && response.guest == 0)
            {
                alert("Your session has expired due to inactivity.");
                document.location.href = domain + '/logout'
            }
        });
    },
}

$(document).ready(function(){
    Activity.refresh();
    
    setInterval(function(){
        Activity.check();
    }, 1000 * 60); // one minute
});


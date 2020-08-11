var Activity = {
    
    RefreshThread : null,
    CheckThread : null,
    ForceRefresh : false,
    
    monitor : function(){
        $('body').bind('mousemove keydown', function(e) {
            Activity.ForceRefresh = true;
        });
    },
    
    refresh : function() {
        Activity.ForceRefresh = false;
        url = domain + '/activity?type=refresh';
        $.get(url, function(response){
        });
    },
    
    check : function() {
        url = domain + '/activity?type=check';
        $.get(url, function(response){
            if (response.logout == 1 && response.guest == 0)
            {
                clearInterval(Activity.CheckThread);
                alert("Your session has expired due to inactivity.");
                document.location.href = domain + '/logout'
            }
        });
    },
    
    
    
    
    
}

$(document).ready(function(){
    Activity.monitor();
    Activity.refresh();
    
    Activity.RefreshThread = setInterval(function(){
        if (Activity.ForceRefresh)
            Activity.refresh();
    }, 1000 * 60 * 2); // every X minutes
    
    Activity.CheckThread = setInterval(function(){
        Activity.check();
    }, 1000 * 60); // one minute
});


var Timeout = {
    
    Thread : null,
    TimeoutMinutes : 15,
    
    Initialize : function(){
        Timeout.Start();
        Timeout.Refresher();
    },
    
    
    Refresher : function(){
        $('body').bind('mousemove keydown', function(e) {
            Timeout.Reset();
        });
    },
    
    Reset : function(){
        Timeout.Stop();
        Timeout.Start();
    },
    
    Stop : function(){
        clearTimeout(Timeout.Thread);
        Timeout.Thread = null;
    },
    
    Start : function() {
        Timeout.Thread = setTimeout(function(){
            alert("Your session has expired due to inactivity.");
            document.location.href = domain + '/logout'
        }, 1000 * 60 * Timeout.TimeoutMinutes);
    },
}

$(document).ready(function(){
    Timeout.Initialize();
});


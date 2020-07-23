var Themer = {
    
    Backgrounds : [
        '1.jpg',
        '2.jpg',
        '3.jpg',
        '4.jpg',
        '5.jpg',
    ],
    
    init : function(){
        var bk = this.Backgrounds[Math.floor(Math.random()*this.Backgrounds.length)];
        var url = 'url(https://polk.uwosh.edu/studentjobs/themes/images/scenes/' + bk + ')';
        $('html').css('background-image', url);
    },
}
Themer.init();


var Formatter = {
    
    bool_to_friendly : function(v){
        v = (v + '').toLowerCase();
        if (v == 'false' || v == 'no' || v == '0' || v == 'no')
            return 'No';
        return 'Yes';
    },
    
    auto_size_heights : function() {
        var heights = {};
        $('.pat-auto-height').each(function(){
            var id = $(this).attr('data-hid');
            if (!heights.hasOwnProperty(id))
                heights[id] = 0;
            
            var h = $(this).height();
            if (heights[id] < h)
                heights[id] = h;
        })
        
        for(var k in heights)
            $('.pat-auto-height[data-hid="'+ k +'"]').css('min-height', heights[k]);
    },
}


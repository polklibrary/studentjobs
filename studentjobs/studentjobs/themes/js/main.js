

var Main = {
    
    
    initialize : function(){
        this.set_graduation_years();
        this.set_start_date();
        this.set_availability();
        this.prevent_precise_address();
        this.block_form_enter();
       // this.tester();
    },
    
    make_random_str : function(l) {
       var result           = '';
       var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz ';
       var charactersLength = characters.length;
       for ( var i = 0; i < l; i++ ) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength));
       }
       return result;
    }, 
    
    fill_test_data : function(){
        
        $('input').each(function(){
            if ($(this).attr('type') == 'checkbox')
                $(this).prop( "checked", true );
            else if ($(this).attr('type') == 'email')
                $(this).val("test@uwosh.edu");
            else if ($(this).attr('type') == 'tel')
                $(this).val("123-123-1234");
            else if ($(this).attr('type') == 'date')
                $(this).val("2020-06-01");
            else if ($(this).attr('type') == 'number')
                $(this).val(1000);
            else if ($(this).attr('type') == 'text')
                $(this).val(Main.make_random_str(15));
        });
        $('textarea').each(function(){
            $(this).val(Main.make_random_str(128));
        });
        // $('select').each(function(){
            // $(this).find('option:nth-child(1)').prop('selected', true);
        // });
        
        $('input[name="availability.monday"]').val('7:00 AM - 9:00 AM,');
        $('input[name="availability.thursday"]').val('10:00 AM - 12:00 PM,');
        
    },
    
    block_form_enter : function(){
        $(window).keydown(function(e){
            if(e.keyCode == 13) {
                e.preventDefault();
                return false;
            }
        });
    },
    
    prevent_precise_address : function(){
        $('.pattern-only-citystate').on('keyup',function(){
            var v = $(this).val();
            var HasNumber = /\d/.test(v);
            if (HasNumber){
                v = v.replace(/[0-9]/g, '');
                $(this).val(v);
                alert("Address and zip codes are NOT allowed.  Please only provide City and State.");
            }
        });
    },
    
    prevent_submission_unless_accepted : function(){
        $('#application-form').on('submit', function(){
            if($('#final-check').is(':checked'))
                return true;
            
            return false;
        });  
    },
    
    set_graduation_years : function(){
        var YearsAhead = 10;
        var Year = new Date().getFullYear();
        for(var i = Year; i < Year+YearsAhead; i++)
            $('#graduation-year').append($('<option>').val(i).html(i));
    },
    
    set_start_date : function() {
        var Now = new Date();
        var Day = Now.getDate();
        if (Day < 10)
            Day = '0' + Day;
        var Month = Now.getMonth() + 1;
        if (Month < 10)
            Month = '0' + Month;
        var Year = Now.getFullYear();
        $('#start-date').val(Year + '-' + Month + '-' + Day);
    },
    
    
    id_counter : 0,
    set_availability : function(){        
        
        $('#work-add-time').on('click', function(){
            //var new_id = Main.id_counter;
            //Main.id_counter++;
            var start_hour = $('#work-start-hour option:selected').val();
            var start_minute = $('#work-start-minute option:selected').val();
            var start_ampm = $('#work-start-ampm option:selected').val();
            
            var end_hour = $('#work-end-hour option:selected').val();
            var end_minute = $('#work-end-minute option:selected').val();
            var end_ampm = $('#work-end-ampm option:selected').val();

            var label_val = start_hour+':'+start_minute+' '+start_ampm+' - '+end_hour+':'+end_minute+' '+end_ampm;
            var input_val = start_hour+':'+start_minute+' '+start_ampm+' - '+end_hour+':'+end_minute+' '+end_ampm+',';

            var checkdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'];
            for(var i in checkdays)
                if ( $('#work-'+checkdays[i]).is(':checked')) {
                    var tc = Main.create_timecontrol(checkdays[i], input_val, label_val)
                    $('.' + checkdays[i] + ' .values').append(tc);
                }

            Main.recheck_unavailable();
        });
        
    },
    
    create_timecontrol : function(day, input_val, label_val){    
        day = day.toLowerCase();
        var iv = $('input[name="availability.' + day + '"]').val();

        if (iv.indexOf(input_val) == -1){
            iv += input_val;
            $('input[name="availability.' + day + '"]').val(iv);
            
            var span = $('<span>').addClass('time-option').attr({'data-day':day,'data-val':input_val, 'title':'Click to remove'}).html(label_val).on('click', function(){
                $(this).remove();
                var tv = $(this).attr('data-val');
                var d = $(this).attr('data-day');
                var v = $('input[name="availability.' + d + '"]').val();
                v = v.replace(tv, '');
                $('input[name="availability.' + d + '"]').val(v);
                Main.recheck_unavailable();
            });
            return span;
        }
        return null;
    },   
    
    recheck_unavailable : function(){
        var checkdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'];
        
        for(var i in checkdays)
            if($('input[name="availability.' + checkdays[i] + '"]').val().length < 5)
                $('.' + checkdays[i] + ' label').addClass("unavailable");
            else
                $('.' + checkdays[i] + ' label').removeClass("unavailable");
        
    }
    
}







$(document).ready(function(){
    Main.initialize();
});

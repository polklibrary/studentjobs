// FORCE HTTPS
if(document.location.hostname != 'localhost' && document.location.protocol != 'https:')
    document.location.href = document.location.href.replace('http:','https:')

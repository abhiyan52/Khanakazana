$(document).ready(()=>{
    $('.delete-button').click((event)=>{
        itemID = Number(event.target.getAttribute('data-item-id'));
        $.post('/api/owner/delete',{'id':itemID},(data,status)=>{
            event.target.style.display='none'
            if(data.code=='200') {
                window.location.replace(window.location.href)
            }   
                else{
                    pushAlert('Failed to delete',1)       
            }
                   
        });
    });
});
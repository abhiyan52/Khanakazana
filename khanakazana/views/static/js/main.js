$(document).ready(()=>{
  $('.cart-add').click(async (event)=>{
      target_button = event.target;
      flag = target_button.getAttribute('added')
      item_id = Number(event.target.getAttribute('data-item-id'));
      if(flag != 'true'){
      target_button.setAttribute('added','true')
      await addToCart(item_id);
      target_button.innerText = '-Remove'
      target_button.classList.remove('btn-primary')
      target_button.classList.add('btn-warning')
      }
      else {
      await addToCart(item_id,1)
      target_button.innerText = 'Add Item +'
      target_button.setAttribute('added','false')
      target_button.classList.add('btn-primary')
      target_button.classList.remove('btn-warning')
      target_button.classList.add('cart-add')
    
      }
      
  });
 

  getCategories().then((response)=>{
    categories_template = "#categories-template"
    categories_content = '#categories-content'
    renderTemplate(response.result, categories_template,categories_content)
  
    getRestaurants().then((response)=>{
      restaurant_template = "#restaurant-template"
      restaurant_content = '#restaurant-content'
      renderTemplate(response.result.slice(0,5), restaurant_template,restaurant_content)
    });

  });

  
});


async function addToCart(item_id,operation=0) {
  cartCountField = $('#item-count')
  cart_count = 0
  await $.post('/add_to_cart',{'operation_id': operation,'item_id': item_id},(data, status)=>{
    cartCountField.text(data.count)
    cart_count = Number(data.count) 
  });
  return cart_count;
}

function renderTemplate(data, template,content) {
  var theTemplateScript = $(template).html();
  var theTemplate = Handlebars.compile(theTemplateScript);
  var context={
    "data": data,
  };
  var theCompiledHtml = theTemplate(context);
  $(content).html(theCompiledHtml);
}

const getCategories = async ()=>{
    return new Promise((resolve, reject)=>{
     $.get('api/v1/categories', (data, status)=>{
        if(data.code == 200)
         resolve(data);
         else
         reject('Not valid')
     });
    });
 }

 const pushAlert = (message, type=0)=>{
    
   alertBox = $('#alert_box')
    alertBox.css('display','block')
    if(type==0){
      alertBox.addClass('alert-success')
    } else {
      alertBox.addClass('alert-danger')
    }
    $('#alert_box p').text(message)
 }

 const getRestaurants = async ()=>{
  return new Promise((resolve, reject)=>{
   $.get('api/v1/restaurants', (data, status)=>{
      if(data.code == 200)
       resolve(data);
       else
       reject('Not valid')
   });
  });
}

const requestLogin = async (event)=>{
  event.preventDefault();
  obj = {}
  data = $('#login-nav').serialize().split('&').map((element)=>{
   [key,value] = element.split('=')
   obj[key] = value
   return undefined; 
  });

  await $.post('/auth/login',obj,(data,status)=>{
     if(data.status == 'sucessful')
     window.location.replace(window.location.href)
     else 
     pushAlert('Please check your username password',1)
  });
 
return false;
}
